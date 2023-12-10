import requests
import os
import sys
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
import tkinter as tk
from tkinter import ttk, filedialog, NORMAL, DISABLED
import threading


class QuickApplyException(Exception):
    pass


class Seeker(object):
    def __init__(self, role, temp_path, where, keywords):
        self.driver = None
        self.role = role
        self.temp_path = temp_path
        self.where = where
        self.keywords = keywords
        self.base_url = None
        self.output_folder = "outputs"
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
        self.listings_array = []
        self.listings_iterator = None
        
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
                        runs = paragraph.runs
                        for i in range(len(runs)):
                            if key in runs[i].text:
                                text = runs[i].text.replace(key, value)
                                runs[i].text = text
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

    def load_pages(self, max_pages=1):
        self.base_url = r"https://www.seek.co.nz/api/chalice-search/v4/search?siteKey=NZ-Main&where=" + self.where + "&keywords=" + self.keywords
        for page_num in range(1, max_pages):
            self.wait_random()
            url = self.base_url + f"&page={page_num}"
            res = requests.get(url)
            print(res.status_code)
            self.listings_array.extend(res.json().get('data'))
        self.listings_iterator = iter(self.listings_array)

    def complete_application(self):
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

    def apply(self):
        if self.driver is None:
            self.driver = webdriver.Chrome(service=ChromeService(), options=webdriver.ChromeOptions())

        try:
            listing = next(self.listings_iterator)
        except StopIteration:
            print("Completed all listings")
            self.driver.quit()
            return

        self.read_visited_jobs()
        self.temporary_documents = []
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
            if self.visited_jobs[self.job_id]['applied'] is True:
                print("Already applied")

        else:
            self.driver.get(self.job_url)
            print(f"Got {self.job_url}")

            self.replacements = {
                "COMPANY_NAME": self.company_name,
                "JOB_TITLE": self.job_title,
                "LOCATION_NAME": self.location
            }

            self.job_details = self.driver.find_element(By.CSS_SELECTOR, 'div[data-automation="jobAdDetails"]').text

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
                self.wait_random()
                self.complete_application()

            except TimeoutException:
                print("No quick apply")

            self.save_visited_job()
            self.remove_temporary_files()

        self.apply()


class Interface(Seeker):
    def __init__(self, root):
        self.root = root
        self.root.title("Seeker")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.role_label = ttk.Label(self.main_frame, text="Role:")
        self.role_label.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky='E')
        role_options = ['gis', 'developer']
        self.role_dropdown = ttk.Combobox(self.main_frame, textvariable=tk.StringVar(), values=role_options)
        self.role_dropdown.set(role_options[1])
        self.role_dropdown.grid(row=0, column=2, columnspan=2, pady=5, padx=5, sticky='W')

        self.temp_path_label = ttk.Label(self.main_frame, text="Temporary Path:")
        self.temp_path_label.grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky='E')
        self.browse_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_temp_path)
        self.browse_button.grid(row=1, column=2, columnspan=2, pady=5, padx=5, sticky='W')

        self.where_label = ttk.Label(self.main_frame, text="Where:")
        self.where_label.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky='E')
        self.where_entry = ttk.Entry(self.main_frame)
        self.where_entry.grid(row=2, column=2, columnspan=2, pady=5, padx=5, sticky='W')

        self.keywords_label = ttk.Label(self.main_frame, text="Keywords:")
        self.keywords_label.grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky='E')
        self.keywords_entry = ttk.Entry(self.main_frame)
        self.keywords_entry.grid(row=3, column=2, columnspan=2, pady=5, padx=5, sticky='W')

        self.run_button = ttk.Button(self.main_frame, text="Run", command=self.run_action)
        self.run_button.grid(row=4, column=1, columnspan=2, pady=5)

        self.skip_button = ttk.Button(self.main_frame, text="Skip current listing", command=self.skip_action, state=DISABLED)
        self.skip_button.grid(row=5, column=1, columnspan=2, pady=5)

        self.quit_button = ttk.Button(self.main_frame, text="Quit", command=self.quit_action)
        self.quit_button.grid(row=6, column=1, columnspan=2, pady=5)

        self.messages_label = ttk.Label(self.main_frame, text="", wraplength=240, justify='center')
        self.messages_label.configure(anchor="center")
        self.messages_label.grid(row=7, column=1, columnspan=2, pady=5)

        self.temp_path_output = None
        self.thread = None

    def browse_temp_path(self):
        temp_path = filedialog.askdirectory(title="Select Temporary Folder")
        self.temp_path_output = temp_path
        self.messages_label.config(text=f"Set temporary path to {temp_path}")

    @staticmethod
    def return_clean_url_args(url_args):
        return url_args.replace(' ', '+')

    def skip_action(self):
        print(f"Skipping {self.job_title}")
        try:
            self.remove_temporary_files()
        except:
            print("Couldn't remove temporary files")
        threading.Thread(target=self.apply).start()

    def quit_action(self):
        self.remove_temporary_files()
        self.driver.quit()
        self.root.destroy()
        sys.exit()

    def run_action(self):
        self.role = self.role_dropdown.get()
        self.temp_path = self.temp_path_output
        self.where = self.return_clean_url_args(self.where_entry.get())
        self.keywords = self.return_clean_url_args(self.keywords_entry.get())
        super().__init__(self.role, self.temp_path, self.where, self.keywords)

        self.load_pages(max_pages=2)
        self.skip_button['state'] = NORMAL
        self.messages_label.config(text="Running browser...")
        self.thread = threading.Thread(target=self.apply)
        self.thread.daemon = True
        self.thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    app.role_dropdown.set('developer')
    app.temp_path_output = r"C:\Users\angus\Documents\CV_Creator_Reborn\temporary"
    app.where_entry.insert(0, "All Australia")
    app.keywords_entry.insert(0, "Python Developer")
    test_path = r"C:\Users\angus\Documents\CV_Creator_Reborn\temporary"
    app.messages_label.config(text=f'Set temporary path to {test_path}')
    app.root.mainloop()

print("Complete")
