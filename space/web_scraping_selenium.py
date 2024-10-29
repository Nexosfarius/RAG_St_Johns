from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from langchain.document_loaders import TextLoader
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# List of URLs to crawl
urls = [
     "https://www.stjohns.edu/who-we-are/faith-and-mission",
    "https://www.stjohns.edu/equity-and-inclusion",
    "https://www.stjohns.edu/who-we-are/leadership-and-administration",
    "https://www.stjohns.edu/who-we-are/history-and-facts",
    "https://www.stjohns.edu/who-we-are/campus-sustainability",
    "https://www.stjohns.edu/who-we-are/student-consumer-information",
    "https://www.stjohns.edu/who-we-are/public-safety",
    "https://www.stjohns.edu/who-we-are/title-ix",
    # Add all the new URLs here
    "https://www.stjohns.edu/",
    "https://www.stjohns.edu/#block-menu-block-main",
    "https://www.stjohns.edu/#main-content",
    "https://www.stjohns.edu/st-johns-university-news-media",
    "https://www.stjohns.edu/events",
    "https://www.stjohns.edu/st-johns-university-alumni-friends",
    "https://www.stjohns.edu/st-johns-university-athletics",
    "https://www.stjohns.edu/offices-departments",
    "https://www.stjohns.edu/welcome-future-johnnies",
    "https://www.stjohns.edu/my-st-johns-current-students",
    "https://www.stjohns.edu/life-st-johns/st-johns-university-parent-and-family-connections",
    "https://www.stjohns.edu/my-st-johns-faculty-administrators-and-staff",
    "https://www.stjohns.edu/academics",
    "https://www.stjohns.edu/academics/build-your-st-johns-pathway-based-what-drives-you",
    "https://www.stjohns.edu/academics/programs",
    "https://www.stjohns.edu/academics/schools",
    "https://www.stjohns.edu/academics/study-abroad-global-programs",
    "https://www.stjohns.edu/libraries",
    "https://www.stjohns.edu/academics/st-johns-university-research-programs-and-opportunities",
    "https://www.stjohns.edu/academics/faculty",
    "https://www.stjohns.edu/academics/centers-institutes",
    "https://www.stjohns.edu/academics/academic-resources-and-programs",
    "https://www.stjohns.edu/academics/university-course-offerings",
    "https://www.stjohns.edu/academics/office-registrar",
    "https://www.stjohns.edu/admission",
    "https://www.stjohns.edu/admission/undergraduate-admission",
    "https://www.stjohns.edu/admission/graduate-admission",
    "https://www.stjohns.edu/admission/international-admission",
    "https://www.stjohns.edu/admission/st-johns-welcomes-transfer-students",
    "https://www.stjohns.edu/admission/visiting-students",
    "https://www.stjohns.edu/admission/tuition-and-financial-aid",
    "https://www.stjohns.edu/admission/scholarships",
    "https://www.stjohns.edu/admission/other-programs",
    "https://www.stjohns.edu/admission/connect-us",
    "https://www.stjohns.edu/life-st-johns",
    "https://www.stjohns.edu/life-st-johns/new-york-locations",
    "https://www.stjohns.edu/life-st-johns/global-locations",
    "https://www.stjohns.edu/life-st-johns/career-development",
    "https://www.stjohns.edu/life-st-johns/health-and-wellness",
    "https://www.stjohns.edu/life-st-johns/student-success",
    "https://www.stjohns.edu/who-we-are",
    "https://www.stjohns.edu/who-we-are/faith-and-mission",
    "https://www.stjohns.edu/equity-and-inclusion",
    "https://www.stjohns.edu/who-we-are/leadership-and-administration",
    "https://www.stjohns.edu/who-we-are/history-and-facts",
    "https://www.stjohns.edu/who-we-are/campus-sustainability",
    "https://www.stjohns.edu/who-we-are/student-consumer-information",
    "https://www.stjohns.edu/who-we-are/public-safety",
    "https://www.stjohns.edu/who-we-are/title-ix",
    "https://www.stjohns.edu/academics/programs/childhood-special-education-1-6-bachelor-science-education-master-science-education",
    "https://www.stjohns.edu/about/leadership-and-administration/office-president/presidents-society",
    "https://www.stjohns.edu/about/faith-and-mission/campus-ministry/leadership-and-development/catholic-scholars"
]

# Initialize Selenium WebDriver with Service
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# File to save the extracted text
output_file = "stjohns_content.txt"

with open(output_file, "w") as file:
    for url in urls:
        # Navigate to the page
        driver.get(url)
        time.sleep(2)  # Allow the page to load completely

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract text content and clean it up
        text_content = soup.get_text(separator="\n", strip=True)

        # Write the clean text content to the file
        file.write(f"URL: {url}\n\n")
        file.write(text_content)
        file.write("\n\n" + "=" * 80 + "\n\n")

# Close the WebDriver
driver.quit()