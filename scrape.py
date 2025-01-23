from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup

SBR_WEBDRIVER = "https://brd-customer-hl_ffc05b9b-zone-ai_scraper:kpg45guzxxid@brd.superproxy.io:9515"

def scrape_website(website):
    try:
        print("Launching Chrome browser...")

        # Initialize ChromeOptions
        options = ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")  # Disable GPU acceleration
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--disable-dev-shm-usage")  # Overcome resource limits

        # Connect to the remote WebDriver
        with Remote(command_executor=SBR_WEBDRIVER, options=options) as driver:
            driver.get(website)

            # Placeholder for CAPTCHA handling
            print("Waiting for CAPTCHA to solve...")
            # Implement CAPTCHA handling here if needed

            print("Navigated! Scraping page content...")
            html = driver.page_source
            return html  # Return the scraped HTML

    except WebDriverException as e:
        print(f"Error occurred: {e}")
        return None
    finally:
        print("Scraping completed.")

def extract_body_content(html_content):

    #checks if html content is not of type str OR contains only whitespaces :
    #strip remove the whitespace
    #if the value is true a valueerror is raised

    if not isinstance(html_content, str) or not html_content.strip():
        raise ValueError("Invalid or empty HTML content provided.")
    
    #html.parser is a bulit-in parser : parses html content in tree structure.
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body #extract body element of prased html content
        return str(body_content).strip() if body_content else "" # if found return striped string else return empty string
    except Exception as e: # if invalid html content or errors it raises a Runtimeerrors
        raise RuntimeError(f"Error while parsing HTML: {str(e)}")

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove <script> and <style> elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Extract and clean text
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    # Split content into chunks of max_length
    return [
        dom_content[i: i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]
