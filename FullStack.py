from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, \
    ElementNotInteractableException
import sys
# Mail Importing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Import MIMEText for body text
from email.mime.base import MIMEBase
from email import encoders

import time
import csv
import random
import os
import datetime
import requests

# from config import USERNAME, PASSWORD, CHROME_DRIVER_PATH, OUTPUT_DIRECTORY, LINK, KEYWORDS, FRAUD_COMPANIES_LIST, MAX_NO_OF_PAGES_TO_POOL

# USERNAME = "dakshayaniyellanki@gmail.com"
# PASSWORD = "#@292686@#"
# USERNAME = "kotaharshita@gmail.com"
# PASSWORD = "Harshita123$"
# USERNAME = "8106012348"
# PASSWORD = "r@vinxtwave"
# USERNAME = "anjalianuz.0508@gmail.com"
# PASSWORD = "Satyavathi@3213"
# USERNAME = "subbumanne28@gmail.com"
# PASSWORD = "Oppo@123"
CHROME_DRIVER_PATH = r"c:\Users\NxtWave Hire\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe"
OUTPUT_DIRECTORY = r"C:\Users\linus\Downloads\LinkedIN"
# key_word = sys.argv[1]
# USERNAME = sys.argv[2]
# PASSWORD = sys.argv[3]
key_word = 'FullStack'
# USERNAME = "kotaharshita@gmail.com"
# PASSWORD = "Harshita123$"
LINK = f'https://www.linkedin.com/jobs/search/?currentJobId=4304630441&f_E=1%2C2&f_TPR=r86400&keywords={str(key_word)}'
print(f'Scraping with Keyword "{key_word}"')
# print ( f'Current Arguments :{sys.argv[1:]}')

print(f'LINK : {LINK} ')
# LINK ="https://www.linkedin.com/jobs/search/?currentJobId=4304630441&f_E=1%2C2&f_TPR=r86400&keywords=%28%22React%20Developer%22%20OR%20%22Frontend%20Developer%22%20OR%20%22Front%20End%20Developer%22%29%20AND%20%28React%20OR%20%22React.js%22%20OR%20%22ReactJS%22%29"
# WEB_APP_URL = "https://script.google.com/macros/s/AKfycbztQssu11nwksFG_mdVOFW_fVRuJPxsejmj9cRhLOIKCdCYWxp66aVJgYHrnge36lIQDQ/exec"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw_G1iVzFqdGNcaeTIg59uPhUPerf5m0bawyBmjEW51mymYoP1V6LNfCLNFRy6L5qQhXA/exec"
KEYWORDS = ["Entry Level", "0", "0-1", "0-2", "Internship+ Full Time", "Internship", "2024", "2025", "2023",
            "Recent Graduates", "PPO", "JobOffer", "Trainee", "Intern", "0-3"]
FRAUD_COMPANIES_LIST = ["Turing", "Wipro", "Infosys", "Tech Mahindra", "CGI", "Tekwissen India", "Enerzcloud Solutions",
                        "The Skillians" "GE Healthcare", "IBM", "Larsen & Toubro", "Innovate Solutions", "Lead India",
                        "WeBoost Solutions by UM", "UM IT Solutions", "UNIKWORKS", "Infosys", "Accenture",
                        "myGwork - LGBTQ+ Business Community", "SkillFied Mentor", "AlgoSec", "NA",
                        "Zetheta Algorithms Private Limited", "Outscal Gaming", "turning", "Internkaksha IT Solutions",
                        "Truelancer.com", "Unified Mentor", "Unified Mentor Private Limited", "Uplers", "MedTourEasy",
                        "Aadhvik Technologies", "Buddha Education Association Incorporation", "pawz", "MentorBoxx",
                        "Coding Junior", "Vicharak Computers LLP", "Accenture", "Bajaj Finserv Ltd.", "Jio",
                        "Leading IT Company", "Large-Sized Firm in IT Services Sector", "Leading MNC Client",
                        "Nexpro247", "O A Compserve", "Rakesh Kumar", "MNC Group", "Accenture in India",
                        "Divya Placement Consultants", "EY", "TECHPLEMENT", "The BigCjobs.com", "Workassist",
                        "Refonte Learning", "Skill Secure AI", "Traders Training Academy"]
SKIP_ROLE_NAMES = ["Azure", "Business Development", "SALES", "Campus Ambassador", "Data Analytics", "Data Engineer",
                   "Data Scientist", "Devops", "Data Analyst", "Digital Marketing", "Operations", "Embedded Engineer",
                   "Flutter", "Human Resources", "iOS Developer", "WordPress", "Sales Executive", "Sales Intern", "SEO",
                   "Shopify", "Test Engineer", "Volunteer Internship", "Product Analyst", "Product manager", "Research",
                   "Cybersecurity", "Business Analyst", "Electrical Engineer", "SDET", "Word Press", "L2 Support",
                   "L1 Support", "L3 Support", "Apprentice", "Marketing Intern", "Marketing", "React Native",
                   "Graphic Design", "Graphic Designer", "Placement Coordinator", "Blockchain", "Project Engineer",
                   "Product Analyst", "Mechanical", "AWS", "Service Engineer", "Site Engineer"]

MAX_NO_OF_PAGES_TO_POOL = 10

# Email credentials for Gmail
SENDER_EMAIL = "sunilchandralanke@gmail.com"  # Replace with your Gmail address
SENDER_PASSWORD = "iiii"  # Use your App Password if 2FA is enabled

# List of recipients' emails
RECIPIENT_EMAILS = ["linuslanke@gmail.com"]  # Add multiple emails here
RECIPIENT_EMAIL = ",".join(RECIPIENT_EMAILS)  # Join the list of emails into a comma-separated string

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # This is the port for TLS/STARTTLS

chrome_options = Options()
chrome_options.add_argument("--disable-webrtc")
chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-position=-3000,0")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_experimental_option('detach', True)
# chrome_options.add_argument("--window-size=2560,1440")   # set large window size
# chrome_options.add_argument("--force-device-scale-factor=0.6")
# Set up the WebDriver (using Chrome in this example)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
# Initialize an empty list to store job details
jobs_list = []


def account_login(USERNAME, PASSWORD):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    # print("logging into the Portal")
    # Enter the username
    username = driver.find_element(By.ID, "username")
    username.send_keys(str(USERNAME))  # Use constant from configf
    # print('sent username')
    # Enter the password
    password = driver.find_element(By.ID, "password")
    password.send_keys(str(PASSWORD))  # Use constant from config
    # print('sent password')
    time.sleep(2)
    # Click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    # print('login button clicked')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".global-nav__me-photo")))
    # print("accessing the profile image")


def scroll_job_list():
    # Locate the parent div containing the job list
    parent_div = driver.find_element(By.CLASS_NAME, "scaffold-layout__list")

    # Find all the child div elements within the parent container
    child_divs = parent_div.find_elements(By.TAG_NAME, "div")

    # The second element is the one you're interested in, so access it by index
    second_child = child_divs[1]  # Index 1 represents the second child
    num_elements_to_load = 3  # Number of elements to load with each scroll

    loaded_elements = len(driver.find_elements(By.CSS_SELECTOR, "[data-occludable-job-id]"))
    total_elements = loaded_elements + num_elements_to_load

    while loaded_elements < total_elements:
        # print(f"Scrolling to load next {num_elements_to_load} job items...")

        # Scroll down a bit to load the next set of elements
        driver.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", second_child)
        time.sleep(2)  # Allow time for the elements to load

        new_loaded_elements = len(driver.find_elements(By.CSS_SELECTOR, "[data-occludable-job-id]"))

        if new_loaded_elements == loaded_elements:
            # print("No more new elements loaded.")
            break  # Stop if no new elements are being loaded
        else:
            # print(f"Loaded {new_loaded_elements - loaded_elements} new job items.")
            loaded_elements = new_loaded_elements


def extract_job_details(key_word):
    wait_time = random.randint(1, 3)
    time.sleep(wait_time)

    # Initialize all variables with default values
    title = "NA"
    job_link = "NA"
    company_name = "NA"
    company_name_link = "NA"
    company_website = "NA"
    employee_size = "NA"
    company_industry = "NA"
    company_city = "NA"
    company_linkedin_url = "NA"
    location = "NA"
    posted_time = "NA"
    insight_text = "NA"
    job_description = "NA"
    poc_name = "NA"
    poc_link = "NA"
    connection_degree = "NA"
    headline = "NA"

    main_container = driver.find_element(By.CLASS_NAME, "jobs-search__job-details--wrapper")

    # Extract Job Title
    try:
        title = main_container.find_element(By.CSS_SELECTOR, "h1.t-24.t-bold.inline a").text
    except:
        title = "NA"

    # Check if the role name should be skipped
    if any(skip_role.lower() in title.lower() for skip_role in SKIP_ROLE_NAMES):
        # print(f"Skipping job with role name: {title}")
        return  # Skip this job and move to the next one

    # Extract Job Link
    try:
        job_title_element = main_container.find_element(By.CSS_SELECTOR,
                                                        "div.t-24.job-details-jobs-unified-top-card__job-title h1 a")
        job_link = job_title_element.get_attribute("href")
    except:
        job_link = "NA"

    # Extract Company Name and Company Link
    try:
        company_name_element = main_container.find_element(By.CLASS_NAME,
                                                           "job-details-jobs-unified-top-card__company-name")
        company_name_link = company_name_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        company_name = company_name_element.text
    except:
        company_name = "NA"
        company_name_link = "NA"

    # Check if the company is in the fraud list (case insensitive)
    if company_name.lower() in [fraud_company.lower() for fraud_company in FRAUD_COMPANIES_LIST]:
        # print(f"Skipping job from fraudulent company: {company_name}")
        return  # Skip this job and move to the next one
    else:
        pass
        # print("No fraud detected")

    # Extract POC (Point of Contact) details
    try:
        # Check if hiring team section exists using a more reliable method
        hiring_team_sections = driver.find_elements(By.TAG_NAME, "h2")
        hiring_team_section = None
        for section in hiring_team_sections:
            if "Meet the hiring team" in section.text:
                hiring_team_section = section
                break

        if hiring_team_section:
            # Extract POC name and profile link
            try:
                poc_element = driver.find_element(By.CSS_SELECTOR, "span.jobs-poster__name strong")
                poc_name = poc_element.text.strip()

                # Get the parent anchor tag for the profile link
                poc_link = poc_element.find_element(By.XPATH, "./ancestor::a").get_attribute("href")
            except:
                poc_name = "NA"
                poc_link = "NA"

            # Extract connection degree
            try:
                connection_degree_element = driver.find_element(By.CSS_SELECTOR, "span.hirer-card__connection-degree")
                connection_degree = connection_degree_element.text.strip()
            except:
                connection_degree = "NA"

            # Extract headline
            try:
                headline_element = driver.find_element(By.CSS_SELECTOR, "div.text-body-small")
                headline = headline_element.text.strip()
            except:
                headline = "NA"

            # print(f"POC Name: {poc_name}")
            # print(f"POC Link: {poc_link}")
            # print(f"Connection Degree: {connection_degree}")
            # print(f"Headline: {headline}")
        else:
            # print("Hiring team section not found.")
            poc_name = "NA"
            poc_link = "NA"
            connection_degree = "NA"
            headline = "NA"
    except Exception as e:
        # print(f"Error extracting POC details: {str(e)}")
        poc_name = "NA"
        poc_link = "NA"
        connection_degree = "NA"
        headline = "NA"

    # Modify the URL to point to the 'About' page (replace 'life' with 'about')
    if company_name_link != "NA":
        company_about_url = company_name_link.replace("/life", "/about")
        # print(f"Company About URL: {company_about_url}")

        # Open the About page in a new tab
        driver.execute_script(f"window.open('{company_about_url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

        # Extract Company Website from the About page
        try:
            website_element = driver.find_element(By.CSS_SELECTOR, "dd.mb4.t-black--light.text-body-medium a")
            company_website = website_element.get_attribute("href")
        except:
            company_website = "NA"

        # Extract Employee Size from the About page
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, "dd.t-black--light.mb4.text-body-medium a span")
            employee_size = "NA"
            for element in elements:
                if "associated members" in element.text.lower() or "associated member" in element.text.lower():
                    employee_size = element.text.strip()
                    break
        except:
            employee_size = "NA"

        # Get company LinkedIn URL (removing /about)
        company_linkedin_url = company_name_link.replace("/about", "")

        # Extract Industry and City from the About page
        try:
            info_items = driver.find_elements(By.CLASS_NAME, "org-top-card-summary-info-list__info-item")
            if len(info_items) >= 2:
                company_industry = info_items[0].text.strip()
                company_city = info_items[1].text.strip()
            else:
                company_industry = "NA"
                company_city = "NA"
        except:
            company_industry = "NA"
            company_city = "NA"

        # Close the About page and switch back to the main tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # Switch back to the original tab
    else:
        company_website = "NA"

    # Extract Location and Posted Time
    try:
        primary_description_container = main_container.find_element(By.CLASS_NAME,
                                                                    "job-details-jobs-unified-top-card__primary-description-container")
        primary_description_text = primary_description_container.text
        parts = primary_description_text.split(' · ')

        if len(parts) >= 2:
            location = parts[0].strip()
            posted_time = parts[1].strip()
        else:
            location = "NA"
            posted_time = "NA"
    except Exception as e:
        location = "NA"
        posted_time = "NA"
    try:
        job_insight_element = driver.find_element(By.CLASS_NAME, "job-details-fit-level-preferences")
        insight_text = job_insight_element.text.strip()
    except NoSuchElementException:
        insight_text = "NA"

    # Extract Job Description
    try:
        job_description_element = driver.find_element(By.CSS_SELECTOR,
                                                      "div.jobs-box__html-content.jobs-description-content__text--stretch")
        job_description = job_description_element.text.strip()
    except:
        job_description = "NA"

    # Track matched keywords, allowing partial matches for all except "PPO"
    matched_keywords = []

    for keyword in KEYWORDS:
        if keyword.lower() in ["ppo", "intern", "internship", "interns"]:
            # Exact match check for "PPO" (case insensitive)
            if any(f" {keyword.lower()} " in f" {detail.lower()} " for detail in
                   [job_description, title, company_name]):
                matched_keywords.append(key_word)
        else:
            # Partial match for other keywords (case insensitive)
            if any(keyword.lower() in detail.lower() for detail in [job_description, title, company_name]):
                matched_keywords.append(key_word)

    matched_keywords_str = ', '.join(matched_keywords) if matched_keywords else "None"

    # print(f"Job Link: {job_link}")
    # print(f"Company Website: {company_website}")
    # print(f"Employee Size: {employee_size}")
    # print(f"Company Industry: {company_industry}")
    # print(f"Company City: {company_city}")
    # print(f"Company LinkedIn URL: {company_linkedin_url}")
    # #print(f"Matched Keywords: {matched_keywords_str}")

    job_details = {
        "Title": title,
        "Company": company_name,
        "Posted Time": posted_time,
        "Location": location,
        "Job Link": job_link,
        "Job Details": insight_text,
        "Job Description": job_description,
        "Matched Keywords": matched_keywords_str,
        "Company Website": company_website,
        "Employee Size": employee_size,
        "Company Industry": company_industry,
        "Company City": company_city,
        "Company LinkedIn URL": company_linkedin_url,
        "POC Name": poc_name,
        "POC Profile Link": poc_link,
        "Connection Degree": connection_degree,
        "POC Headline": headline
    }

    jobs_list.append(job_details)
    # "additional_data": os.path.splitext(os.path.basename(__file__))[0]
    job_data = {
        "additional_data": key_word,
        "title": title,
        "company": company_name,
        "posted_time": posted_time,
        "location": location,
        "job_link": job_link,
        "job_details": insight_text,
        "job_description": job_description,
        "matched_keywords": matched_keywords_str,
        "company_website": company_website,
        "employee_size": employee_size,
        "company_industry": company_industry,
        "company_city": company_city,
        "company_linkedin_url": company_linkedin_url,
        "poc_name": poc_name,
        "poc_profile_link": poc_link,
        "connection_degree": connection_degree,
        "poc_headline": headline
    }

    response = requests.post(WEB_APP_URL, json=job_data)
    # print("Response:", response.text)


def click_each_job_item():
    job_items = driver.find_elements(By.CSS_SELECTOR, '[data-occludable-job-id]')

    for job in job_items:
        # Check if the job has already been viewed
        try:
            viewed_label = job.find_element(By.CSS_SELECTOR,
                                            "li.job-card-container__footer-item.job-card-container__footer-job-state.t-bold")
            if "Viewed" in viewed_label.text:
                # print("Job already viewed. Skipping this job item.")
                continue  # Skip to the next job item
        except NoSuchElementException:
            # If the 'Viewed' label is not present, proceed to click the job
            pass

        # Extract the company name before clicking the job item
        try:
            company_element = job.find_element(By.CLASS_NAME, 'boAvmrAFfwZEHebYjctgTppwiEwazqIftEMU')
            company_name = company_element.text.strip()

            # Check if the company is in the fraud list (case insensitive)
            if company_name.lower() in [fraud_company.lower() for fraud_company in FRAUD_COMPANIES_LIST]:
                # print(f"Skipping job from fraudulent company: {company_name}")
                continue  # Skip this job and move to the next one

        except NoSuchElementException:
            pass
            # print("Company name element not found. Proceeding with caution...")

        wait_time = random.randint(2, 4)
        # print(f"Waiting for {wait_time} seconds before clicking the next job...")
        time.sleep(wait_time)
        # scroll_job_list()
        driver.execute_script("arguments[0].scrollIntoView(true);", job)

        try:
            job_link = job.find_element(By.CSS_SELECTOR, 'a.job-card-container__link')
            job_link.click()
            # print("Clicked job item and extracting the job details")
            extract_job_details(key_word)
        except (ElementNotInteractableException, NoSuchElementException):
            # print("Anchor element not clickable. Trying a different element...")
            # Try to click another element
            alternative_links = driver.find_elements(By.CSS_SELECTOR, 'a.job-card-container__link')
            if alternative_links:
                alternative_links[0].click()
                # print("Clicked an alternative job item and extracting the job details")
                extract_job_details(key_word)
            else:
                pass
                # print("No alternative job elements found.")


def get_job_listings():
    try:
        job_list_container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__list"))
        )
        # print("Job list container found.")

        job_list_items = job_list_container.find_elements(By.CSS_SELECTOR, "[data-occludable-job-id]")
        # print(f"Total number of job listings: {len(job_list_items)}")
        click_each_job_item()

    except TimeoutException as e:
        pass
        # print("Job list container not found or took too long to load.", str(e))
    except NoSuchElementException as e:
        pass
        # print("Error accessing job listing details.", str(e))
    except Exception as e:
        pass
        # print("An error occurred:", str(e))


def click_next_button(current_page):
    try:
        # First try to find the numbered page button
        next_page_label = f"Page {current_page + 1}"
        try:
            page_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@aria-label='{next_page_label}']"))
            )
            page_button.click()
            # print(f"Page button {next_page_label} clicked.")
            return True
        except TimeoutException:
            # If numbered page button not found, try the "View next page" button
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'View next page')]"))
            )
            next_button.click()
            # print(f"Next button for {next_page_label} clicked.")
            return True
    except TimeoutException:
        # print(f"No more pages available after page {current_page}.")
        return False


def iterate_pages(key_word):
    page = 1
    max_pages = MAX_NO_OF_PAGES_TO_POOL
    with tqdm(total=max_pages, desc="Extracting Pages...", ncols=100, colour="cyan") as pbar:
        while page <= max_pages:
            # print(f"Extracting jobs from page {page}")
            get_job_listings()

            if click_next_button(page):
                wait_time = random.randint(2, 3)
                # print(f"Waiting for {wait_time} seconds before moving to the next page...")
                time.sleep(wait_time)
                page += 1
                pbar.update(1)
            else:
                # print("No more pages. Extraction complete.")
                tqdm.write("✅ No more pages with keyword . Extraction complete.")
                if key_word == 'MERN':
                    key_word = 'ReactJS'
                    LINK = f'https://www.linkedin.com/jobs/search/?currentJobId=4304630441&f_E=1%2C2&f_TPR=r86400&keywords={str(key_word)}'
                    driver.get(LINK)
                    print(
                        f"No results found with keyword : MERN .So searching with keyword {key_word} and continuing the process")
                    iterate_pages(key_word)
                break


def send_email_with_attachment(filename):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL  # Sending to multiple recipients
        msg['Subject'] = f'Job Listings CSV File: {filename}'

        # Attach the body with the email (using MIMEText for the email body)
        body = "Attached is the CSV file containing the scraped job listings."
        msg.attach(MIMEText(body, 'plain'))  # Attach the body as plain text

        # Attach the CSV file
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(filename)}")
        msg.attach(part)

        # Establish SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Use TLS encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send the email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAILS, text)  # Send to all recipients in the list
        server.quit()

        # print(f"Email sent successfully to {', '.join(RECIPIENT_EMAILS)}")

    except Exception as e:
        pass
        # print(f"Error sending email: {e}")


def save_to_csv(filename='jobs_list.csv'):
    # Ensure the directory exists
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    script_name = os.path.splitext(os.path.basename(__file__))[0]

    # Append the current timestamp to the filename
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{script_name}_jobs_list_{timestamp}.csv'

    # Create the full file path
    file_path = os.path.join(OUTPUT_DIRECTORY, filename)

    # Save the CSV file to the specified path
    if jobs_list:
        keys = jobs_list[0].keys()
        with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(jobs_list)

        # print(f"Job List saved at {file_path}")
        send_email_with_attachment(file_path)
    else:
        pass
        # print("No job details to save.")


def main():
    try:
        driver.get("https://www.linkedin.com/login")
        try:
            USERNAME = "kotaharshita@gmail.com"
            PASSWORD = "Harshita123$"
            account_login(USERNAME=USERNAME, PASSWORD=PASSWORD)
        except Exception as e:
            print(e)
            USERNAME = "dakshayaniyellanki@gmail.com"
            PASSWORD = "#@292686@#"
            print(f'Using alternate credentials : {USERNAME}')
            account_login(USERNAME, PASSWORD)
        finally:
            print('Website not responding with current credentials')

        print("Successfully logged In...")
        # print(LINK)
        driver.get(LINK)
        iterate_pages(key_word)
    except Exception as e:
        pass

        # print(f"An error occurred during execution: {e}")
    finally:
        save_to_csv()
        driver.quit()


if __name__ == "__main__":
    main()
