from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Set up the WebDriver
driver = webdriver.Chrome()

# Open the login page
driver.get("http://118.179.149.36:8082/login")

# Wait for the email input field to be present
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
)

# Find the email input field
email_input = driver.find_element("css selector", "input[type='email']")

# Find the email and password input fields and the login button
email_input = driver.find_element("css selector", "input[type='email']")
password_input = driver.find_element("id", "password")
login_button = driver.find_element("css selector", "button[type='submit']")

# Fill in the email and password fields
email_input.send_keys("admin@example.com")
password_input.send_keys("password")

# Click the login button
login_button.click()

# Wait for the Common link to be clickable
common_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//p[contains(text(),'Common')]"))
)

# Click the Common link
common_link.click()


# Wait for the attendance link to be clickable
attendance_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/attendance']"))
)


# Click the attendance link
attendance_link.click()

# Wait for the DLC Name dropdown to be clickable
dlc_name_dropdown = WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.multiselect__input[aria-controls='listbox-null']"))
)

# Click on the DLC Name dropdown to open it
dlc_name_dropdown.click()

# Wait for the dropdown options to be present
dropdown_options = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".multiselect__select"))
)

# Loop through the options to find and click on the desired option
desired_option_text = "DLC_Jarir"
for option in dropdown_options:
    if option.text == desired_option_text:
        option.click()
        break

        


# Introduce a delay to keep the browser open for demonstration purposes
time.sleep(10)

# Quit the driver
driver.quit()
