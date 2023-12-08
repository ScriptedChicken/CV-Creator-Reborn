import requests
import os
from docx import Document
import shutil
import time
import json
import random
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchWindowException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI


class QuickApplyException(Exception):
    pass


def return_clean_name(name):
    return name.lower().replace(" ", "_").replace("-", "_").replace("/", "_").replace("|", "_").replace("__", "_")


def load_secrets():
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
    return secrets


def wait_random():
    seconds = random.randint(1, 3)
    print(f"Waiting {seconds} seconds", end='\r')
    time.sleep(seconds)


def return_api_key():
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
    return secrets["chat_gpt_login"]["key"]


def log_in():
    secrets_data = load_secrets()
    email = secrets_data['seek_login']['email']
    password = secrets_data['seek_login']['password']

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


def save_visited_job(job_id, data_dict):
    visited_jobs[job_id] = data_dict
    with open('visited_jobs.json', 'w') as file:
        json.dump(visited_jobs, file, indent=4)


def return_chat_gpt_response(job_description):
    client = OpenAI(api_key=return_api_key())
    message = f"In no more that 70 words, write why I want this job based on this job description: {job_description}"
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user","content": message}],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content


role = "developer"

TEMP_PATH = r"C:\Users\angus\Documents\CV_Creator_Reborn\temporary"
url = r"https://www.seek.co.nz/api/chalice-search/v4/search?siteKey=NZ-Main&where=All+Australia&keywords=Python+Developer"
res = requests.get(url)
print(res.status_code)

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

with open('visited_jobs.json', 'r') as file:
    visited_jobs = json.load(file)

for listing in res.json().get('data'):
    is_agency = False
    company_name = listing.get("companyName")

    if company_name is None:
        is_agency = True
        company_name = listing.get("advertiser").get('description')

    job_title = listing.get("title")
    location = listing.get("location")
    job_id = listing.get('solMetadata').get('jobId')
    job_url = r"https://www.seek.co.nz/job/" + job_id

    data_dict = {
        "job_title": job_title,
        "company_name": company_name,
        "location": location,
        "url": job_url,
        "applied": False
    }

    if job_id in visited_jobs.keys():
        pass
    
    else:
        driver.get(job_url)
        replacements = {
            "COMPANY_NAME": company_name,
            "JOB_TITLE": job_title,
            "LOCATION_NAME": location
        }

        if role == "chat_gpt_test":
            time.sleep(2)
            element = driver.find_element(By.CSS_SELECTOR, 'div[data-automation="jobAdDetails"]')
            chat_gpt_response = return_chat_gpt_response(element.text)
            replacements["CHAT_GPT_RESPONSE"] = chat_gpt_response
    
        if is_agency:
            template_path = os.path.join("templates", f"cover_letter_angus_hunt_{role}_agency.docx")
        else:
            template_path = os.path.join("templates", f"cover_letter_angus_hunt_{role}.docx")
        output_folder = "outputs"
    
        doc = Document(template_path)
    
        for key, value in replacements.items():
            for paragraph in doc.paragraphs:
                if key in paragraph.text:
                    try:
                        paragraph.text = paragraph.text.replace(key, value)
                    except TypeError:
                        pass
    
        cover_letter_name = return_clean_name(f"cover_letter_angus_hunt_{job_title}.docx")
        cover_letter_path = os.path.join(output_folder, cover_letter_name)
        doc.save(cover_letter_path)
    
        cv_name = return_clean_name(f'cv_angus_hunt_{job_title}.docx')
        cv_path = os.path.join('outputs', cv_name)
        shutil.copyfile(os.path.join('templates', f'cv_angus_hunt_{role}.docx'), cv_path)
    
        cover_letter_temp = os.path.join(TEMP_PATH, cover_letter_name)
        shutil.copyfile(cover_letter_path, cover_letter_temp)
    
        cv_temp = os.path.join(TEMP_PATH, cv_name)
        shutil.copyfile(cv_path, cv_temp)

        try:
            already_applied_flag = driver.find_element(By.ID, 'applied')
            print("Already applied - skipping")

        except:
            quick_apply_button = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Quick apply'))
            )
            quick_apply_button.click()

            time.sleep(2)
            if EC.presence_of_element_located((By.ID, 'password')):
                try:
                    log_in()
                except:
                    print("Automatic log-in failed; please enter login details manually")

            pyperclip.copy(TEMP_PATH)

            print("Please complete application. This browser will expire in 5 mins.")
            application_success = WebDriverWait(driver, 300).until(
                EC.url_contains('success')
            )

            print(f"Application for {job_title} sent successfully.")
            data_dict["applied"] = True

        save_visited_job(job_id, data_dict)
        # os.remove(cover_letter_temp)
        # os.remove(cv_temp)
        break

print("Complete")
