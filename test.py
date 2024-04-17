# Tunggu hingga elemen gambar muncul
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-listing__coffee--img img"))
)

# Temukan semua elemen gambar
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.product-listing__coffee--img img")

# Coba dapatkan 'data-src' jika 'src' bukan URL yang benar
image_urls = []
for image in image_elements:
    # Cek jika 'data-src' ada atau tidak
    image_url = image.get_attribute('data-src') or image.get_attribute('src')
    if image_url.endswith('.svg'):
        # Jika URL berakhir dengan .svg, kita abaikan karena itu adalah placeholder
        continue
    image_urls.append(image_url)