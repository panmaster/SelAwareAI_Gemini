tool_type_for_TOOL_MANAGER="all"


get_duckduckgo_links_short_description="""Retrieves DuckDuckGo search result links with the option to disable safe search
    and scroll through 'More Results'"""


def get_duckduckgo_links(search_phrase, num_more_results=0):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    """
    Retrieves DuckDuckGo search result links with the option to disable safe search
    and scroll through 'More Results'.

    Args:
        search_phrase (str): The search query to use.
        num_more_results (int): The number of times to click the 'More Results' button.

    Returns:
        set: A set of unique links from the DuckDuckGo search results.
    """
    def perform_search(driver):
        search_input = driver.find_element(By.NAME, "q")
        search_input.send_keys(search_phrase)
        search_input.submit()

    def set_safe_search_off(driver):
        try:
            # Click the Safe Search dropdown button
            safe_search_dropdown_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown--safe-search .dropdown__button.js-dropdown-button"))
            )
            safe_search_dropdown_button.click()

            # Find the "Safe Search: Off" option and click it
            safe_search_off_option = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal--dropdown--safe-search a[data-value='-2']"))
            )
            safe_search_off_option.click()

            # Click outside the dropdown menu to close it
            overlay = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal__overlay.js-modal-close"))
            )
            overlay.click()

        except TimeoutException:
            print("TimeoutException occurred while setting safe search off..")

    def get_search_result_links(driver):
        try:
            search_results = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href]"))
            )
            # Filter links to exclude those containing "duckduckgo"
            links = [link.get_attribute("href") for link in search_results if "duckduckgo" not in link.get_attribute("href")]
            return links
        except TimeoutException:
            print("TimeoutException occurred while waiting for search result links.")
            return []

    # Create a ChromeDriver instance
    driver = webdriver.Chrome()

    # Navigate to DuckDuckGo
    url = "https://duckduckgo.com/"
    driver.get(url)

    # Perform initial search (safe search might be on by default)
    perform_search(driver)

    # Disable safe search
    set_safe_search_off(driver)

    # Perform search again with safe search off
    perform_search(driver)

    # Scroll through 'More Results' if requested
    for _ in range(num_more_results):
        try:
            more_results_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.ID, "more-results"))
            )
            more_results_button.click()
        except TimeoutException:
            print("Failed to click the 'More Results' button.")

    # Get and filter the links
    links = get_search_result_links(driver)
    filtered_links = set(filter(lambda link: link.startswith("http"), links))

    # Print the links (optional)
    for link in filtered_links:
        print(f"Link: {link}")

    driver.quit()

    return filtered_links