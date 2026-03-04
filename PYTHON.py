
import os
import csv
import time
import random
import logging
from datetime import datetime
from typing import List, Dict, Optional

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)
from webdriver_manager.chrome import ChromeDriverManager


# =========================
# CONFIGURATION
# =========================

KEYWORDS = ["Entry Level", "Intern", "Internship", "0-1", "0-2", "0-3"]

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

DEFAULT_MAX_PAGES = 10
WEB_APP_URL="https://script.google.com/macros/s/AKfycbw_G1iVzFqdGNcaeTIg59uPhUPerf5m0bawyBmjEW51mymYoP1V6LNfCLNFRy6L5qQhXA/exec"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# =========================
# DRIVER FACTORY
# =========================

def create_driver(headless: bool = False) -> webdriver.Chrome:
    """Create and return a Chrome WebDriver instance."""

    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--window-position=-3000,0")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    return driver


# =========================
# PURE LOGIC FUNCTIONS (TESTABLE)
# =========================

def should_skip_role(title: str) -> bool:
    if not title:
        return True

    return any(role.lower() in title.lower() for role in SKIP_ROLE_NAMES)


def is_fraud_company(company: str) -> bool:
    if not company:
        return True

    fraud_list = [c.lower() for c in FRAUD_COMPANIES_LIST]
    return company.lower() in fraud_list


def match_keywords(title: str, description: str, company: str) -> str:
    combined = f"{title} {description} {company}".lower()

    matched = [
        keyword for keyword in KEYWORDS
        if keyword.lower() in combined
    ]

    return ", ".join(matched) if matched else "None"

keyword = os.getenv("JOB_KEYWORD", "Data Analyst")
def build_job_dict(
    keyword: str ,
    title: str,
    job_link : str,
    company_name: str,
    company_name_link: str,
    company_website: str,
    employee_size: str,
    company_industry: str,
    company_city: str,
    company_linkedin_url: str,
    location : str,
    posted_time : str,
    insight_text : str,
    job_description : str,
    poc_name : str,
    poc_link : str,
    connection_degree : str,
    headline : str
) -> Dict:

    return {
        "additional_data": keyword,
        "Title": title or "NA",
        "Company": company_name or "NA",
        "posted_time": posted_time or "NA",
        "Location": location or "NA",
        "Job Link": job_link or "NA",
        "job_details": insight_text or "NA",
        "Description": job_description or "NA",
        "Matched Keywords": match_keywords(title, job_description, company_name) ,
        "company_website": company_website or "NA",
        "employee_size": employee_size or "NA",
        "company_industry": company_industry or "NA",
        "company_city": company_city or "NA",
        "company_linkedin_url": company_linkedin_url or "NA",
        "poc_name": poc_name or "NA",
        "poc_profile_link": poc_link or "NA",
        "connection_degree": connection_degree or "NA",
        "poc_headline": headline or "NA",
        "Scraped At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# =========================
# SCRAPER CLASS
# =========================

class LinkedInJobScraper:

    def __init__(
        self,
        driver: webdriver.Chrome,
        username: str,
        password: str,
        keyword: str,
        max_pages: int = DEFAULT_MAX_PAGES,
        webhook_url: str = WEB_APP_URL,
        # webhook_url: Optional[str] = None,
    ):
        self.driver = driver
        self.username = username
        self.password = password
        self.keyword = keyword
        self.max_pages = max_pages
        self.webhook_url = webhook_url
        self.jobs: List[Dict] = []

    # ---------------------

    def login(self) -> None:
        logger.info("Logging into LinkedIn...")

        self.driver.get("https://www.linkedin.com/login")

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        time.sleep(1)
        # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[4]/button').click()

        logger.info("Login submitted.")

    # ---------------------

    def open_jobs_page(self) -> None:
        url = (f"https://www.linkedin.com/jobs/search/?currentJobId=4304630441&f_E=1%2C2&f_TPR=r86400&keywords={self.keyword}")
        self.driver.get(url)
        logger.info(f"Opened jobs page for keyword: {self.keyword}")

    # ---------------------

    def extract_current_job(self) -> Optional[Dict]:
        location = posted_time = insight_text = job_description = "NA"
        company_website = employee_size = company_industry = company_city = company_linkedin_url = "NA"
        time.sleep(random.uniform(1, 2))

        try:
            title = self.driver.find_element(
                By.CSS_SELECTOR, "h1"
            ).text
        except NoSuchElementException:
            return None

        if should_skip_role(title):
            return None
        try:
            job_title_element =self.driver.find_element(By.CSS_SELECTOR,"div.t-24.job-details-jobs-unified-top-card__job-title h1 a")
            job_link = job_title_element.get_attribute("href")
        except:
            job_link ="NA"
        try:
            company_name_element = self.driver.find_element(By.CLASS_NAME,
                                                               "job-details-jobs-unified-top-card__company-name")
            company_name_link = company_name_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            company_name = company_name_element.text
        except NoSuchElementException:
            company_name = "NA"
            company_name_link ="NA"
        if is_fraud_company(company_name):
            return None
        # Extract POC (Point of Contact) details
        try:
            # Check if hiring team section exists using a more reliable method
            hiring_team_sections = self.driver.find_elements(By.TAG_NAME, "h2")
            hiring_team_section = None
            for section in hiring_team_sections:
                if "Meet the hiring team" in section.text:
                    hiring_team_section = section
                    break

            if hiring_team_section:
                # Extract POC name and profile link
                try:
                    poc_element = self.driver.find_element(By.CSS_SELECTOR, "span.jobs-poster__name strong")
                    poc_name = poc_element.text.strip()

                    # Get the parent anchor tag for the profile link
                    poc_link = poc_element.find_element(By.XPATH, "./ancestor::a").get_attribute("href")
                except:
                    poc_name = "NA"
                    poc_link = "NA"

                # Extract connection degree
                try:
                    connection_degree_element = self.driver.find_element(By.CSS_SELECTOR,
                                                                    "span.hirer-card__connection-degree")
                    connection_degree = connection_degree_element.text.strip()
                except:
                    connection_degree = "NA"

                # Extract headline
                try:
                    headline_element = self.driver.find_element(By.CSS_SELECTOR, "div.text-body-small")
                    headline = headline_element.text.strip()
                except:
                    headline = "NA"
            else:
                # print("Hiring team section not found.")
                poc_name = "NA"
                poc_link = "NA"
                connection_degree = "NA"
                headline = "NA"

        except:
            poc_name = "NA"
            poc_link = "NA"
            connection_degree = "NA"
            headline = "NA"
        # Modify the URL to point to the 'About' page (replace 'life' with 'about')
        if company_name_link != "NA":
            company_about_url = company_name_link.replace("/life", "/about")
            # print(f"Company About URL: {company_about_url}")

            # Open the About page in a new tab
            self.driver.execute_script(f"window.open('{company_about_url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])  # Switch to the new tab

            # Extract Company Website from the About page
            try:
                website_element = self.driver.find_element(By.CSS_SELECTOR, "dd.mb4.t-black--light.text-body-medium a")
                company_website = website_element.get_attribute("href")
            except:
                company_website = "NA"

            # Extract Employee Size from the About page
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, "dd.t-black--light.mb4.text-body-medium a span")
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
                info_items = self.driver.find_elements(By.CLASS_NAME, "org-top-card-summary-info-list__info-item")
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
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])  # Switch back to the original tab
        else:
            company_website = "NA"
            # Extract Location and Posted Time
            try:
                primary_description_container = self.driver.find_element(By.CLASS_NAME,
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
                job_insight_element = self.driver.find_element(By.CLASS_NAME, "job-details-fit-level-preferences")
                insight_text = job_insight_element.text.strip()
            except NoSuchElementException:
                insight_text = "NA"

            # Extract Job Description
            try:
                job_description_element = self.driver.find_element(By.CSS_SELECTOR,
                                                              "div.jobs-box__html-content.jobs-description-content__text--stretch")
                job_description = job_description_element.text.strip()
            except:
                job_description = "NA"
        job_data = build_job_dict(
            keyword,title,job_link,company_name,company_name_link,company_website,employee_size,company_industry,company_city,
            company_linkedin_url,location,posted_time,insight_text,job_description,poc_name,poc_link,connection_degree,headline)

        return job_data

    # ---------------------

    def scrape_page(self) -> None:
        time.sleep(3)
        job_cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            "[data-occludable-job-id]"
        )
        time.sleep(2)
        for card in job_cards:
            try:
                card.click()
                time.sleep(2)
                job_data = self.extract_current_job()

                if job_data:
                    self.jobs.append(job_data)

                    if self.webhook_url:
                        requests.post(self.webhook_url, json=job_data)

            except ElementNotInteractableException:
                continue

    # ---------------------

    def scrape(self) -> List[Dict]:

        for page in range(self.max_pages):
            logger.info(f"Scraping page {page + 1}")
            self.scrape_page()

        return self.jobs


# =========================
# CSV SAVE FUNCTION
# =========================

def save_to_csv(jobs: List[Dict], output_dir: str) -> str:

    if not jobs:
        raise ValueError("No jobs to save.")

    os.makedirs(output_dir, exist_ok=True)

    filename = f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.join(output_dir, filename)

    keys = jobs[0].keys()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(jobs)

    logger.info(f"Saved CSV to {file_path}")
    return file_path


# =========================
# MAIN ENTRY
# =========================

def main():

    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    keyword = os.getenv("JOB_KEYWORD", "Data Analyst")
    output_dir = os.getenv("OUTPUT_DIR", r"C:\Users\linus\Downloads\LinkedIN")

    if not username or not password:
        raise ValueError("Missing LinkedIn credentials in environment variables.")

    driver = create_driver(headless=True)

    try:
        scraper = LinkedInJobScraper(
            driver=driver,
            username=username,
            password=password,
            keyword=keyword,
            max_pages=10,
        )

        scraper.login()
        scraper.open_jobs_page()
        jobs = scraper.scrape()

        if jobs:
            save_to_csv(jobs, output_dir)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()