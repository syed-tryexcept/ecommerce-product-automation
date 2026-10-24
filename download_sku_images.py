import os
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
from lxml import html

# ==========================================
# CONFIGURATION
# ==========================================
EXCEL_FILE = "Product_Remake.xlsx"  # Apnar Excel file name
OUTPUT_FOLDER = "Downloaded_Products"  # Main Folder path
MAX_WORKERS = 8  # Parallel downloading thread count (speed baranor jonno)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}


def sanitize_folder_name(name):
    """Folder name theke invalid characters remove kore."""
    clean_name = re.sub(r'[\\/*?:"<>|]', "", str(name))
    return clean_name.strip()


def download_single_image(img_url, save_path):
    """Single image download helper."""
    try:
        resp = requests.get(img_url, headers=HEADERS, timeout=15)
        if resp.status_code == 200 and len(resp.content) > 2000:  # Skip tiny icons
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True
    except Exception as e:
        pass
    return False


def process_product(row_tuple):
    index, row = row_tuple
    product_name = str(row["Product Name"]).strip()
    product_url = str(row["KickBazar"]).strip()

    if (
        not product_url
        or pd.isna(product_url)
        or not product_url.startswith("http")
    ):
        print(f"[{index+1}/276] Skipping: Invalid URL for '{product_name}'")
        return

    # Folder setup
    folder_name = sanitize_folder_name(product_name)
    sku_folder = os.path.join(OUTPUT_FOLDER, folder_name)
    os.makedirs(sku_folder, exist_ok=True)

    print(f"[{index+1}/276] Processing SKU: {product_name}")

    try:
        resp = requests.get(product_url, headers=HEADERS, timeout=20)
        if resp.status_code != 200:
            print(f"   ❌ Failed to access URL (Status {resp.status_code})")
            return

        tree = html.fromstring(resp.content)

        # 1. Main Product Images Extraction (Gallery / Slider / Product Box)
        # Standard ecommerce selectors for main product image
        main_img_urls = tree.xpath(
            '//div[contains(@class, "product")]//img/@src | '
            '//div[contains(@class, "gallery")]//img/@src | '
            '//div[contains(@class, "slider")]//img/@src | '
            '//img[contains(@class, "main")]/@src'
        )

        # Fallback if no specific gallery found: get first 2 prominent images
        all_imgs = tree.xpath("//img/@src | //img/@data-src")

        # Clean URLs
        cleaned_all_urls = []
        for url in all_imgs:
            full_url = urllib.parse.urljoin(product_url, url)
            if (
                any(ext in full_url.lower() for ext in [".jpg", ".png", ".webp", ".jpeg"])
                and "logo" not in full_url.lower()
                and "icon" not in full_url.lower()
            ):
                if full_url not in cleaned_all_urls:
                    cleaned_all_urls.append(full_url)

        # Separate Main vs Description Images
        # First 1-2 images as Main Images
        main_target = cleaned_all_urls[:2]
        # Next 3-5 images as Description Images
        desc_target = cleaned_all_urls[2:7]

        # Download Main Images (1-2)
        main_count = 1
        for img_url in main_target:
            ext = img_url.split(".")[-1].split("?")[0]
            if len(ext) > 4:
                ext = "jpg"
            file_name = f"Main_Image_{main_count}.{ext}"
            save_path = os.path.join(sku_folder, file_name)

            if download_single_image(img_url, save_path):
                main_count += 1

        # Download Description Images (3-4)
        desc_count = 1
        for img_url in desc_target:
            ext = img_url.split(".")[-1].split("?")[0]
            if len(ext) > 4:
                ext = "jpg"
            file_name = f"Desc_Image_{desc_count}.{ext}"
            save_path = os.path.join(sku_folder, file_name)

            if download_single_image(img_url, save_path):
                desc_count += 1

        print(
            f"   ✅ Saved {main_count-1} Main Images, {desc_count-1} Description Images -> Folder: '{folder_name}'"
        )

    except Exception as e:
        print(f"   ❌ Error processing {product_name}: {e}")


def main():
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: '{EXCEL_FILE}' path-e Excel file-ti paowa jayni!")
        return

    print("Excel File reading...")
    df = pd.read_excel(EXCEL_FILE)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(
        f"Total {len(df)} SKU processing shuru hocche. Output folder: '{OUTPUT_FOLDER}'\n"
    )

    # Multi-threading to speed up downloading
    rows = list(df.iterrows())
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(process_product, rows)

    print(
        "\n🎉 Shob 276-ti SKU er image download complete! Check 'Downloaded_Products' folder."
    )


if __name__ == "__main__":
    main()