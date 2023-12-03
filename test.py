import time
import json
import random
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def load_secrets():
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
    return secrets


def wait_random():
    seconds = random.randint(1, 3)
    print(f"Waiting {seconds} seconds", end='\r')
    time.sleep(seconds)


def log_in():
    secrets_data = load_secrets()
    email = secrets_data['seek_login']['email']
    password = secrets_data['seek_login']['password']

    driver.get(r"https://www.seek.com.au/oauth/login/?returnUrl=%2F")
    text_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'emailAddress'))
    )
    text_box.send_keys(email)

    text_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    text_box.send_keys(password)

    login_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="signin_seekanz"]/div/div[4]/div/div[1]/button'))
    )
    wait_random()
    login_button.click()
    wait_random()


chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
log_in()
job_ids = ['71825612', '71425478']
for job_id in job_ids:
    try:
        url = r"https://www.seek.co.nz/job/" + job_id
        driver.get(url)

        quick_apply_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Quick apply'))
        )
        quick_apply_button.click()

        pyperclip.copy(r"C:\Users\angus\Documents\CV_Creator_Reborn\temporary")
        print("Copied saved path")

        cv_success = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, r'upload-another-resume'))
        )
        print("Uploaded CV")

        cover_letter_success = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, r'coverLetterField'))
        )
        print("Uploaded cover letter")

        print("Please fill in role requirements. This page will expire in 5 mins.")
        application_success = WebDriverWait(driver, 300).until(
            EC.url_contains('success')
        )
        print("Application sent successfully.")

    except WebDriverException as e:
        # Handle the browser close event gracefully
        print(f"Browser closed by the user: {e}")

print("Complete")
