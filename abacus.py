import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def get_usb_devices():
    cmd = ["system_profiler", "SPUSBDataType"]
    output = subprocess.run(cmd, capture_output=True, text=True).stdout
    return output

def device_is_connected(device_name):
    devices_output = get_usb_devices()
    return device_name in devices_output

def open_website_and_login(driver, wait):
    driver.get("https://abacus.nosergroup.com")
    try:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/main/div/a[2]')))
        button.click()
        username_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]')))
        username_field.send_keys("din benuzername")
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_field.send_keys("dis passwort")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginButton"]')))
        login_button.click()
        driver.get("https://abacus.nosergroup.com/portal/myabacus/proj_inandout?qp=eyJUeXBlZE1hcCI6W3siVHlwZSI6IkdVSUQiLCJWYWx1ZSI6IjgzMDc5NTZkLTc3ZjgtZTgwMS1mNWI4LTAwNTA1NmI2MjhjMyIsIklEIjoiTUVOVV9JRCJ9LHsiVHlwZSI6IlN0cmluZyIsIlZhbHVlIjoiRU1QTE9ZRUUiLCJJRCI6IlBPUlRBTF9UWVBFIn1dfQ%3D%3D")
        print("Login successful")
        return True
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return False

def click_button_with_js(driver, wait, button_id):
    max_retries = 69
    for attempt in range(max_retries):
        try:
            js_script = f"document.getElementById('{button_id}').click();"
            driver.execute_script(js_script)
            print(f"Button '{button_id}' clicked successfully.")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}: An error occurred while clicking the button '{button_id}': {e}")
            if attempt < max_retries - 1:
                print("Attempting to log in again...")
                if open_website_and_login(driver, wait):
                    continue
                else:
                    print("Failed to log in. Retrying to click the button...")
            else:
                print(f"Failed to click button '{button_id}' after {max_retries} attempts.")
                return False

def put_mac_to_sleep():
    try:
        subprocess.run(["pmset", "sleepnow"], check=True)
        print("Mac is going to sleep.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to put Mac to sleep: {e}")

def main():
    print("Starting the program...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 30)
    driver.set_window_size(200, 200)
    driver.set_window_position(-10000, 0)

    if not open_website_and_login(driver, wait):
        print("Failed to open website and log in. Exiting.")
        driver.quit()
        return

    print("Monitoring USB devices for device named 'LOG'...")
    device_connected_previously = False
    try:
        while True:
            time.sleep(5)  # Check every 5 seconds
            device_connected_currently = device_is_connected("LOG")
            if device_connected_currently and not device_connected_previously:
                print("LOG is now connected: Hello World")
                click_button_with_js(driver, wait, "mainAction")
            elif not device_connected_currently and device_connected_previously:
                print("LOG has been removed.")
                if click_button_with_js(driver, wait, "mainActionPrimaryAction"):
                    put_mac_to_sleep()
            device_connected_previously = device_connected_currently
    except KeyboardInterrupt:
        print("Stopped monitoring.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
