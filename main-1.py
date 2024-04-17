import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Inisialisasi driver dengan webdriver_manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Buka URL
driver.get("https://bachacoffee.com/en/coffee-beans")

# Mendapatkan sumber HTML dari halaman
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

result = []

# Definisikan fungsi untuk mendapatkan URL gambar
def parse_image_urls(classes, location, source):
    for a in soup.find_all(attrs={"class": classes}):
        name = a.find(location)
        if name:
            image_url = name.get(source)
            if image_url not in result:
                result.append(image_url)

# Panggil fungsi dengan parameter yang benar
parse_image_urls("product-listing__coffee--img", "img", "src")

# Simpan URL ke CSV
df = pd.DataFrame({"links": result})
df.to_csv("links.csv", index=False, encoding="utf-8")

# Unduh gambar dari URL
for image_url in result:
    response = requests.get(image_url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        # Simpan gambar ke disk
        image_file_name = os.path.basename(image_url)
        with open(image_file_name, "wb") as file:
            file.write(response.content)
        print(f"Berhasil mengunduh {image_file_name}")
    else:
        print(f"Gagal mengunduh {image_url}")

# Tutup driver
driver.quit()

# Misal, result adalah daftar URL gambar yang Anda dapatkan
result = ["https://bachacoffee.com/en/coffee-beans"]

for image_url in result:
    try:
        response = requests.get(image_url, timeout=10)  # Menambahkan timeout untuk menghindari menunggu terlalu lama

        if response.status_code == 200:
            # Simpan gambar ke disk
            image_file_name = os.path.basename(image_url)
            with open(image_file_name, "wb") as file:
                file.write(response.content)
            print(f"Berhasil mengunduh {image_file_name}")
        else:
            # Cetak status code dan URL jika gagal karena status code
            print(f"Gagal mengunduh {image_url}, Status Code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Menangkap semua jenis kesalahan yang mungkin terjadi selama permintaan
        print(f"Gagal mengunduh {image_url}, Error: {str(e)}")
        