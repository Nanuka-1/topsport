import json
import os
import re
import time
from datetime import datetime, timezone
from urllib.parse import urljoin
from xml.sax.saxutils import escape

import requests
from bs4 import BeautifulSoup


# =========================
# კონფიგურაცია
# =========================

CATALOG_URL = "https://topsport.ge/en/products/qalis-fekhsatsmeli"
BASE = "https://topsport.ge"

MAX_PRODUCTS = 20
SLEEP_SEC = 0.8

GOOGLE_PRODUCT_CATEGORY = "Apparel & Accessories > Shoes"

# მხოლოდ ის პროდუქტები მოხვდება, ვის URL-შიც ეს სტრინგი იქნება
PRODUCT_SLUG_FILTER = "qalis-sportuli-fekhsatsmeli"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,ka;q=0.8,ru;q=0.7",
}


# =========================
# ტექსტების/ფასის გასუფთავება
# =========================

# ფასი მხოლოდ GEL/₾ კონტექსტში რომ ვიპოვოთ (ფოლბექისთვის)
PRICE_CONTEXT_PATTERNS = [
    re.compile(r"\bGEL\b\s*([0-9]+(?:[.,][0-9]{1,2})?)", re.I),
    re.compile(r"([0-9]+(?:[.,][0-9]{1,2})?)\s*\bGEL\b", re.I),
    re.compile(r"₾\s*([0-9]+(?:[.,][0-9]{1,2})?)"),
    re.compile(r"([0-9]+(?:[.,][0-9]{1,2})?)\s*₾"),
]


def clean_text(s: str) -> str:
    # ტექსტში ზედმეტი სფეისების მოცილება
    s = (s or "").strip()
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def format_price_gel_from_number(num: str) -> str:
    # რიცხვიდან "123.00 GEL" ფორმატი
    num = (num or "").replace(",", ".")
    num = re.sub(r"[^\d.]", "", num)
    if not num:
        return ""
    try:
        value = float(num)
    except ValueError:
        return ""
    return f"{value:.2f} GEL"


def format_price_gel(raw: str) -> str:
    # ფასის სტანდარტიზაცია: ყოველთვის "123.00 GEL"
    raw = clean_text(raw)
    if not raw:
        return ""
    m = re.search(r"([0-9]+(?:[.,][0-9]{1,2})?)", raw)
    if not m:
        return ""
    return format_price_gel_from_number(m.group(1))


def find_price_in_text_with_currency(text: str) -> str:
    # ფოლბექი: ვეძებთ ფასს მხოლოდ GEL/₾-თან ერთად (ზომებს/sku-ს რომ არ “დაჭამოს”)
    if not text:
        return ""
    text = text.replace("\u00a0", " ")
    for pat in PRICE_CONTEXT_PATTERNS:
        m = pat.search(text)
        if m:
            return format_price_gel_from_number(m.group(1))
    return ""


def normalize_brand(brand: str) -> str:
    # ბრენდის სახელის გასუფთავება + მსუბუქი კაპიტალიზაცია
    b = clean_text(brand)
    if not b:
        return ""
    if b.islower():
        b = b.title()
    return b


def extract_brand_from_title(title: str) -> str:
    # fallback: ბრენდი = სათაურის პირველი სიტყვა
    t = clean_text(title)
    if not t:
        return ""
    w = t.split()
    if len(w) >= 2 and w[0].lower() == "under" and w[1].lower() == "armour":
        return "Under Armour"
    return w[0] if w else ""


# =========================
# HTTP სესია + ფეჩი (retries)
# =========================

def make_session() -> requests.Session:
    # სესია უფრო სტაბილურია (keep-alive)
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def fetch(session: requests.Session, url: str) -> str:
    # 3 ცდა დროებითი შეცდომებისთვის
    last_err = None
    for attempt in range(1, 4):
        try:
            r = session.get(url, timeout=25)
            r.raise_for_status()
            return r.text
        except Exception as e:
            last_err = e
            time.sleep(0.8 * attempt)
    raise last_err


# =========================
# კატალოგიდან პროდუქტის ლინკები
# =========================

def extract_product_links(listing_html: str) -> list[str]:
    soup = BeautifulSoup(listing_html, "lxml")

    links: list[str] = []
    for a in soup.select('a[href*="/en/product/"], a[href*="/product/"]'):
        href = (a.get("href") or "").strip()
        if not href:
            continue

        full = urljoin(BASE, href)

        # მხოლოდ topsport-ის დომენი
        if not full.startswith(BASE):
            continue

        # მხოლოდ სასურველი სლაგის მქონე პროდუქტები
        if PRODUCT_SLUG_FILTER and PRODUCT_SLUG_FILTER not in full:
            continue

        links.append(full)

    # უნიკალიზაცია (რიგის შენარჩუნებით)
    uniq: list[str] = []
    seen = set()
    for u in links:
        if u not in seen:
            uniq.append(u)
            seen.add(u)

    return uniq


# =========================
# სურათის URL-ის გასუფთავება
# =========================

def clean_image_url(image: str) -> str:
    # ზოგჯერ დუბლირებული ფორმა აქვს: .../uploads/https://... -> https://...
    if not image:
        return ""
    if "uploads/https://" in image:
        image = "https://" + image.split("uploads/https://", 1)[1]
    return image.strip()


# =========================
# JSON-LD (schema.org) პროდუქტის ამოღება
# =========================

def parse_jsonld_product(soup: BeautifulSoup) -> dict:
    # ვეძებთ <script type="application/ld+json">
    for tag in soup.select('script[type="application/ld+json"]'):
        raw = (tag.string or tag.get_text() or "").strip()
        if not raw:
            continue

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue

        candidates = data if isinstance(data, list) else [data]

        for obj in candidates:
            if not isinstance(obj, dict):
                continue

            # ხანდახან Product @graph-შია ჩაშენებული
            if "@graph" in obj and isinstance(obj["@graph"], list):
                for x in obj["@graph"]:
                    if isinstance(x, dict) and x.get("@type") == "Product":
                        return x
                continue

            if obj.get("@type") == "Product":
                return obj

    return {}


def map_availability(schema_url: str) -> str:
    # schema.org მნიშვნელობას ვაქცევთ Google-ის ფორმატად
    v = (schema_url or "").lower()
    if "instock" in v:
        return "in_stock"
    if "outofstock" in v:
        return "out_of_stock"
    if "preorder" in v:
        return "preorder"
    if "backorder" in v:
        return "backorder"
    return ""


# =========================
# ფასი + sale_price DOM-დან
# =========================

def extract_price_and_sale_from_dom(soup: BeautifulSoup) -> tuple[str, str]:
    # ლოგიკა:
    # - თუ არის ძველი (გადახაზული) და ახალი -> price=ძველი, sale_price=ახალი
    # - თუ არის მხოლოდ ერთი -> price=ერთი, sale_price=""

    current_el = soup.select_one("div.product-price span.current-price") or soup.select_one("span.current-price")
    current = format_price_gel(current_el.get_text(" ", strip=True) if current_el else "")

    old_el = (
        soup.select_one("div.product-price span.old-price")
        or soup.select_one("div.product-price del")
        or soup.select_one("div.product-price s")
        or soup.select_one("span.old-price")
        or soup.select_one("del")
        or soup.select_one("s")
    )
    old = format_price_gel(old_el.get_text(" ", strip=True) if old_el else "")

    # თუ ორივე გვაქვს და current < old -> sale რეჟიმი
    if old and current:
        try:
            old_num = float(old.split()[0])
            cur_num = float(current.split()[0])
            if cur_num < old_num:
                return old, current
        except Exception:
            pass

    return current, ""


# =========================
# availability DOM-დან (უფრო სანდო)
# =========================

def extract_availability_from_dom(soup: BeautifulSoup) -> str:
    # მიზანი: არ მივიღოთ ცრუ out_of_stock/in_stock
    # ვამოწმებთ მხოლოდ “ყიდვის” ზონას და ღილაკის მდგომარეობას

    buy_scope = soup.select_one("div.product-price") or soup

    btn = soup.select_one(
        "button.add-to-cart, button[name='add'], button[name='add_to_cart'], form[action*='cart'] button[type='submit']"
    )

    if btn:
        btn_text = btn.get_text(" ", strip=True).lower()
        disabled = btn.has_attr("disabled") or ("disabled" in (btn.get("class") or []))

        # მკაფიო უარყოფითი სიგნალები
        if "out of stock" in btn_text or "sold out" in btn_text or "unavailable" in btn_text:
            return "out_of_stock"

        # თუ ღილაკი disabled-ია, მაგრამ უარყოფითი ტექსტი არაა — არ ვამბობთ out_of_stock
        # (ხშირად ზომის არჩევას ითხოვს)
        if disabled:
            return ""

        return "in_stock"

    scope_text = buy_scope.get_text(" ", strip=True).lower()
    if "out of stock" in scope_text or "sold out" in scope_text:
        return "out_of_stock"

    return ""


# =========================
# პროდუქტის პარსინგი
# =========================

def parse_product(session: requests.Session, url: str) -> dict:
    html = fetch(session, url)
    soup = BeautifulSoup(html, "lxml")

    ld = parse_jsonld_product(soup)

    # სათაური (JSON-LD -> H1 -> <title>)
    title = clean_text(str(ld.get("name") or ""))
    if not title:
        h1 = soup.find("h1")
        if h1:
            title = clean_text(h1.get_text(strip=True))
        elif soup.title:
            title = clean_text(soup.title.get_text(strip=True))
        else:
            title = "Unknown"

    # აღწერა (JSON-LD -> meta description -> fallback title)
    description = clean_text(str(ld.get("description") or ""))
    if not description:
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = clean_text(meta_desc.get("content", "") if meta_desc else "")
    if not description:
        description = title

    # სურათი (JSON-LD image -> og:image)
    image = ""
    if ld.get("image"):
        img = ld.get("image")
        if isinstance(img, list):
            image = str(img[0]).strip() if img else ""
        else:
            image = str(img).strip()
    if not image:
        og_img = soup.find("meta", property="og:image")
        image = (og_img.get("content", "") if og_img else "").strip()
    image = clean_image_url(image)

    # ბრენდი (JSON-LD -> fallback title)
    brand = ""
    b = ld.get("brand")
    if isinstance(b, dict) and b.get("name"):
        brand = str(b["name"])
    if not brand:
        brand = extract_brand_from_title(title)
    brand = normalize_brand(brand)

    # availability (JSON-LD -> DOM -> fallback)
    availability = ""
    offers = ld.get("offers") if isinstance(ld.get("offers"), dict) else {}
    availability = map_availability(offers.get("availability", ""))

    # ფასი + sale_price (DOM)
    price, sale_price = extract_price_and_sale_from_dom(soup)

    # fallback: თუ DOM-ით ვერ ვიპოვეთ (მხოლოდ GEL/₾ კონტექსტში)
    if not price:
        text = soup.get_text(" ", strip=True)
        price = find_price_in_text_with_currency(text)
        sale_price = ""

    # sale_price ვწერთ მხოლოდ მაშინ, როცა რეალურად ნაკლებია
    if sale_price:
        try:
            p = float(price.split()[0])
            sp = float(sale_price.split()[0])
            if sp >= p:
                sale_price = ""
        except Exception:
            sale_price = ""

    # DOM availability-ს პრიორიტეტი (თუ მკაფიოდ დადგინდა)
    availability_dom = extract_availability_from_dom(soup)
    if availability_dom:
        availability = availability_dom

    # საბოლოო fallback
    if not availability:
        availability = "in_stock" if price else "out_of_stock"

    pid = url.rstrip("/").split("/")[-1]

    return {
        "id": pid,
        "title": title,
        "description": description,
        "link": url,
        "image_link": image,
        "availability": availability,
        "condition": "new",
        "price": price,
        "sale_price": sale_price,
        "brand": brand,
        "google_product_category": GOOGLE_PRODUCT_CATEGORY,
    }


# =========================
# Google RSS (Merchant Center)
# =========================

def build_google_rss(items: list[dict]) -> str:
    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">')
    parts.append("<channel>")
    parts.append("<title><![CDATA[TopSport Test Feed]]></title>")
    parts.append(f"<link>{escape(CATALOG_URL)}</link>")
    parts.append("<description><![CDATA[Test product feed generated by parsing public pages]]></description>")
    parts.append("<language>en</language>")

    # pubDate RSS-სთვის (UTC)
    pub_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    parts.append(f"<pubDate>{pub_date}</pubDate>")

    for it in items:
        # მინიმალური აუცილებელი ველები
        if not it.get("id") or not it.get("title") or not it.get("link"):
            continue

        # ფასის გარეშე Merchant ხშირად reject-ს აკეთებს
        if not it.get("price"):
            continue

        parts.append("<item>")
        parts.append(f"<g:id>{escape(it['id'])}</g:id>")
        parts.append(f"<g:title><![CDATA[{it['title']}]]></g:title>")
        parts.append(f"<g:description><![CDATA[{it['description']}]]></g:description>")
        parts.append(f"<g:link>{escape(it['link'])}</g:link>")

        if it.get("image_link"):
            parts.append(f"<g:image_link>{escape(it['image_link'])}</g:image_link>")

        parts.append(f"<g:availability>{escape(it['availability'])}</g:availability>")
        parts.append(f"<g:condition>{escape(it['condition'])}</g:condition>")
        parts.append(f"<g:price>{escape(it['price'])}</g:price>")

        # sale_price მხოლოდ თუ გვაქვს რეალური ფასდაკლება
        if it.get("sale_price"):
            parts.append(f"<g:sale_price>{escape(it['sale_price'])}</g:sale_price>")

        if it.get("brand"):
            parts.append(f"<g:brand><![CDATA[{it['brand']}]]></g:brand>")

        if it.get("google_product_category"):
            cat = it["google_product_category"].replace(">", "&gt;")
            parts.append(f"<g:google_product_category><![CDATA[{cat}]]></g:google_product_category>")

        parts.append("</item>")

    parts.append("</channel>")
    parts.append("</rss>")
    return "\n".join(parts)


# =========================
# main
# =========================

def main():
    session = make_session()

    listing_html = fetch(session, CATALOG_URL)
    product_links = extract_product_links(listing_html)

    if not product_links:
        print("❌ პროდუქტების ლინკები ვერ მოიძებნა. გადაამოწმე CATALOG_URL/PRODUCT_SLUG_FILTER.")
        return

    product_links = product_links[:MAX_PRODUCTS]

    items: list[dict] = []
    for i, url in enumerate(product_links, 1):
        print(f"[{i}/{len(product_links)}] {url}")
        try:
            items.append(parse_product(session, url))
        except Exception as e:
            print("  ERROR:", e)
        time.sleep(SLEEP_SEC)

    xml = build_google_rss(items)

    # GitHub Pages-ისთვის საუკეთესოა public/feed.xml
    os.makedirs("public", exist_ok=True)
    out_file = "public/feed.xml"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"\nDONE ✅ Saved: {out_file}")
    print(f"Items (raw parsed): {len(items)}")


if __name__ == "__main__":
    main()
