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
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI


class QuickApplyException(Exception):
    pass


class Seeker(object):
    def __init__(self, role, temp_path, where, keywords, pause_description_sec):
        self.driver = webdriver.Chrome(service=ChromeService(), options=webdriver.ChromeOptions())
        self.role = role
        self.temp_path = temp_path
        self.base_url = r"https://www.seek.co.nz/api/chalice-search/v4/search?siteKey=NZ-Main&where=" + where + "&keywords=" + keywords
        self.output_folder = "outputs"
        self.pause_description_sec = pause_description_sec
        self.job_title = None
        self.location = None
        self.job_id = None
        self.job_url = None
        self.data_dict = None
        self.secrets = None
        self.company_name = None
        self.cv_name_raw = None
        self.cover_letter_name_raw = None
        self.document = None
        self.template_path = None
        self.replacements = None
        self.cv_temp = None
        self.cv_path = None
        self.cv_name = None
        self.cover_letter_temp = None
        self.cover_letter_path = None
        self.cover_letter_name = None
        self.visited_jobs = None
        self.temporary_documents = []
        
    @staticmethod
    def return_clean_name(name):
        return name.lower().replace(" ", "_").replace("-", "_").replace("/", "_").replace("|", "_").replace("__", "_")
    
    def load_secrets(self):
        with open('secrets.json', 'r') as file:
            self.secrets = json.load(file)
    
    @staticmethod
    def wait_random():
        seconds = random.randint(1, 3)
        print(f"Waiting {seconds} seconds", end='\r')
        time.sleep(seconds)
    
    def log_in(self):
        self.load_secrets()
        email = self.secrets['seek_login']['email']
        password = self.secrets['seek_login']['password']
    
        text_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'emailAddress'))
        )
        text_box.send_keys(email)
    
        text_box = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )
        text_box.send_keys(password)
    
        login_button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="signin_seekanz"]/div/div[4]/div/div[1]/button'))
        )
        self.wait_random()
        login_button.click()
        self.wait_random()

    def read_visited_jobs(self):
        with open('visited_jobs.json', 'r') as file:
            self.visited_jobs = json.load(file)
    
    def save_visited_job(self):
        self.visited_jobs[self.job_id] = self.data_dict
        with open('visited_jobs.json', 'w') as file:
            json.dump(self.visited_jobs, file, indent=4)
    
    def return_chat_gpt_response(self, job_description):
        client = OpenAI(api_key=self.secrets["chat_gpt_login"]["key"])
        message = f"In no more that 70 words, write why I want this job based on this job description: {job_description}"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": message}], model="gpt-3.5-turbo",
        )
        return chat_completion.choices[0].message.content
        
    def save_document(self, document_type):
        document_name = self.return_clean_name(f"{document_type}_angus_hunt_{self.job_title}.docx")
        document_path = os.path.join(self.output_folder, document_name)
        self.document.save(document_path)
        document_temp_path = os.path.join(self.temp_path, document_name)
        shutil.copyfile(document_path, document_temp_path)
        self.temporary_documents.append(document_temp_path)
        
    def update_document(self):
        for key, value in self.replacements.items():
            for paragraph in self.document.paragraphs:
                if key in paragraph.text:
                    try:
                        paragraph.text = paragraph.text.replace(key, value)
                    except TypeError:
                        pass

    def remove_temporary_files(self):
        for temporary_document in self.temporary_documents:
            os.remove(temporary_document)
        
    def query_chat_gpt(self):
        self.replacements["CHAT_GPT_RESPONSE"] = self.return_chat_gpt_response(self.job_details)

    def click_quick_apply(self):
        quick_apply_button = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Quick apply'))
        )
        quick_apply_button.click()

    def execute(self):
        for page_num in range(0, 100):
            self.wait_random()
            url = self.base_url + f"&page={page_num}"
            res = requests.get(url)
            print(res.status_code)
            listings_array = res.json().get('data')
        
            self.read_visited_jobs()
        
            if len(listings_array) == 0:
                print("Reached end of listings")
                break
        
            for listing in listings_array:
                is_agency = False
                self.company_name = listing.get("companyName")
        
                if self.company_name is None:
                    is_agency = True
                    self.company_name = listing.get("advertiser").get('description')
        
                self.job_title = listing.get("title")
                self.location = listing.get("location")
                self.job_id = listing.get('solMetadata').get('jobId')
                self.job_url = r"https://www.seek.co.nz/job/" + self.job_id
        
                self.data_dict = {
                    "job_title": self.job_title,
                    "company_name": self.company_name,
                    "location": self.location,
                    "url": self.job_url,
                    "applied": False
                }
        
                if self.job_id in self.visited_jobs.keys():
                    print("Already applied")
                    pass
        
                else:
                    self.driver.get(self.job_url)
                    print(f"Got {self.job_url}")
                    time.sleep(self.pause_description_sec)

                    self.replacements = {
                        "COMPANY_NAME": self.company_name,
                        "JOB_TITLE": self.job_title,
                        "LOCATION_NAME": self.location
                    }

                    self.job_details = self.driver.find_element(By.CSS_SELECTOR, 'div[data-automation="jobAdDetails"]').text
                    print(self.job_details)

                    if self.role == "chat_gpt_test":
                        self.query_chat_gpt()

                    if is_agency:
                        self.template_path = os.path.join("templates", f"cover_letter_angus_hunt_{self.role}_agency.docx")
                    else:
                        self.template_path = os.path.join("templates", f"cover_letter_angus_hunt_{self.role}.docx")

                    self.document = Document(self.template_path)
                    self.update_document()

                    for document_type in ['cv', 'cover_letter']:
                        self.save_document(document_type)

                    try:
                        self.click_quick_apply()
                    except TimeoutException:
                        print("No quick apply")
                        self.save_visited_job()
                        self.remove_temporary_files()
                        break

                    self.wait_random()
                    if EC.presence_of_element_located((By.ID, 'password')):
                        try:
                            self.log_in()
                        except:
                            print("Automatic log-in failed; please enter login details manually")

                    pyperclip.copy(self.temp_path)

                    print("Please complete application. This browser will expire in 5 mins.")

                    try:
                        WebDriverWait(self.driver, 300).until(
                            EC.presence_of_element_located((By.ID, 'applicationSent'))
                        )
                        print(f"Application for {self.job_title} sent successfully.")
                        self.data_dict["applied"] = True

                    except NoSuchWindowException:
                        print("Reopening closed browser")
                        self.driver = webdriver.Chrome(service=ChromeService(), options=webdriver.ChromeOptions())
        
                    self.save_visited_job()
                    self.remove_temporary_files()


seeker = Seeker(
    role="developer",
    temp_path=r"C:\Users\angus\Documents\CV_Creator_Reborn\temporary",
    where="All+Australia",
    keywords="Python+Developer",
    pause_description_sec=30
)
seeker.execute()
print("Complete")
