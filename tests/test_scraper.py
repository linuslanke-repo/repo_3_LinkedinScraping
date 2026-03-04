# tests/test_scrapper.py

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from PYTHON import (
    should_skip_role,
    is_fraud_company,
    match_keywords,
    build_job_dict,
    save_to_csv,
    LinkedInJobScraper,
)


# =====================================================
# 1️⃣ PURE FUNCTION TESTS
# =====================================================

def test_should_skip_role():
    assert should_skip_role("Data Analyst") is True
    assert should_skip_role("Azure Developer") is True
    assert should_skip_role("Software Intern") is False


def test_is_fraud_company():
    assert is_fraud_company("Infosys") is True
    assert is_fraud_company("Random Startup") is False


def test_match_keywords():
    result = match_keywords(
        title="Intern Data Engineer",
        description="Entry Level position",
        company="ABC"
    )

    assert "Intern" in result or "Entry Level" in result


def test_build_job_dict():
    job = build_job_dict(
        keyword="Data Analyst",
        title="Intern",
        job_link="link",
        company_name="ABC",
        company_name_link="company_link",
        company_website="site",
        employee_size="100",
        company_industry="IT",
        company_city="Delhi",
        company_linkedin_url="linkedin",
        location="India",
        posted_time="1 day ago",
        insight_text="insight",
        job_description="description",
        poc_name="John",
        poc_link="profile",
        connection_degree="1st",
        headline="Hiring Manager"
    )

    assert isinstance(job, dict)
    assert job["Title"] == "Intern"
    assert "Scraped At" in job


# =====================================================
# 2️⃣ CSV SAVE TEST
# =====================================================

def test_save_to_csv_creates_file():
    sample_jobs = [
        {"Title": "Test", "Company": "ABC"}
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = save_to_csv(sample_jobs, tmpdir)

        assert os.path.exists(file_path)


# =====================================================
# 3️⃣ SCRAPER CLASS TEST (WITHOUT REAL SELENIUM)
# =====================================================

@patch("PYTHON.requests.post")
def test_scrape_page_appends_jobs(mock_post):
    # Create fake driver
    fake_driver = MagicMock()

    # Fake job card element
    fake_card = MagicMock()
    fake_driver.find_elements.return_value = [fake_card]

    # Create scraper instance
    scraper = LinkedInJobScraper(
        driver=fake_driver,
        username="user",
        password="pass",
        keyword="Data",
        max_pages=1,
        webhook_url="http://fake-url"
    )

    # Mock extract_current_job to avoid Selenium calls
    scraper.extract_current_job = MagicMock(return_value={"Title": "Test Job"})

    scraper.scrape_page()

    assert len(scraper.jobs) == 1
    mock_post.assert_called_once()


# =====================================================
# 4️⃣ FULL SCRAPE LOOP TEST (NO REAL BROWSER)
# =====================================================

def test_scrape_loop():
    fake_driver = MagicMock()

    scraper = LinkedInJobScraper(
        driver=fake_driver,
        username="user",
        password="pass",
        keyword="Data",
        max_pages=3,
        webhook_url=None
    )

    scraper.scrape_page = MagicMock()

    scraper.scrape()

    assert scraper.scrape_page.call_count == 3