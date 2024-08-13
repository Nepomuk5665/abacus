import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def get_usb_devices():
    cmd = ["system_profiler", "SPUSBDataType"]
    output = subprocess.run(cmd, capture_output=True, text=True).stdout
    return output

def device_is_connected(device_name):
    devices_output = get_usb_devices()
    return device_name in devices_output

def open_website_and_login():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://abacus.nosergroup.com")
    try:
        wait = WebDriverWait(driver, 30)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/main/div/a[2]')))
        button.click()
        username_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]')))
        username_field.send_keys("din benuzername")
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_field.send_keys("dis pw")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginButton"]')))
        login_button.click()
        driver.get("https://abacus.nosergroup.com/portal/myabacus/proj_inandout?qp=eyJUeXBlZE1hcCI6W3siVHlwZSI6IkdVSUQiLCJWYWx1ZSI6IjgzMDc5NTZkLTc3ZjgtZTgwMS1mNWI4LTAwNTA1NmI2MjhjMyIsIklEIjoiTUVOVV9JRCJ9LHsiVHlwZSI6IlN0cmluZyIsIlZhbHVlIjoiRU1QTE9ZRUUiLCJJRCI6IlBPUlRBTF9UWVBFIn1dfQ%3D%3D")
        driver.set_window_size(200, 200)
        driver.set_window_position(-10000, 0)
        return driver, wait
    except Exception as e:
        print(f"An error occurred during login: {e}")
        driver.quit()
        return None, None

def click_button_with_js(driver, button_id):
    try:
        js_script = f"document.getElementById('{button_id}').click();"
        driver.execute_script(js_script)
        print(f"Button '{button_id}' clicked successfully.")
    except Exception as e:
        print(f"An error occurred while clicking the button '{button_id}': {e}")

def put_mac_to_sleep():
    try:
        subprocess.run(["pmset", "sleepnow"], check=True)
        print("Mac is going to sleep.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to put Mac to sleep: {e}")

def main():
    print("Opening website and logging in...")
    driver, wait = open_website_and_login()
    if not driver or not wait:
        print("Failed to open website and log in. Exiting.")
        return

    print("Monitoring USB devices for device named 'LOG'...")
    device_connected_previously = False
    try:
        while True:
            time.sleep(5) 
            device_connected_currently = device_is_connected("LOG")
            if device_connected_currently and not device_connected_previously:
                print("LOG is now connected: Hello World")
                click_button_with_js(driver, "mainAction")
            elif not device_connected_currently and device_connected_previously:
                print("LOG has been removed.")
                click_button_with_js(driver, "mainActionPrimaryAction")
                put_mac_to_sleep()
            device_connected_previously = device_connected_currently
    except KeyboardInterrupt:
        print("Stopped monitoring.")
    finally:
        driver.quit()  # Make sure to close the browser session

if __name__ == "__main__":
    main()
