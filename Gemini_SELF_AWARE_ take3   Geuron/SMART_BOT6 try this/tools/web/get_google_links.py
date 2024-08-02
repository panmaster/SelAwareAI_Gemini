tool_type_for_TOOL_MANAGER="os"
get_google_search_links_short_description="""  Retrieves Google search result links with the option to disable safe search,
    navigate through multiple pages, and filter out links containing forbidden phrases. """

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

def get_google_search_links(search_phrase, num_pages=1, forbidden_phrases=[], safe_search=False):
    """
    Retrieves Google search result links with the option to disable safe search,
    navigate through multiple pages, and filter out links containing forbidden phrases.

    Args:
        search_phrase (str): The search query to use.
        num_pages (int): The number of pages to navigate through.
        forbidden_phrases (list): A list of phrases to exclude from the results.
        safe_search (bool): Whether to enable safe search (default: False).

    Returns:
        set: A set of unique links from the Google search results.
    """

    def perform_search(driver):
        search_input = driver.find_element(By.NAME, "q")
        search_input.send_keys(search_phrase)
        search_input.submit()

    def set_safe_search_off(driver):
        if not safe_search:
            try:
                # Click the Safe Search dropdown button (if it exists)
                safe_search_dropdown_button = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown--safe-search .dropdown__button.js-dropdown-button"))
                )
                safe_search_dropdown_button.click()

                # Find the "Safe Search: Off" option and click it
                safe_search_off_option = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal--dropdown--safe-search a[data-value='-2']"))
                )
                safe_search_off_option.click()

            except TimeoutException:
                print("Safe Search dropdown not found (may already be off).")

    def get_search_result_links(driver):
        try:
            # Wait for search results to be visible
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#search .g"))
            )
            search_results = driver.find_elements(By.CSS_SELECTOR, "#search .g a[href]")
            links = [link.get_attribute("href") for link in search_results]
            return links
        except TimeoutException:
            print("TimeoutException occurred while waiting for search result links.")
            return []

    # Create a ChromeDriver instance with custom preferences
    options = Options()
    options.add_argument("--disable-search-engine-choice-screen")

    driver = webdriver.Chrome(options=options)

    # Navigate to Google
    url = "https://www.google.com/"
    driver.get(url)

    # Click "Accept All" button
    try:
        accept_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "L2AGLb"))
        )
        accept_all_button.click()
    except TimeoutException:
        print("Could not find the 'Accept All' button.")

    # Perform initial search
    perform_search(driver)

    # Wait for the first result to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#search .g"))
    )

    # Disable safe search if requested
    set_safe_search_off(driver)

    all_links = []
    # Navigate through the pages
    for page in range(num_pages):
        print(f"Scraping page {page+1}")
        # Get links from the current page
        all_links.extend(get_search_result_links(driver))

        # Go to the next page
        try:
            next_page_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.ID, "pnnext"))
            )
            next_page_button.click()
        except TimeoutException:
            print("No more pages found.")
            break

    # Filter the links
    filtered_links = set(filter(lambda link: link.startswith("http") and not any(phrase.lower() in link.lower() for phrase in forbidden_phrases), all_links))

    # Print the links
    for link in filtered_links:
        print(f"Link: {link}")

    driver.quit()

    return filtered_links

# Example usage
search_phrase = "dragon ball"
num_pages = 3  # Navigate through 3 result pages
forbidden_phrases = ["phrase1", "phrase2"]
safe_search = False

links = get_google_search_links(search_phrase, num_pages, forbidden_phrases, safe_search)

print(f"Found {len(links)} links in total.")