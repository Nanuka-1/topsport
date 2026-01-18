import re
import sys
import xml.etree.ElementTree as ET

G_NS = "http://base.google.com/ns/1.0"
NS = {"g": G_NS}

PRICE_RE = re.compile(r"^\d+(\.\d{2})\s+[A-Z]{3}$")


def get_text(item: ET.Element, path: str) -> str:
    el = item.find(path, NS) if path.startswith("g:") else item.find(path)
    return (el.text or "").strip() if el is not None and el.text else ""


def main():
    feed_file = sys.argv[1] if len(sys.argv) > 1 else "topsport_qalis_fekhsatsmeli.xml"

    tree = ET.parse(feed_file)
    root = tree.getroot()

    items = root.findall("./channel/item")
    print(f"ITEMS: {len(items)}")

    missing_brand = 0
    missing_product_type = 0
    missing_title = 0
    missing_link = 0
    missing_price = 0
    with_sale_price = 0
    missing_image_link = 0
    missing_google_cat = 0
    with_mpn = 0
    bad_price_format = 0

    for it in items:
        title = get_text(it, "g:title") or get_text(it, "title")
        link = get_text(it, "g:link") or get_text(it, "link")
        brand = get_text(it, "g:brand")
        ptype = get_text(it, "g:product_type")
        price = get_text(it, "g:price")
        sale = get_text(it, "g:sale_price")
        img = get_text(it, "g:image_link")
        gcat = get_text(it, "g:google_product_category")
        mpn = get_text(it, "g:mpn")

        if not title:
            missing_title += 1
        if not link:
            missing_link += 1
        if not brand:
            missing_brand += 1
        if not ptype:
            missing_product_type += 1
        if not price:
            missing_price += 1
        if sale:
            with_sale_price += 1
        if not img:
            missing_image_link += 1
        if not gcat:
            missing_google_cat += 1
        if mpn:
            with_mpn += 1
        if price and not PRICE_RE.match(price):
            bad_price_format += 1

    print(f"WITH PRICE: {len(items) - missing_price}")
    print(f"WITH SALE_PRICE: {with_sale_price}")
    print(f"MISSING BRAND: {missing_brand}")
    print(f"MISSING PRODUCT_TYPE: {missing_product_type}")
    print(f"MISSING TITLE: {missing_title}")
    print(f"MISSING LINK: {missing_link}")
    print(f"MISSING IMAGE_LINK: {missing_image_link}")
    print(f"MISSING GOOGLE CATEGORY: {missing_google_cat}")
    print(f"WITH MPN: {with_mpn}")
    print(f"BAD PRICE FORMAT: {bad_price_format}")

    if items:
        first = items[0]
        print("\n--- FIRST ITEM TAGS ---")
        for ch in list(first):
            print(f"TAG: {ch.tag} | TEXT: {(ch.text or '').strip()}")

        print("\n--- TRY READ ---")
        print("g:title:", get_text(first, "g:title"))
        print("title:", get_text(first, "title"))
        print("g:link:", get_text(first, "g:link"))
        print("link:", get_text(first, "link"))
        print("g:image_link:", get_text(first, "g:image_link"))
        print("g:price:", get_text(first, "g:price"))
        print("g:mpn:", get_text(first, "g:mpn"))
        print("g:google_product_category:", get_text(first, "g:google_product_category"))


if __name__ == "__main__":
    main()
