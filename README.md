# 🚀 E-Commerce SKU Data Automation & Pipeline

An automated Python-based solution designed to streamline product data organization for 276+ SKUs. This tool automates web scraping, local asset management, and cloud directory mapping to save manual data-entry hours.

## 🛠️ Tech Stack & Libraries
* **Python** (Core logic & scripting)
* **Pandas & OpenPyXL** (Excel data processing & manipulation)
* **Requests & BeautifulSoup4 (bs4)** (Web scraping & HTML parsing)
* **LXML** (Fast XML/HTML processing)

## ✨ Key Features
1. **Automated Image Downloader:** Scrapes and downloads high-res Main and Description images into dedicated SKU-specific local folders.
2. **Content Extraction:** Automatically extracts clean product descriptions and saves them as structured `.txt` files per SKU.
3. **Cloud Mapping:** Generates automated Google Drive mapping links to seamlessly link local folders with cloud master directories.
4. **Batch Optimization:** Designed for efficient multi-item processing without pipeline bottlenecks.

## 📂 Project Structure
```text
📦 ecommerce-product-automation/
├── 📜 download_sku_images.py       # Script for batch downloading product images
├── 📜 download_descriptions.py     # Script for extracting product descriptions
├── 📜 generate_drive_links.py      # Script for mapping Google Drive links to Excel
├── 📋 requirements.txt             # Project dependencies list
└── 📄 README.md                    # Project documentation
