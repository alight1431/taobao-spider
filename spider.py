"""
淘宝商品搜索结果批量采集脚本
============================
作者: 季先生
日期: 2026-08
说明: 按关键词批量采集淘宝搜索结果，支持多页翻页与数据清洗
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import json
from typing import List, Dict, Optional


# ============================================================
# 配置区
# ============================================================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# 请求间隔（秒），避免被反爬
REQUEST_DELAY = (1.5, 3.0)

# 失败重试次数
MAX_RETRIES = 3


# ============================================================
# 核心功能
# ============================================================
def fetch_page(keyword: str, page: int) -> Optional[str]:
    """获取淘宝搜索页 HTML

    Args:
        keyword: 搜索关键词
        page: 页码（从 0 开始）

    Returns:
        HTML 文本；失败返回 None
    """
    # 淘宝搜索 URL 翻页参数：s = 页码 * 44
    url = f"https://s.taobao.com/search?q={keyword}&s={page * 44}"
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            resp.encoding = "utf-8"
            return resp.text
        except requests.RequestException as e:
            print(f"  [retry {attempt+1}/{MAX_RETRIES}] page {page+1} failed: {e}")
            time.sleep(random.uniform(2, 5))
    return None


def parse_items(html: str) -> List[Dict]:
    """从 HTML 中解析商品列表

    实际生产中需要根据淘宝最新页面结构动态调整，
    这里使用通用 JSON-LD 与正则提取示例。
    """
    items = []

    # 尝试提取嵌入的 JSON 数据
    json_match = re.search(r"g_page_config\s*=\s*({.+?});", html, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            # 此处根据实际 JSON 结构解析（仅作示例）
            print("  [debug] 找到嵌入 JSON 数据，长度:", len(json_match.group(1)))
        except json.JSONDecodeError:
            pass

    # 用 BeautifulSoup 兜底解析
    soup = BeautifulSoup(html, "lxml")

    # 提取商品卡片（选择器需根据实际页面调整）
    for card in soup.select("div.item, div.m-itemlist .items .item"):
        try:
            title_el = card.select_one(".title, h3")
            price_el = card.select_one(".price strong, .price-current")
            sales_el = card.select_one(".sale-num, .sales")
            shop_el = card.select_one(".shop a, .shopname")
            link_el = card.select_one("a")

            if not title_el or not price_el:
                continue

            item = {
                "title": title_el.get_text(strip=True),
                "price": clean_price(price_el.get_text()),
                "sales": clean_sales(sales_el.get_text() if sales_el else ""),
                "shop": shop_el.get_text(strip=True) if shop_el else "",
                "link": "https:" + link_el["href"] if link_el and link_el.get("href", "").startswith("//") else (link_el["href"] if link_el else ""),
            }
            items.append(item)
        except (AttributeError, KeyError) as e:
            continue

    return items


def clean_price(text: str) -> Optional[float]:
    """清洗价格文本：'¥199.00' -> 199.0"""
    if not text:
        return None
    match = re.search(r"[\d.]+", text.replace(",", ""))
    return float(match.group(0)) if match else None


def clean_sales(text: str) -> str:
    """清洗销量文本：'月销 1.2万+人付款' -> '1.2万+付款'"""
    if not text:
        return "0"
    text = re.sub(r"月销|月售", "", text)
    text = re.sub(r"人付款|人收货|笔", "", text)
    return text.strip()


def search_taobao(keyword: str, pages: int = 3) -> List[Dict]:
    """主函数：搜索淘宝商品

    Args:
        keyword: 搜索关键词，如 "蓝牙耳机"
        pages: 翻页数（每页 44 条）

    Returns:
        商品列表
    """
    print(f"🔍 开始采集: keyword={keyword}, pages={pages}")
    all_items = []

    for page in range(pages):
        print(f"  📄 正在抓取第 {page+1}/{pages} 页...")
        html = fetch_page(keyword, page)
        if not html:
            print(f"  ❌ 第 {page+1} 页失败，跳过")
            continue

        items = parse_items(html)
        all_items.extend(items)
        print(f"  ✅ 第 {page+1} 页解析到 {len(items)} 条")

        # 反爬延迟
        time.sleep(random.uniform(*REQUEST_DELAY))

    print(f"🎉 采集完成！共 {len(all_items)} 条数据")
    return all_items


def save_to_excel(items: List[Dict], filename: str = "taobao_items.xlsx") -> None:
    """保存为 Excel"""
    if not items:
        print("⚠️  无数据可保存")
        return
    df = pd.DataFrame(items)
    df.drop_duplicates(subset=["link"], inplace=True)  # 按链接去重
    df.to_excel(filename, index=False, engine="openpyxl")
    print(f"💾 已保存: {filename}（{len(df)} 条去重后数据）")


def save_to_csv(items: List[Dict], filename: str = "taobao_items.csv") -> None:
    """保存为 CSV"""
    if not items:
        print("⚠️  无数据可保存")
        return
    df = pd.DataFrame(items)
    df.drop_duplicates(subset=["link"], inplace=True)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"💾 已保存: {filename}（{len(df)} 条去重后数据）")


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    KEYWORD = "蓝牙耳机"
    PAGES = 3

    items = search_taobao(KEYWORD, pages=PAGES)
    save_to_excel(items, f"taobao_{KEYWORD}.xlsx")
    save_to_csv(items, f"taobao_{KEYWORD}.csv")
