import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configuration
EXCEL_FILE = "Product_Remake.xlsx"
OUTPUT_FOLDER = "Downloaded_Products"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def sanitize_folder_name(name):
  return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()


def main():
  if not os.path.exists(EXCEL_FILE):
    print(f"Error: '{EXCEL_FILE}' file-ti paowa jayni!")
    return

  df = pd.read_excel(EXCEL_FILE)
  os.makedirs(OUTPUT_FOLDER, exist_ok=True)

  print(f"Total {len(df)} ta SKU er description download shuru hocche...\n")

  for index, row in df.iterrows():
    product_name = str(row["Product Name"]).strip()
    product_url = str(row["KickBazar"]).strip()

    if (
        not product_url
        or pd.isna(product_url)
        or not product_url.startswith("http")
    ):
      continue

    folder_name = sanitize_folder_name(product_name)
    sku_folder = os.path.join(OUTPUT_FOLDER, folder_name)
    os.makedirs(sku_folder, exist_ok=True)

    print(
        f"[{index+1}/{len(df)}] Fetching description for: {product_name}..."
    )

    try:
      resp = requests.get(product_url, headers=HEADERS, timeout=15)
      if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

        # Description container ba text khuje ber kora
        desc_div = soup.find(
            "div", class_=re.compile("description|details|content|product")
        )
        if desc_div:
          desc_text = desc_div.get_text(separator="\n", strip=True)
        else:
          desc_text = soup.get_text(separator="\n", strip=True)

        # description.txt file hishebe save kora
        txt_path = os.path.join(sku_folder, "description.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
          f.write(f"Product: {product_name}\nURL: {product_url}\n\n" + desc_text)

        print(f"   ✅ Saved description.txt")
      else:
        print(f"   ❌ Failed to load page (Status: {resp.status_code})")

    except Exception as e:
      print(f"   ❌ Error: {e}")

  print("\n🎉 Shob SKU er description.txt file save kora complete!")


if __name__ == "__main__":
  main()