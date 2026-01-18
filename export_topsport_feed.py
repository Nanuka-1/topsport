# =========================
# TOPSPORT -> META XML FEED
# =========================
# მიზანი: Topsport-ის კატეგორიიდან (ქალის ფეხსაცმელი) ყველა პროდუქტის ამოღება
# და Meta Catalog-ში ატვირთვადი XML (RSS + g:) ფიდის გენერირება.
#
# დამატებები:
# - g:google_product_category (კონსტანტით)
# - g:mpn (ვცდილობთ გამოვიღოთ პროდუქტის გვერდიდან; ეს +N request-ია)
#
# გაშვება:
# pip install requests beautifulsoup4 lxml
# python export_topsport_feed.py

from __future__ import annotations

import json
import re
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# -------------------------
# 1) საბაზო პარამეტრები
# -------------------------
BASE_URL = "https://topsport.ge"
CATEGORY_URL = "https://topsport.ge/ka/products/qalis-fekhsatsmeli"
OUTPUT_XML = "topsport_qalis_fekhsatsmeli.xml"

CURRENCY = "GEL"
SLEEP_SECONDS = 0.4  # სერვერზე ზედმეტი დატვირთვის თავიდან ასაცილებლად

# Meta/Google კატეგორია (სტაბილურად ერთნაირი)
GOOGLE_PRODUCT_CATEGORY = "Apparel & Accessories > Shoes"

# სტაბილური product_type (რადგან card-ზე ზოგჯერ არასრულია)
DEFAULT_PRODUCT_TYPE = "ქალი > ქალის ფეხსაცმელი"

# თუ გინდა გამორთო "მძიმე" ნაწილი (MPN ამოღება პროდუქტის გვერდიდან) -> False
FETCH_MPN = True

# სურვილისამებრ შეზღუდვები ტესტისთვის (None = შეუზღუდავი)
MAX_PAGES: Optional[int] = None
MAX_PRODUCTS: Optional[int] = None


# -------------------------
# 2) მონაცემის სტრუქტურა
# -------------------------
@dataclass
class Product:
    pid: str
    title: str
    link: str
    image_link: str
    brand: str
    category: str
    price: str
    sale_price: Optional[str]
    mpn: Optional[str] = None
    gtin: Optional[str] = None  # თუ ოდესმე გამოჩნდება (EAN/GTIN)


# -------------------------
# 3) HTML parser არჩევა (lxml თუ არ არის -> html.parser)
# -------------------------
def _choose_parser() -> str:
    try:
        import lxml  # noqa: F401
        return "lxml"
    except Exception:
        return "html.parser"


PARSER = _choose_parser()


# -------------------------
# 4) დამხმარე: HTTP + Soup
# -------------------------
def fetch_soup(session: requests.Session, url: str) -> BeautifulSoup:
    resp = session.get(url, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, PARSER)


# -------------------------
# 5) დამხმარე: ფასის წმენდა
# -------------------------
def normalize_price(text: str) -> str:
    """
    "399,00 ₾" / "399.00 GEL" -> "399.00 GEL"
    """
    s = (text or "").strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("₾", "").replace("GEL", "").strip()
    s = s.replace(",", ".")
    s = re.sub(r"[^0-9.]", "", s)

    if not s:
        return f"0.00 {CURRENCY}"

    if "." in s:
        left, right = s.split(".", 1)
        right = (right + "00")[:2]
        s = f"{left}.{right}"
    else:
        s = f"{s}.00"

    return f"{s} {CURRENCY}"


def extract_prices_from_card(card: BeautifulSoup) -> tuple[str, Optional[str]]:
    """
    ლოგიკა:
    - old + new -> price=old, sale_price=new
    - ერთი ფასი -> price=current, sale_price=None
    """
    price_box = card.select_one(".product-price")
    if not price_box:
        return (f"0.00 {CURRENCY}", None)

    old_el = price_box.select_one(".old-price, del, s")
    new_el = price_box.select_one(".current-price, .new-price, .text-brand")

    if old_el and new_el:
        old_price = normalize_price(old_el.get_text(" ", strip=True))
        new_price = normalize_price(new_el.get_text(" ", strip=True))
        if old_price == new_price:
            return (new_price, None)
        return (old_price, new_price)

    spans = price_box.find_all("span")
    texts = [sp.get_text(" ", strip=True) for sp in spans if sp.get_text(strip=True)]

    if len(texts) >= 2:
        old_price = normalize_price(texts[0])
        new_price = normalize_price(texts[-1])
        if old_price == new_price:
            return (new_price, None)
        return (old_price, new_price)

    if len(texts) == 1:
        return (normalize_price(texts[0]), None)

    return (f"0.00 {CURRENCY}", None)


# -------------------------
# 6) MPN/GTIN ამოღება პროდუქტის გვერდიდან (მძიმე ნაწილი)
# -------------------------
def _iter_jsonld_objects(obj):
    # JSON-LD შეიძლება იყოს dict, list, ან nested სტრუქტურა
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _iter_jsonld_objects(v)
    elif isinstance(obj, list):
        for x in obj:
            yield from _iter_jsonld_objects(x)


def fetch_identifiers_from_product_page(session: requests.Session, url: str) -> tuple[Optional[str], Optional[str]]:
    """
    მიზანი: პროდუქტის გვერდიდან მოვძებნოთ sku/mpn და gtin (თუ არის).
    პრიორიტეტი:
    1) JSON-LD (script type=application/ld+json)
    2) ტექსტური regex fallback გვერდის HTML-დან
    """
    try:
        soup = fetch_soup(session, url)
    except Exception:
        return (None, None)

    # 1) JSON-LD
    scripts = soup.select('script[type="application/ld+json"]')
    for sc in scripts:
        raw = (sc.string or sc.get_text() or "").strip()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue

        mpn = None
        gtin = None

        for d in _iter_jsonld_objects(data):
            # sku/mpn
            for key in ("mpn", "sku"):
                val = d.get(key)
                if isinstance(val, str) and val.strip():
                    mpn = mpn or val.strip()

            # gtin
            for key in ("gtin13", "gtin14", "gtin12", "gtin8", "gtin"):
                val = d.get(key)
                if isinstance(val, str) and val.strip():
                    gtin = gtin or val.strip()

            if mpn or gtin:
                return (mpn, gtin)

    # 2) fallback regex (სწრაფი, მაგრამ ნაკლებად საიმედო)
    text = soup.get_text(" ", strip=True)

    mpn_match = re.search(r"\b(?:SKU|MPN)\b\s*[:\-]?\s*([A-Z0-9\-]{3,})", text, flags=re.I)
    gtin_match = re.search(r"\b(?:GTIN|EAN)\b\s*[:\-]?\s*([0-9]{8,14})", text, flags=re.I)

    mpn = mpn_match.group(1).strip() if mpn_match else None
    gtin = gtin_match.group(1).strip() if gtin_match else None

    return (mpn, gtin)


# -------------------------
# 7) ბარათიდან პროდუქტის ამოღება
# -------------------------
def parse_product_card(card: BeautifulSoup) -> Optional[Product]:
    # LINK + TITLE
    title_a = card.select_one("h2 a") or card.select_one(".product-img a")
    if not title_a or not title_a.get("href"):
        return None

    link = urljoin(BASE_URL, title_a["href"].strip())

    title = title_a.get_text(" ", strip=True)
    if not title:
        img_fallback = card.select_one("img.default-img") or card.select_one("img")
        title = (img_fallback.get("alt") or "").strip() if img_fallback else ""

    # BRAND
    brand = ""
    brand_a = card.select_one('a[href*="products?brand="]') or card.select_one("span.text-muted a")
    if brand_a:
        brand = brand_a.get_text(" ", strip=True)

    # CATEGORY / PRODUCT_TYPE
    category = DEFAULT_PRODUCT_TYPE

    # IMAGE
    img = card.select_one("img.default-img") or card.select_one(".product-img img") or card.select_one("img")
    image_link = ""
    if img and img.get("src"):
        image_link = urljoin(BASE_URL, img["src"].strip())

    # PRICE / SALE_PRICE
    price, sale_price = extract_prices_from_card(card)
    if price.startswith("0.00"):
        return None

    # ID
    pid = link.rstrip("/").split("/")[-1]

    return Product(
        pid=pid,
        title=title,
        link=link,
        image_link=image_link,
        brand=brand,
        category=category,
        price=price,
        sale_price=sale_price,
    )


# -------------------------
# 8) გვერდების გავლა (pagination)
# -------------------------
def collect_products() -> list[Product]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (compatible; TopsportFeedBot/1.0)",
            "Accept-Language": "ka,en;q=0.8,ru;q=0.7",
        }
    )

    products: list[Product] = []
    seen_links: set[str] = set()

    page = 1
    while True:
        if MAX_PAGES is not None and page > MAX_PAGES:
            break

        url = f"{CATEGORY_URL}?page={page}"
        soup = fetch_soup(session, url)

        cards = soup.select("div.product-cart-wrap")
        if not cards:
            break

        added_this_page = 0
        for card in cards:
            p = parse_product_card(card)
            if not p:
                continue
            if p.link in seen_links:
                continue

            # მძიმე ნაწილი: თითო პროდუქტზე პროდუქტის გვერდზე შესვლა
            if FETCH_MPN:
                mpn, gtin = fetch_identifiers_from_product_page(session, p.link)
                p.mpn = mpn
                p.gtin = gtin
                time.sleep(SLEEP_SECONDS)

            seen_links.add(p.link)
            products.append(p)
            added_this_page += 1

            if MAX_PRODUCTS is not None and len(products) >= MAX_PRODUCTS:
                return products

        if added_this_page == 0:
            break

        page += 1
        time.sleep(SLEEP_SECONDS)

    return products


# -------------------------
# 9) XML (RSS + g:) გენერაცია
# -------------------------
def build_rss_feed(products: list[Product]) -> ET.ElementTree:
    # Google Merchant namespace (Meta ხშირად ამავე სტრუქტურას “ჭამს”)
    G_NS = "http://base.google.com/ns/1.0"
    ET.register_namespace("g", G_NS)

    def g(tag: str) -> str:
        return f"{{{G_NS}}}{tag}"

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "TOPSPORT.GE - ქალის ფეხსაცმელი (Catalog Feed)"
    ET.SubElement(channel, "link").text = CATEGORY_URL
    ET.SubElement(channel, "description").text = "Products feed generated from topsport.ge category pages."

    for p in products:
        item = ET.SubElement(channel, "item")

        # RSS compatibility
        ET.SubElement(item, "title").text = p.title
        ET.SubElement(item, "link").text = p.link
        ET.SubElement(item, "description").text = (p.category or p.title)

        # g: fields
        ET.SubElement(item, g("id")).text = p.pid
        ET.SubElement(item, g("title")).text = p.title
        ET.SubElement(item, g("link")).text = p.link
        ET.SubElement(item, g("condition")).text = "new"
        ET.SubElement(item, g("availability")).text = "in stock"

        ET.SubElement(item, g("google_product_category")).text = GOOGLE_PRODUCT_CATEGORY

        if p.category:
            ET.SubElement(item, g("product_type")).text = p.category

        if p.brand:
            ET.SubElement(item, g("brand")).text = p.brand

        if p.image_link:
            ET.SubElement(item, g("image_link")).text = p.image_link

        # pricing
        ET.SubElement(item, g("price")).text = p.price
        if p.sale_price:
            ET.SubElement(item, g("sale_price")).text = p.sale_price

        # identifiers
        if p.mpn:
            ET.SubElement(item, g("mpn")).text = p.mpn
        if p.gtin:
            ET.SubElement(item, g("gtin")).text = p.gtin

    return ET.ElementTree(rss)


def save_xml(tree: ET.ElementTree, path: str) -> None:
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    print("ვიწყებ პროდუქტის შეგროვებას...")
    products = collect_products()
    print(f"ნაპოვნია: {len(products)} პროდუქტი")

    print("ვაგენერირებ XML ფიდს...")
    tree = build_rss_feed(products)
    save_xml(tree, OUTPUT_XML)

    print(f"მზადაა: {OUTPUT_XML}")


if __name__ == "__main__":
    main()
