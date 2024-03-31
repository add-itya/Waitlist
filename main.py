from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pydantic import BaseModel
from typing import List

app = FastAPI()

class WaitlistNotificationRequest(BaseModel):
    username: str
    password: str
    term: str
    phone_number: str
    carrier: str
    class_nums: List[str]

@app.post("/waitlist-notification/")
async def waitlist_notification(request_data: WaitlistNotificationRequest):
    # Start a browser session options=chrome_options
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    # Open the webpage
    driver.get("https://one.ufl.edu/")

    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "dfJjmO"))
    )

    # Click the login button
    login_button.click()

    # Username button
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "j_username"))
    )

    # Send keys to the username input field
    username_input.send_keys(request_data.username)

    # Password button
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "j_password"))
    )

    # Send keys to password input field
    password_input.send_keys(request_data.password)

    # Login button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "_eventId_proceed"))
    )

    # Click the login button
    login_button.click()

    # Wait until not in duo security
    while "duosecurity" in driver.current_url:
        sleep(1)
        if driver.current_url == 'https://one.uf.edu/':
            break
        try:
            button = WebDriverWait(driver, 0).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, this is my device')]")))
            button.click()
        except:
            pass
    
    # Open schedule for the specified term
    driver.get(f"https://one.uf.edu/myschedule/{request_data.term}")
    

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
    

    # Click add course button
    add_course_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "cKFOMJ"))
    )
    add_course_button.click()

    email_body = str()
    ret = list()
    for class_num in request_data.class_nums:
        class_number_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "class-num")))
        class_number_input.send_keys(Keys.CONTROL + "a")
        class_number_input.send_keys(Keys.DELETE)
        class_number_input.send_keys(class_num)

        submit_butt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search')]")))
        submit_butt.click()

        # Wait for waitlist element
        wait_list_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Wait List:')]")))

        # Get the waitlist number
        pattern = r"Wait List: (\d+)"
        match = re.search(pattern, wait_list_element.text)
        wait_list_count = int(match.group(1))
        class_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'p.sc-kpDqfm.dvjGPq.MuiTypography-root.MuiTypography-body1.sc-bHnlcS.hSUoMM'))
        )
        class_name = class_name.text
        ret.append(wait_list_count)
        email_body += f"Waitlist count for {class_name}: {wait_list_count}\n\n"



    # Send text to phone with SMTP
    email = "waitlist279@gmail.com"
    password = "gewj yzly omuz vvcv"
    phone_email = f"{request_data.phone_number}@{request_data.carrier}"

    # Send email
    def send_email(body):
        message = MIMEText(body, "plain")
        message["From"] = email
        message["To"] = phone_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        text = message.as_string()
        server.sendmail(email, phone_email, text)
        server.quit()
    
    send_email(email_body)

    # Close browser session
    driver.quit()
    print(ret)
    return ret