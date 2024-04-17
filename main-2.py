import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Pengaturan Selenium WebDriver
options = webdriver.ChromeOptions()
options.headless = True  # Jalankan browser dalam mode headless
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL target
url = "https://bachacoffee.com/en/coffee-beans"

# Folder untuk menyimpan gambar yang diunduh
image_folder = "gambar_terunduh"
os.makedirs(image_folder, exist_ok=True)

try:
    # Navigasi ke situs web
    driver.get(url)
    
    # Tunggu hingga elemen gambar muncul
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-listing__coffee--img img"))
    )

    # Temukan semua elemen gambar
    image_elements = driver.find_elements(By.CSS_SELECTOR, "div.product-listing__coffee--img img")

    # Fungsi untuk membersihkan nama file
    def sanitize_filename(url):
        # Mengambil bagian dari URL sebelum tanda tanya
        clean_url = url.split('?')[0]
        # Mendapatkan nama file tanpa ekstensi
        file_name = os.path.basename(clean_url)
        # Mengganti karakter yang tidak valid
        return re.sub(r'[\\/*?:"<>|]', '', file_name)

    # Dapatkan URL gambar dari setiap elemen gambar
    image_urls = []
    for image in image_elements:
        # Mencoba mendapatkan 'data-src' atau 'src'
        image_url = image.get_attribute('data-src') or image.get_attribute('src')
        if not image_url.endswith('.svg'):  # Abaikan jika URL adalah file SVG
            image_urls.append(image_url)

    # Unduh setiap gambar menggunakan requests
    for i, image_url in enumerate(image_urls):
        response = requests.get(image_url)
        if response.status_code == 200:
            # Bersihkan nama file
            image_file_name = sanitize_filename(image_url)
            # Menambahkan indeks dan ekstensi file yang benar
            image_file_path = os.path.join(image_folder, f'gambar_{i}{os.path.splitext(image_file_name)[1]}')
            with open(image_file_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Error {response.status_code} - Tidak dapat mengunduh {image_url}")

finally:
    # Tutup browser
    driver.quit()

print(f"Berhasil mengunduh {len(image_urls)} gambar ke folder {image_folder}")
