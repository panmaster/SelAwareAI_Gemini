tool_type_for_TOOL_MANAGER="all"


scrape_web_short_description=""" scrapes web. 
        """



import json
import urllib
from googlesearch import search
import random
import requests
from requests.exceptions import SSLError, TimeoutException
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import socket
import datetime

# Global variables for storing gathered data
SetUrlsGlobal = set()
SetLinksGlobal = set()
SetImagesGlobal = set()

# Default configuration
DEFAULT_CONFIG = {
    "source": "google",
    "query": None,
    "initial_processing_method": "random",
    "initial_filtering_phrases": [],
    "excluded_phrases": [],
    "image_extraction_method": "selenium",
    "save_structure": "folder",  # Options: 'folder', 'flat', 'json'
    "save_path": "scraped_data",
    "max_depth": 3,
    "rate_limit": 1,  # Seconds between requests
}


def scrape_web(source=None, query=None, initial_processing_method=None, initial_filtering_phrases=[],
               excluded_phrases=[], image_extraction_method=None, save_structure=None, save_path=None, max_depth=None,
               rate_limit=None):
    """

    The main function to scrape the web.

    This function orchestrates the entire web scraping process, from obtaining initial links to saving extracted data. It utilizes various methods for search, link processing, filtering, image extraction, and data storage, providing a comprehensive and customizable solution.

    Args:
        source (str, optional): The search engine to use for obtaining initial links ("google" or "duckduckgo"). Defaults to None, which will use the value specified in `DEFAULT_CONFIG`.
        query (str, optional): The search query to use for retrieving initial links. Defaults to None, which will use the value specified in `DEFAULT_CONFIG`.
        initial_processing_method (str, optional): The method to process the initial set of links ("random", "switch", "random_number"). Defaults to None, which will use the value specified in `DEFAULT_CONFIG`.
        initial_filtering_phrases (list, optional): A list of phrases that links should contain to be included in the initial set. Defaults to [], which will use the value specified in `DEFAULT_CONFIG`.
        excluded_phrases (list, optional): A list of phrases that should be excluded from links and images during crawling. Defaults to [], which will use the value specified in `DEFAULT_CONFIG`.
        image_extraction_method (str, optional): The method to extract images ("selenium" or "bs4"). Defaults to None, which will use the value specified in `DEFAULT_CONFIG`.
        save_structure (str, optional): The structure to save the scraped data ("folder", "flat", "json"). Defaults to None, which will use the value specified in `DEFAULT_CONFIG`.
        save_path (str, optional): The directory where the scraped data will be saved. Defaults to None, which will use the value specified in `DEFAULT_CONFIG`.
        max_depth (int, optional): The maximum number of levels to crawl (starting from the initial links). Defaults to None, which will use the value specified in `DEFAULT_CONFIG`.
        rate_limit (int, optional): The delay in seconds between requests to avoid overloading the target website. Defaults to None, which will use the value specified in `DEFAULT_CONFIG`.

    Returns:
        None: This function does not return a value but performs the web scraping process.
    """


    def resolve_ip_address(url):
        """Resolves the IP address of a given URL."""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        try:
            ip_address = socket.gethostbyname(domain)
            return ip_address
        except socket.gaierror:
            return None

    def filter_link(link, excluded_phrases):
        """Filters a link based on excluded phrases and image extensions."""
        image_extensions = [".jpeg", ".jpg", ".gif", ".png"]

        # Exclude image links
        for extension in image_extensions:
            if link.endswith(extension):
                return False

        # Exclude links containing excluded phrases
        for phrase in excluded_phrases:
            if phrase.lower() in link.lower():
                return False

        return True

    def process_initial_set(resultSet, method="random"):
        """Processes the initial set of links based on the chosen method."""
        finalSet = resultSet.copy()
        if method == "random":
            finalSet = set(random.sample(finalSet, len(finalSet)))
        elif method == "switch":
            finalSet = set(list(finalSet)[::-1])
        elif method == "random_number":
            num_to_keep = int(input("Enter the number of entries to keep: "))
            finalSet = set(random.sample(finalSet, num_to_keep))
        return finalSet

    def get_initial_links(source="google", query=None):
        """Retrieves initial links from Google or DuckDuckGo."""
        initialLinks = set()

        if source == "google":
            if query is None:
                print("Please provide a search query for Google.")
                return initialLinks
            num_results = int(input("Enter the number of links to obtain from Google: "))
            search_results = search(query, num_results=num_results)
            initialLinks = set(search_results)
        elif source == "duckduckgo":
            driver = webdriver.Chrome()
            driver.get("https://duckduckgo.com/")

            def perform_search(driver, search_phrase):
                search_input = driver.find_element(By.NAME, "q")
                search_input.send_keys(search_phrase)
                search_input.submit()

            def get_search_result_links(driver):
                try:
                    # Wait for the search results container to be present (adjust the selector if needed)
                    results_container = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "search-results"))
                    )

                    # Then, wait for links within the container to appear:
                    search_results = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#search-results a[href]"))
                    )
                    links = [
                        link.get_attribute("href")
                        for link in search_results
                        if "duckduckgo" not in link.get_attribute("href")
                    ]
                    return links
                except TimeoutException:
                    print("Timeout waiting for search results. Proceeding with an empty link list.")
                    return []

            search_phrase = input("Enter DuckDuckGo search phrase: ")
            num_more_results = int(input("Number of 'More Results' scrolls: "))
            perform_search(driver, search_phrase)

            while num_more_results > 0:
                try:
                    num_more_results -= 1
                    more_results_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.ID, "more-results"))
                    )
                    more_results_button.click()
                except:
                    print("Failed to click the 'More Results' button.")
                    print(num_more_results)

            initialLinks = set(get_search_result_links(driver))
            driver.quit()
        else:
            print("Invalid source specified. Please use 'google' or 'duckduckgo'.")

        return initialLinks

    def filter_initial_links(initialLinks, phrases):
        """Filters initial links based on user-provided phrases."""
        filtered_links = set()
        if phrases:
            filtered_links = {
                link for link in initialLinks if any(phrase in link for phrase in phrases)
            }
        else:
            filtered_links = initialLinks
        return filtered_links

    def crawl_links(
            starting_links,
            visited_links=None,
            layer=None,
            excluded_phrases=None,
            image_extraction_method="selenium",
            config=DEFAULT_CONFIG,
    ):
        """Crawls links and extracts data based on provided parameters."""
        if visited_links is None:
            visited_links = set()

        for link in starting_links:
            if link not in visited_links:
                print(f"Crawling link: {link}")
                try:
                    response = requests.get(link)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    soup = BeautifulSoup(response.text, "html.parser")
                    ip_address = resolve_ip_address(link)

                    new_links = set()
                    images = set()

                    # Image extraction
                    if image_extraction_method == "selenium":
                        images = extract_images_selenium(link, soup)
                    elif image_extraction_method == "bs4":
                        images = extract_images_bs4(link, soup)
                    else:
                        print(
                            "Invalid image extraction method. Please use 'selenium' or 'bs4'."
                        )

                    # Link extraction
                    for tag in soup.find_all(["a", "img", "ul", "li", "div", "body"]):
                        if tag.name == "a":
                            href = tag.get("href")
                        elif tag.name == "img":
                            href = tag.get("src")
                        elif tag.name in ["ul", "li", "div", "body"]:
                            href = tag.get("data-href")  # Adjust attribute if needed
                        if href and href.startswith("http"):
                            if filter_link(href, excluded_phrases):
                                new_links.add(href)
                                if href not in visited_links:
                                    save_data(
                                        href,
                                        ip_address,
                                        layer,
                                        "links",
                                        config,
                                    )
                        else:
                            full_link = urljoin(str(link), str(href))
                            if full_link.startswith("http") and filter_link(
                                    full_link, excluded_phrases
                            ):
                                new_links.add(full_link)
                                if full_link not in visited_links:
                                    save_data(
                                        full_link,
                                        ip_address,
                                        layer,
                                        "links",
                                        config,
                                    )

                    # Save extracted images
                    if images:
                        for image_link in images:
                            save_data(
                                image_link, None, layer, "images", config
                            )

                    # Recursively crawl new links
                    if layer is not None and layer < config["max_depth"]:
                        crawl_links(
                            new_links,
                            visited_links,
                            layer + 1,
                            excluded_phrases,
                            image_extraction_method,
                            config,
                        )
                    time.sleep(config["rate_limit"])
                except requests.exceptions.RequestException as e:
                    print(f"Error crawling link: {link}, reason: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                finally:
                    visited_links.add(link)
            else:
                print(f"Link {link} has already been visited.")

    def extract_images_selenium(link, soup):
        """Extracts image links using Selenium."""
        images = set()
        try:
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get(link)

            # Wait for page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Extract image links
            for tag in driver.find_elements(By.XPATH, "//img"):
                image_url = tag.get_attribute("src")
                if image_url and image_url.startswith("http"):
                    alt_description = tag.get_attribute("alt")
                    image_source = "src"
                    formatted_image_link = f"{image_url} ****** {alt_description} ****** {image_source}"
                    images.add(formatted_image_link)

            driver.quit()

        except TimeoutException as e:
            print(f"Timeout waiting for image elements on {link}: {e}")
        except Exception as e:
            print(f"Error extracting images using Selenium: {e}")

        return images

    def extract_images_bs4(link, soup):
        """Extracts image links using Beautiful Soup."""
        images = set()
        body = soup.find("body")
        if body is not None:
            body_tags = body.find_all()
            for tag in body_tags:
                if tag.name == "img":
                    if tag.has_attr("src") or tag.has_attr("data-src"):
                        image_url = None
                        image_source = None

                        if tag.has_attr("src"):
                            src = tag["src"].lower()
                            if (
                                    src.endswith(".jpg")
                                    or src.endswith(".jpeg")
                                    or src.endswith(".png")
                                    or re.search(r"\.(jpg|jpeg|png)\?.+", src)
                            ):
                                image_url = urljoin(link, tag["src"])
                                image_source = "src"

                        if tag.has_attr("data-src"):
                            data_src = tag["data-src"].lower()
                            if (
                                    data_src.endswith(".jpg")
                                    or data_src.endswith(".jpeg")
                                    or data_src.endswith(".png")
                                    or re.search(r"\.(jpg|jpeg|png)\?.+", data_src)
                            ):
                                image_url = urljoin(link, tag["data-src"])
                                image_source = "data-src"

                        if image_url is not None:
                            alt_description = tag.get("alt", "NoDescription")
                            formatted_image_link = f"{image_url} ****** {alt_description} ****** {image_source}"
                            images.add(formatted_image_link)

                if tag.name == "a" and tag.has_attr("href"):
                    href = tag["href"].lower()
                    if (
                            href.endswith(".jpg")
                            or href.endswith(".jpeg")
                            or href.endswith(".png")
                            or re.search(r"\.(jpg|jpeg|png)\?.+", href)
                    ):
                        image_url = urljoin(link, tag["href"])
                        alt_description = tag.get("alt", "NoDescription")
                        image_source = "href"
                        formatted_image_link = f"{image_url} ****** {alt_description} ****** {image_source}"
                        images.add(formatted_image_link)
        return images

    def save_data(data, ip_address, layer, data_type, config):
        """Saves extracted data based on the chosen save structure."""
        if config["save_structure"] == "folder":
            save_to_folder(data, ip_address, layer, data_type, config)
        elif config["save_structure"] == "flat":
            save_to_flat(data, ip_address, layer, data_type, config)
        elif config["save_structure"] == "json":
            save_to_json(data, ip_address, layer, data_type, config)
        else:
            print(
                "Invalid save structure. Please choose 'folder', 'flat', or 'json'."
            )

    def save_to_folder(data, ip_address, layer, data_type, config):
        """Saves data to a folder structure."""
        if layer is not None:
            folder_path = os.path.join(config["save_path"], f"Layer_{layer}")
            if data_type == "links":
                filename = f"{data.replace('://', '_').replace('/', '_')}.txt"
                save_path = os.path.join(folder_path, "links", filename)
            elif data_type == "images":
                filename = f"{data.replace('://', '_').replace('/', '_')}.jpg"
                save_path = os.path.join(folder_path, "images", filename)

            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "a", encoding="utf-8-sig") as file:
                if data_type == "links":
                    file.write(f"{data}-----{ip_address}\n")
                elif data_type == "images":
                    file.write(f"{data}\n")
        else:
            print("Layer is not provided. Unable to save data to folder.")

    def save_to_flat(data, ip_address, layer, data_type, config):
        """Saves data to a flat file structure."""
        if layer is not None:
            if data_type == "links":
                filename = f"links_layer_{layer}.txt"
                save_path = os.path.join(config["save_path"], filename)
            elif data_type == "images":
                filename = f"images_layer_{layer}.txt"
                save_path = os.path.join(config["save_path"], filename)

            with open(save_path, "a", encoding="utf-8-sig") as file:
                if data_type == "links":
                    file.write(f"{data}-----{ip_address}\n")
                elif data_type == "images":
                    file.write(f"{data}\n")
        else:
            print("Layer is not provided. Unable to save data to flat file.")

    def save_to_json(data, ip_address, layer, data_type, config):
        """Saves data to a JSON file."""
        if layer is not None:
            filename = f"{config['save_path']}.json"
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    try:
                        data_json = json.load(file)
                    except json.JSONDecodeError:
                        print(
                            f"Error: Unable to decode JSON file: {filename}. Proceeding with empty JSON data."
                        )
                        data_json = {}

                if "layers" not in data_json:
                    data_json["layers"] = {}
                if f"Layer_{layer}" not in data_json["layers"]:
                    data_json["layers"][f"Layer_{layer}"] = {}
                if data_type == "links":
                    if "links" not in data_json["layers"][f"Layer_{layer}"]:
                        data_json["layers"][f"Layer_{layer}"]["links"] = []
                    data_json["layers"][f"Layer_{layer}"]["links"].append(
                        {"link": data, "ip": ip_address}
                    )
                elif data_type == "images":
                    if "images" not in data_json["layers"][f"Layer_{layer}"]:
                        data_json["layers"][f"Layer_{layer}"]["images"] = []
                    data_json["layers"][f"Layer_{layer}"]["images"].append(data)

                with open(filename, "w") as file:
                    json.dump(data_json, file, indent=4)
            else:
                with open(filename, "w") as file:
                    data_json = {
                        "layers": {
                            f"Layer_{layer}": {
                                data_type: [
                                    {"link": data, "ip": ip_address}
                                    if data_type == "links"
                                    else data
                                ]
                            }
                        }
                    }
                    json.dump(data_json, file, indent=4)
        else:
            print("Layer is not provided. Unable to save data to JSON file.")

    config = DEFAULT_CONFIG.copy()

    if source is not None:
        config["source"] = source
    if query is not None:
        config["query"] = query
    if initial_processing_method is not None:
        config["initial_processing_method"] = initial_processing_method
    if initial_filtering_phrases is not None:
        config["initial_filtering_phrases"] = initial_filtering_phrases
    if excluded_phrases is not None:
        config["excluded_phrases"] = excluded_phrases
    if image_extraction_method is not None:
        config["image_extraction_method"] = image_extraction_method
    if save_structure is not None:
        config["save_structure"] = save_structure
    if save_path is not None:
        config["save_path"] = save_path
    if max_depth is not None:
        config["max_depth"] = max_depth
    if rate_limit is not None:
        config["rate_limit"] = rate_limit

    initialLinks = get_initial_links(config["source"], config["query"])
    print("Initial links obtained:")
    for link in initialLinks:
        print(link)

    # Process initial links based on the chosen method
    initialLinks = process_initial_set(
        initialLinks, method=config["initial_processing_method"]
    )
    print("\nProcessed initial links:")
    for link in initialLinks:
        print(link)

    # Filter initial links by phrases if provided
    initialLinks = filter_initial_links(
        initialLinks, config["initial_filtering_phrases"]
    )
    print("\nFiltered initial links:")
    for link in initialLinks:
        print(link)

    # Start crawling
    crawl_links(
        initialLinks,
        excluded_phrases=config["excluded_phrases"],
        image_extraction_method=config["image_extraction_method"],
        config=config,
    )