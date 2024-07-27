import time
import os
import json
import re
import google.generativeai as genai
from typing import Dict, List, Any, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Assuming these modules exist and are correctly implemented:
from TOOL_MANAGER import ToolManager
from tools.ai.update_focus import update_focus

# Load Google Gemini API key
from keys import googleKey as API_KEY

class Geuron_Gemini:
    """
    A class to manage interactions with the Google Gemini model,
    including web scraping, prompt construction, tool execution,
    and response processing.
    """
    def __init__(self):
        self.tools_folder = "tools"
        self.tool_manager = ToolManager(self.tools_folder)
        genai.configure(api_key=API_KEY)

    class Color:
        """ANSI color codes for enhanced console output."""
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'  # Resets color
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        PURPLE = '\033[95m'
        MAGENTA = '\033[35m'
        YELLOW = '\033[33m'
        CYAN = '\033[36m'
        RED = '\033[31m'

    def print_colored(self, color, text):
        """Prints text with the specified ANSI color."""
        print(color + text + self.Color.ENDC)

    def scrape_website(self, url: str, extract_links: bool = True,
                       extract_images: bool = True,
                       extract_text: bool = True) -> Dict[str, Any]:
        """
        Scrapes data from a website using Selenium.

        Args:
            url (str): Website URL to scrape.
            extract_links (bool): Extract links (default True).
            extract_images (bool): Extract image URLs (default True).
            extract_text (bool): Extract text content (default True).

        Returns:
            Dict[str, Any]: Scraped data ('links', 'images', 'text').
        """
        print(f"Scraping website: {url}")
        scraped_data = {}

        options = webdriver.ChromeOptions()
        # options.add_argument('--headless=new') # Uncomment for headless mode
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            if extract_links:
                scraped_data['links'] = [link.get_attribute("href")
                                          for link in driver.find_elements(By.TAG_NAME, "a")]

            if extract_images:
                scraped_data['images'] = [img.get_attribute("src")
                                          for img in driver.find_elements(By.TAG_NAME, "img")]

            if extract_text:
                scraped_data['text'] = driver.find_element(By.TAG_NAME, "body").text

        except TimeoutException:
            self.print_colored(self.Color.RED,
                              f"Timeout: Page loading took too long for {url}")
        except Exception as e:
            self.print_colored(self.Color.RED, f"Web scraping error: {e}")

        driver.quit()
        return scraped_data

    def run_model(self,
                  model_name: str,
                  initial_system_instruction: str = "You are a helpful AI assistant.",
                  use_stop_loop_flags: bool = False,
                  enable_user_input: bool = False,
                  user_input_interval: int = 15,
                  max_loops: int = 10,
                  looping: bool = True,
                  data_to_include: List[str] = ["text"],
                  injection_prompts: List[str] = None,
                  input_data: Dict[str, Any] = None,
                  expected_output_type: str = None,
                  use_data_loading_flags: bool = False) -> Any:
        """
        Runs the Google Gemini model, manages the interaction loop,
        processes responses, and handles tool executions.

        Args:
            model_name (str): Name of the Gemini model to use.
            initial_system_instruction (str): Initial instructions for the model.
            use_stop_loop_flags (bool): Allow loop control with flags (default False).
            enable_user_input (bool): Enable user input during the loop (default False).
            user_input_interval (int): How often to prompt for user input (default 15).
            max_loops (int): Maximum number of interaction loops (default 10).
            looping (bool): Run in a loop (default True).
            data_to_include (List[str]): Initial data types to include ('text', 'images', 'links').
            injection_prompts (List[str]): Additional prompts to inject.
            input_data (Dict[str, Any]): Input data for the model ('urls', etc.).
            expected_output_type (str): Expected output type ('json', 'text', etc.).
            use_data_loading_flags (bool): Allow data inclusion flags (default False).

        Returns:
            Any: The final result from the model interaction.
        """
        # --- Helper Functions (nested for better organization) ---
        def check_stop_flags(response_text: str) -> Tuple[bool, str, str, Dict[str, bool]]:
            """Checks the model's response for loop control flags."""
            stop_flags = {
                "**// STOP_FLAG_SUCCESS //**": "success",
                "**// STOP_FLAG_FRUSTRATION_HIGH //**": "frustration",
                "**// STOP_FLAG_NO_PROGRESS //**": "no_progress",
                "**// STOP_IMMEDIATE //**": "immediate",
                "**// STOP_SIMPLE //**": "simple"
            }
            data_flags = {}
            flag_pattern = r"\*\*//\s*(INCLUDE|EXCLUDE)_(.*?)\s*//\*\*"
            for match in re.findall(flag_pattern, response_text):
                action, data_source = match
                data_flags[f"{action.lower()}_{data_source.lower()}"] = True

            for flag, reason in stop_flags.items():
                if flag in response_text:
                    return True, reason, flag, data_flags
            return False, "", "", data_flags

        def extract_text_from_response(response) -> str:
            """Extracts text content from the Gemini model's response."""
            return "".join([part.text for candidate in response.candidates
                            for part in candidate.content.parts]).strip()

        def interpret_function_calls(response, tool_manager, focus_file_path) -> Tuple[List[str], Dict]:
            """
            Interprets function calls from the model and executes them.
            Manages a shared 'context' dictionary that can be updated
            by tools and used in subsequent calls.
            """
            results = []
            context = {}
            if hasattr(response, 'candidates'):
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            function_call = getattr(part, 'function_call', None)
                            if function_call:
                                self.print_colored(self.Color.MAGENTA, "---------------INTERPRETER-------------------")
                                tool_name = function_call.name

                                tool_function = tool_manager.get_tool_function(tool_name)
                                if tool_function:
                                    function_args = function_call.args
                                    self.print_colored(self.Color.YELLOW, f"Function name: {tool_name}")
                                    for key, value in function_args.items():
                                        self.print_colored(self.Color.CYAN, f"        {key}: {value}")
                                    try:
                                        result = tool_function(**function_args, context=context, focus_file_path=focus_file_path)
                                        if isinstance(result, dict) and 'context' in result:
                                            context.update(result['context'])
                                        results.append(f"Result of {tool_name}({function_args}): {result}")
                                    except Exception as e:
                                        self.print_colored(self.Color.RED, f"Error calling {tool_name}: {e}")
                                        results.append(f"Error calling {tool_name}: {e}")
                                else:
                                    self.print_colored(self.Color.RED, f"Tool function '{tool_name}' not found.")
            return results, context

        def create_session_name() -> str:
            """Creates a timestamped session name for logging."""
            return f"session_{time.strftime('%Y%m%d_%H%M%S')}"

        def handle_input_data(input_data: Dict[str, Any]) -> List:
            """Prepares and handles different input data types for the model."""
            messages = []
            for data_type, data_values in input_data.items():
                if data_type == "text":
                    if isinstance(data_values, str):
                        messages.append(data_values)
                    elif isinstance(data_values, list):
                        messages.extend(data_values)
                elif data_type in ("image", "audio"):
                    if not isinstance(data_values, list):
                        data_values = [data_values]

                    for data_value in data_values:
                        if not os.path.exists(data_value):
                            self.print_colored(self.Color.RED,
                                              f"Error: {data_type} file not found: {data_value}")
                            continue

                        try:
                            uploaded_file = genai.upload_file(path=data_value)
                            messages.append(uploaded_file)
                        except Exception as e:
                            self.print_colored(self.Color.RED,
                                              f"Error uploading {data_type}: {e}")
                else:
                    self.print_colored(self.Color.WARNING,
                                      f"Warning: Unsupported data type: {data_type}")
            return messages

        def save_data(data: Any, file_path: str):
            """Saves data to a JSON file."""
            print(f"Saving data to: {file_path}")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                self.print_colored(self.Color.RED, f"Error saving data: {e}")

        def save_perception_output(perception_output, session_name, counter):
            """Saves the AI's perception output to log files."""
            output_dir = os.path.join("perception_output", session_name)
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"{counter}.txt")
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(perception_output)

        # --- Main Logic of run_model ---
        instructions = initial_system_instruction

        if use_stop_loop_flags:
            instructions += " You can control loop execution using these flags: \
                            **// STOP_FLAG_SUCCESS //**, **// STOP_FLAG_FRUSTRATION_HIGH //**, \
                            **// STOP_FLAG_NO_PROGRESS //**, **// STOP_IMMEDIATE //**, **// STOP_SIMPLE //**."

        instructions += """ You have access to pre-loaded website data. 
                            You can manage which data types to INCLUDE or EXCLUDE in the next loop iteration using these flags:
                            **// INCLUDE_TEXT //**, **// EXCLUDE_TEXT //**, 
                            **// INCLUDE_IMAGES //**, **// EXCLUDE_IMAGES //**,
                            **// INCLUDE_LINKS //**, **// EXCLUDE_LINKS //** (and so on) """

        # Create session name and focus file path
        session_name = create_session_name()
        focus_file_path = os.path.join("focus", session_name + ".json")
        os.makedirs("focus", exist_ok=True)  # Ensure focus directory exists

        # Initialize focus
        focus = {"id": session_name}
        save_data(focus, focus_file_path)

        model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings={'HARASSMENT': 'block_none'},
            system_instruction=instructions,
            tools=self.tool_manager.load_tools_of_type("all"),
            context={"focus_file_path": focus_file_path}  # Pass focus file path
        )

        model_chat = model.start_chat(history=[])
        execution_text = ""
        execution_function_calls = []
        counter = 0
        perception_output_log = ""
        short_term_memory = []
        context = {
            'web_search_data': [],
            'database_data': [],
            'web_search_query': None,
            'database_query': None,
            'load_web_search_data': False,
            'load_database_data': False
        }
        final_result = None
        current_loop = 0

        # --- Pre-loop Web Scraping ---
        website_data = {}
        if input_data and "urls" in input_data:
            if isinstance(input_data["urls"], str):
                website_data = self.scrape_website(input_data["urls"],
                                                  extract_links=True,
                                                  extract_images=True,
                                                  extract_text=True)
            elif isinstance(input_data["urls"], list):
                for url in input_data["urls"]:
                    website_data[url] = self.scrape_website(url,
                                                          extract_links=True,
                                                          extract_images=True,
                                                          extract_text=True)
        else:
            self.print_colored(self.Color.WARNING, "No URLs provided for scraping.")

        model_context = {"available_data": website_data}

        # --- Set initial data inclusion flags ---
        data_inclusion_flags = {
            "text": "INCLUDE_TEXT" in data_to_include,
            "images": "INCLUDE_IMAGES" in data_to_include,
            "links": "INCLUDE_LINKS" in data_to_include
        }

        # --- Main Interaction Loop ---
        while current_loop < max_loops and (looping or current_loop == 0):
            input_messages = []
            time.sleep(2)

            # --- User Input ---
            if enable_user_input and counter % user_input_interval == 0:
                user_input = input("Enter your input: ")
            else:
                user_input = ""

            # --- Constructing the Prompt ---
            self.print_colored(self.Color.OKGREEN,
                              f"Loop {current_loop}--------------------------------------------------")
            prompt = f"{counter}:\n"
            prompt += "system is user\n"

            # Load focus for this session
            with open(focus_file_path, "r", encoding='utf-8') as f:
                focus = json.load(f)
            if focus:
                prompt += f"Current Focus: {json.dumps(focus)}\n"
            else:
                prompt += "Current Focus: None\n"

            # Add data based on inclusion/exclusion flags
            for url, data in model_context["available_data"].items():
                if data_inclusion_flags['text'] and "text" in data:
                    prompt += f"Website Text ({url}):\n{data['text']}\n"
                if data_inclusion_flags['images'] and "images" in data:
                    prompt += f"Website Images ({url}):\n{', '.join(data['images'])}\n"
                if data_inclusion_flags['links'] and "links" in data:
                    prompt += f"Website Links ({url}):\n{', '.join(data['links'])}\n"

            # Inject additional prompts if provided
            if injection_prompts:
                input_messages.extend(injection_prompts)

            # Add short-term memory (recent interactions) to the prompt
            if short_term_memory:
                prompt += "Recent Interactions:\n"
                for i, memory_item in enumerate(short_term_memory):
                    prompt += f"  - {memory_item}\n"

            prompt += user_input

            # Combine text and media messages for the model
            input_messages.insert(0, prompt)

            # --- Model Interaction ---
            try:
                print("Sending message...")
                response = model_chat.send_message(input_messages)
                try:
                    execution_text = extract_text_from_response(response)
                except Exception as e:
                    print(e)
                    execution_text="..."
                try:
                    execution_function_calls, context = interpret_function_calls(response, self.tool_manager, focus_file_path)
                except Exception as e:
                    print(e)
                    execution_function_calls, context=""

                # Check for stop flags in the response
                should_stop, stop_reason, stop_flag, _ = check_stop_flags(execution_text)
                if should_stop:
                    self.print_colored(self.Color.WARNING,
                                      f"Stopping loop due to flag: {stop_flag} ({stop_reason})")
                    break

                # Update data inclusion/exclusion flags based on the model's response
                if use_data_loading_flags:
                    data_flag_mapping = {
                        "**// INCLUDE_TEXT //**": "text",
                        "**// EXCLUDE_TEXT //**": "text",
                        "**// INCLUDE_IMAGES //**": "images",
                        "**// EXCLUDE_IMAGES //**": "images",
                        "**// INCLUDE_LINKS //**": "links",
                        "**// EXCLUDE_LINKS //**": "links",
                    }

                    for flag, data_type in data_flag_mapping.items():
                        if flag in execution_text:
                            data_inclusion_flags[data_type] = "INCLUDE" in flag

                # Output interpretation based on expected type
                if expected_output_type == "json":
                    try:
                        output_data = json.loads(execution_text)
                        print(f"Parsed JSON Output: {output_data}")
                        final_result = output_data
                    except json.JSONDecodeError:
                        self.print_colored(self.Color.RED, "Error: Model output is not valid JSON.")
                else:
                    self.print_colored(self.Color.OKBLUE, f" Response: {execution_text}")
                    final_result = execution_text

                self.print_colored(self.Color.OKCYAN, f" Function Calls: {execution_function_calls}")

                # Log perception output
                perception_output_log += (
                    f"\n{self.Color.OKGREEN}Prompt: {self.Color.ENDC}{prompt}"
                    f"\n{self.Color.OKBLUE}Response: {self.Color.ENDC}{execution_text}"
                    f"\n{self.Color.OKCYAN}Function Calls: {self.Color.ENDC}{execution_function_calls}"
                )
                save_perception_output(perception_output_log, session_name, counter)

                # Update short-term memory
                short_term_memory.append(f"User: {user_input}")
                short_term_memory.append(f"Assistant: {execution_text}")

            except Exception as e:
                self.print_colored(self.Color.RED, f"Error in loop: {e}")

            current_loop += 1

        self.print_colored(self.Color.OKGREEN, "Exiting the loop.")
        return final_result

# Usage example:
if __name__ == "__main__":
    runner = Geuron_Gemini()
    urls_to_scrape = [
        "https://www.example.com",
        "https://www.wikipedia.org"
    ]

    result = runner.run_model(
        model_name="gemini-pro",
        initial_system_instruction="You are a helpful AI assistant that analyzes websites.",
        data_to_include=["text", "images", "links"],
        input_data={"urls": urls_to_scrape},
        expected_output_type="text",
        enable_user_input=True,
        max_loops=3,
        use_data_loading_flags=True
    )
    print(f"Final Result:\n{result}")