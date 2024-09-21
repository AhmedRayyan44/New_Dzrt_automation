import json
import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# Global list to store product names that are successfully sent
sent_products = []
# Dictionary to store the time each product was last sent
product_send_times = {}
# List of products that have special handling
special_products = ["بيربل مست", "هايلاند بيريز", "سبايسي زيست"]
# List of products to exclude from sending
excluded_products = []
# Variable to store the time of the last clearing of the sent_products list
last_clear_time = time.time()

# Set up undetected Chrome driver
options = uc.ChromeOptions()
#options.add_argument("--headless")
driver = uc.Chrome(options=options)

def send_product_data_to_telegram():
    global sent_products, last_clear_time, product_send_times

    # Navigate to the page
    driver.get("https://www.dzrt.com/ar-sa/products")
    time.sleep(5)  # Wait for the page to load

    while True:
        driver.refresh()
        time.sleep(5)
       

        try:
            product_divs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".relative.bg-white.px-2\\.5.pb-3.pt-6"))
       )
        except:
           print("Error finding the element .....")


        product_data_list = []
        prduct_names = ["هايلاند بيريز", "جاردن منت", "ايسي رش", "بيربل مست", "منت فيوجن", "سمرة خاص", "هيلة", "سمرة", "ايسي رش", "سي سايد فروست", "إيدجي منت","تمرة"]

        for index, product_div in enumerate(product_divs):
            try:
                # Use the product name from the special_products list
                if index < len(prduct_names):
                    product_name = prduct_names[index]
                else:
                    print(f"No more product names available in the list for index {index}.")
                    continue
                
                # Wait for the "Add to Cart" button and check if it's disabled
                add_to_cart_button = WebDriverWait(product_div, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//button[contains(text(), 'اضف الى السلة')]"))
                )
                is_disabled = driver.execute_script("return arguments[0].hasAttribute('disabled');", add_to_cart_button)
                product_status = "متوفر" if not is_disabled else "غير متوفر"
        
                # Wait for the image tag and get its URL
                image_tag = WebDriverWait(product_div, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
                )
                image_url = image_tag.get_attribute('src') if image_tag else None
        
                # Wait for the product link and get its URL
                product_url = WebDriverWait(product_div, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "a"))
                ).get_attribute('href')
        
                # Add product information to the list
                if product_name and product_status:
                    product_info = {
                        "name": product_name,
                        "status": product_status,
                        "image_url": image_url,
                        "url": product_url
                    }
                    product_data_list.append(product_info)
        
                    # Print product information
                    print(f"Product Name: {product_name}")
                    print(f"Product Status: {product_status}")
                    print(f"Image URL: {image_url}")
                    print("-" * 50)
        
            except Exception as e:
                print(f"Error processing product: {e}")










# Define Telegram bot token and chat ID
        bot_token = "6958486146:AAFtYb_TaInJtSSFevXDn39BCssCzj4inV4"
        chat_id = "-1002411379455"
        telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

        for product_data in product_data_list:
            product_name = product_data.get("name", "")
            product_status = product_data.get("status", "")
            product_url = product_data.get("url", "")
            image_url = product_data.get("image_url", "")

            if product_status == "متوفر" and product_name not in excluded_products:
                current_time = time.time()
                if product_name in prduct_names:
                    if (product_name not in sent_products) or (current_time - product_send_times.get(product_name, 0) >= (3 * 6000)):
                        message_text = f"✅ ** المنتج متاح ** ✅: {product_name}"
                        reply_markup = {
                            "inline_keyboard": [
                                [{"text": "🔍 عرض المنتج", "url": product_url}, {"text": "🛒 عرض السلة", "url": "https://www.dzrt.com/ar/checkout/cart"}],
                                [{"text": "🔐 تسجيل الدخول", "url": "https://www.dzrt.com/ar/customer/account/login/"}, {"text": "💳 الانتقال إلى رابط الدفع النهائي", "url": "https://www.dzrt.com/ar/onestepcheckout.html"}]
                            ]
                        }
                        params = {
                            "chat_id": chat_id,
                            "photo": image_url,
                            "caption": message_text,
                            "reply_markup": json.dumps(reply_markup)
                        }
                        response = requests.post(telegram_api_url, params=params)
                        if response.status_code == 200:
                            print(f"Product data sent successfully for {product_name}")
                            sent_products.append(product_name)
                            product_send_times[product_name] = current_time
                        else:
                            print(f"Failed to send product data for {product_name}. Status code: {response.status_code}")
                else:
                    if product_name not in sent_products:
                        message_text = f"✅ ** المنتج متاح ** ✅: {product_name}"
                        reply_markup = {
                            "inline_keyboard": [
                                [{"text": "🔍 عرض المنتج", "url": product_url}, {"text": "🛒 عرض السلة", "url": "https://www.dzrt.com/ar/checkout/cart"}],
                                [{"text": "🔐 تسجيل الدخول", "url": "https://www.dzrt.com/ar/customer/account/login/"}, {"text": "💳 الانتقال إلى رابط الدفع النهائي", "url": "https://www.dzrt.com/ar/onestepcheckout.html"}]
                            ]
                        }
                        params = {
                            "chat_id": chat_id,
                            "photo": image_url,
                            "caption": message_text,
                            "reply_markup": json.dumps(reply_markup)
                        }
                        response = requests.post(telegram_api_url, params=params)
                        if response.status_code == 200:
                            print(f"Product data sent successfully for {product_name}")
                            sent_products.append(product_name)
                        else:
                            print(f"Failed to send product data for {product_name}. Status code: {response.status_code}")

        if time.time() - last_clear_time >= 6000:
            sent_products = [product for product in sent_products if product in special_products]
            last_clear_time = time.time()

        time.sleep(10)  # Check every 10 seconds

try:
    send_product_data_to_telegram()
finally:
    driver.quit()