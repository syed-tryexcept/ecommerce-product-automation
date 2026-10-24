import os
import re
import pandas as pd
import urllib.parse

# Configuration
EXCEL_FILE = 'Product_Remake.xlsx'
# Apnar main Google Drive folder er ID jei link theke paowa geche
MASTER_DRIVE_FOLDER_URL = "https://drive.خصائص.../folders/19GgzGAiUHZteF4HcIkDTELcKbbFfCM4j"
# Ba general base folder link
BASE_DRIVE_LINK = "https://drive.google.com/drive/folders/19GgzGAiUHZteF4HcIkDTELcKbbFfCM4j"

def sanitize_folder_name(name):
    return re.sub(r'[\\/*?:"<>|]', "", str(name)).strip()

def main():
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: '{EXCEL_FILE}' file-ti paowa jayni!")
        return

    df = pd.read_excel(EXCEL_FILE)
    
    # Notun column toiri kora SKU link er jonno
    drive_links = []

    print("Generating Drive links mapping for SKUs...")

    for index, row in df.iterrows():
        product_name = str(row['Product Name']).strip()
        if not product_name or pd.isna(row['Product Name']):
            drive_links.append("")
            continue
        
        # Folder name encode kora URL er jonno
        encoded_name = urllib.parse.quote(product_name)
        
        # Note: Google Drive direct subfolder search API chara subfolder er direct unique ID 
        # local computer folder name theke exact match kore create korar jonno amra base folder link 
        # ba search query link use korte pari, or search query link banate pari.
        # Ekhane search query link ba direct main folder link-sathe map kora hochhe:
        search_link = f"https://drive.google.com/drive/u/0/search?q={encoded_name}"
        drive_links.append(search_link)

    # Excel file-e notun column add kora
    df['Drive Link'] = drive_links

    # Notun ekta Excel file save kora jate ager file nosto na hoy
    output_excel = "Product_Remake_With_Links.xlsx"
    df.to_excel(output_excel, index=False)
    
    print(f"\n🎉 Success! Updated Excel file saved as '{output_excel}'. Check the new 'Drive Link' column.")

if __name__ == '__main__':
    main()