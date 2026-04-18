import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import csv
import os
from pathlib import Path

def human_typing(element, text, min_delay=0.05, max_delay=0.15):
    """Type characters one by one with random delays to simulate human behavior."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))

def send_whatsapp_message(driver, phone_number, message, max_retries=3):
    """Send a WhatsApp message with error handling and retry logic."""
    for attempt in range(max_retries):
        try:
            url = f"https://web.whatsapp.com/send?phone={phone_number}"
            driver.get(url)
            
            # Wait for page to load
            time.sleep(random.uniform(15, 22))
            
            # Try multiple XPath variations for better compatibility
            xpath_options = [
                '//div[@contenteditable="true"][@data-tab="10"]',
                '//div[@contenteditable="true"][@role="textbox"]',
                '//div[@contenteditable="true"]'
            ]
            
            input_box = None
            for xpath in xpath_options:
                try:
                    input_box = driver.find_element(By.XPATH, xpath)
                    if input_box:
                        break
                except:
                    continue
            
            if not input_box:
                raise Exception("Could not find message input box")
            
            input_box.click()
            time.sleep(random.uniform(1, 2))
            
            human_typing(input_box, message)
            time.sleep(random.uniform(1, 2))
            
            input_box.send_keys(Keys.ENTER)
            print(f"✓ Successfully sent message to: {phone_number}")
            time.sleep(random.uniform(10, 20))
            return True
            
        except Exception as e:
            print(f"✗ Failed to send to {phone_number} (attempt {attempt + 1}/{max_retries}). Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(random.uniform(5, 10))
            else:
                return False
    
    return False

def main():
    file_path = 'kontak.csv'
    
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' not found!")
        print("Please create a CSV file with 'nama' and 'nomor' columns.")
        return
    
    # Verify CSV structure
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            first_line = f.readline()
            if 'nama' not in first_line or 'nomor' not in first_line:
                print("Error: CSV must have 'nama' and 'nomor' columns")
                return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Browser configuration
    options = uc.ChromeOptions()
    # Uncomment to save session (no need to scan QR repeatedly)
    # options.add_argument('--user-data-dir=./whatsapp_session')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = None
    try:
        driver = uc.Chrome(options=options)
        driver.get("https://web.whatsapp.com")
        
        print("Please scan the QR Code if not logged in...")
        input("Press Enter AFTER WhatsApp Web is fully loaded...")
        
        processed = 0
        failed = 0
        
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                nama = row.get('nama', '').strip()
                nomor = row.get('nomor', '').strip()
                
                if not nama or not nomor:
                    print("⚠ Skipping invalid row (missing name or number)")
                    continue
                
                # Personalized message template
                pesan_custom = f"Hello {nama}, how are you? This is an automated personalized message."
                
                print(f"\nProcessing: {nama} ({nomor})...")
                if send_whatsapp_message(driver, nomor, pesan_custom):
                    processed += 1
                else:
                    failed += 1
                
                # Extended delay between contacts (important to avoid blocking)
                jeda_istirahat = random.uniform(45, 75)
                print(f"Waiting {int(jeda_istirahat)} seconds before next contact...")
                time.sleep(jeda_istirahat)
        
        print(f"\n✓ Complete! Processed: {processed}, Failed: {failed}")
        
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()