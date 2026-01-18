import re
import xml.etree.ElementTree as ET

FEED_FILE = "topsport_google_feed.xml"
NS = {"g": "http://base.google.com/ns/1.0"}

SLUG = "qalis-sportuli-fekhsatsmeli"
PRICE_OK = re.compile(r"^\d+(\.\d+)?\s+GEL$")  # მაგალითად: 399.00 GEL

tree = ET.parse(FEED_FILE)
root = tree.getroot()

items = root.findall("./channel/item")

missing_price = 0
bad_price = 0
missing_brand = 0
not_shoes = 0
missing_title = 0
missing_desc = 0

for it in items:
    link = it.findtext("g:link", default="", namespaces=NS)
    title = it.findtext("g:title", default="", namespaces=NS).strip()
    desc = it.findtext("g:description", default="", namespaces=NS).strip()
    brand = it.findtext("g:brand", default="", namespaces=NS).strip()
    price = it.findtext("g:price", default="", namespaces=NS).strip()

    if SLUG not in link:
        not_shoes += 1

    if not title:
        missing_title += 1

    if not desc:
        missing_desc += 1

    if not brand:
        missing_brand += 1

    if not price:
        missing_price += 1
    elif not PRICE_OK.match(price):
        bad_price += 1

print("=== FEED CHECK ===")
print(f"Total items: {len(items)}")
print(f"Not women's shoes (slug missing): {not_shoes}")
print(f"Missing title: {missing_title}")
print(f"Missing description: {missing_desc}")
print(f"Missing brand: {missing_brand}")
print(f"Missing price: {missing_price}")
print(f"Bad price format: {bad_price}")

print("\nSample bad prices (up to 5):")
count = 0
for it in items:
    price = it.findtext("g:price", default="", namespaces=NS).strip()
    if price and not PRICE_OK.match(price):
        pid = it.findtext("g:id", default="", namespaces=NS)
        link = it.findtext("g:link", default="", namespaces=NS)
        print("-", pid, "|", price, "|", link)
        count += 1
        if count >= 5:
            break
