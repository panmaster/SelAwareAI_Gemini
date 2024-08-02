from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time

#  ---  Function to get links  ---
def get_tusksearch_links(search_phrase, num_pages=1, forbidden_phrases=[]):
    """
    Retrieves TUSK Search result links, navigating through multiple pages
    and filtering out links containing forbidden phrases.

    Args:
        search_phrase (str): The search query to use.
        num_pages (int): The number of result pages to scrape.
        forbidden_phrases (list): A list of phrases to exclude from the results.

    Returns:
        set: A set of unique links from the TUSK Search results.
    """

    def perform_search(driver):
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
        )
        search_input.clear()
        search_input.send_keys(search_phrase)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button.search-button")
        submit_button.click()

    def get_search_result_links(driver):
        try:
            # Wait for the result cards to appear
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.result-card"))
            )

            # Extract links from each result card
            result_cards = driver.find_elements(By.CSS_SELECTOR, "div.result-card")
            links = []
            for card in result_cards:
                link_element = card.find_element(By.CSS_SELECTOR, ".result-title a.title")
                link = link_element.get_attribute("href")
                links.append(link)
            return links

        except TimeoutException:
            print("TimeoutException occurred while waiting for search result links.")
            return []

    def crawl_to_bottom(driver):
        """Scrolls to the bottom of the page slowly."""
        scroll_pause_time = 0.5  # You can adjust this value
        screen_height = driver.execute_script("return window.innerHeight")
        i = 1

        while True:
            # Scroll one screen height each time
            driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
            i += 1
            time.sleep(scroll_pause_time)

            # Update scroll height each time after scrolled, as the scroll height can be increased
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            if (screen_height * i) > scroll_height:
                break

    # Create a ChromeDriver instance with options
    options = Options()

    # options.add_argument("--headless=new")  # Uncomment for headless mode
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(options=options)

    # Navigate to TUSK Search
    url = "https://tusksearch.com/"
    driver.get(url)

    # Perform initial search
    perform_search(driver)

    all_links = []
    for page in range(num_pages):
        print(f"Scraping page {page + 1}")
        crawl_to_bottom(driver)  # Scroll to bottom to load all results
        all_links.extend(get_search_result_links(driver))

        if page < num_pages - 1:  # Avoid clicking "Next" on the last page
            try:
                # Find the "Next" page button and click it using JavaScript
                next_page_button = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"tusk-navigation-pager li:nth-child({page + 2}) span"))
                )
                driver.execute_script("arguments[0].click();", next_page_button)
                time.sleep(2)  # Wait for the next page to load
            except TimeoutException:
                print("No more pages found.")
                break
            except NoSuchElementException:
                print("No more pages found (Next button not found).")
                break

    # Filter out links containing forbidden phrases
    filtered_links = set(
        filter(lambda link: not any(phrase.lower() in link.lower() for phrase in forbidden_phrases), all_links))

    # Print the filtered links
    for link in filtered_links:
        print(f"Link: {link}")

    driver.quit()

    return filtered_links

#  ---  Example usage of the function  ---
tool_type_for_TOOL_MANAGER = "os" 

search_phrase = "web scraping python"
num_pages = 3
forbidden_phrases = ["wikipedia.org"]

links = get_tusksearch_links(search_phrase, num_pages, forbidden_phrases)

print(f"Found a total of {len(links)} links.")