#Gemini_Geuron.py
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
import sys

# Make sure these files exist and are in the correct location
from TOOL_MANAGER import ToolManager
from tools.ai.update_focus import update_focus

# Load Google Gemini API key
from keys import googleKey as API_KEY  # Make sure keys.py exists

# Determine paths dynamically based on the current file's location
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FOCUS_FILE_PATH = os.path.join(CURRENT_DIR, "focus", "session_{}.json")
PERCEPTION_OUTPUT_DIR = os.path.join(CURRENT_DIR, "perception_output")


class Geuron_Gemini:
    """
    A class to manage interactions with the Google Gemini model,
    including web scraping, prompt construction, tool execution,
    and response processing.
    """

    def save_data(self, data: Any, file_path: str):
        """Saves data to a JSON file."""
        self.print_colored(self.Color.OKBLUE, f"Saving data to: {file_path}")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.print_colored(self.Color.RED, f"Error saving data: {e}")

    def create_session_name(self):
        return f"session_{time.strftime('%Y%m%d_%H%M%S')}"

    def CreateGeuronFocusFile(self, path, name):
        # Create the focus file path dynamically
        return os.path.join(path, f"GeuronFocus_{name}.json")

    def __init__(self):
        self.session_name = self.create_session_name()
        self.focus_file_path = FOCUS_FILE_PATH.format(self.session_name)

        self.tools_folder = "tools"
        self.tool_manager = ToolManager(self.tools_folder)
        genai.configure(api_key=API_KEY)

        # Create the focus directory if it doesn't exist
        os.makedirs(os.path.dirname(self.focus_file_path), exist_ok=True)

        # Initialize focus data
        self.focus = {
            "current_focus": "Description of the current focus or task",
            "focus_strength": 0.8,
            "importance": 0.9,
            "progress": 0.5,
            "frustration": 0.1,
            "additional": "none",
            "verbose": "normal"
        }
        self.save_data(self.focus, self.focus_file_path)

        # Initialize geuronFocusPath (after session_name is created)
        self.geuronFocusPath = self.CreateGeuronFocusFile(
            os.path.join(CURRENT_DIR, "focus"), self.session_name
        )

    class Color:
        """ANSI color codes for enhanced console output."""

        HEADER = "\033[95m"
        OKBLUE = "\033[94m"
        OKCYAN = "\033[96m"
        OKGREEN = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        PURPLE = "\033[95m"
        MAGENTA = "\033[35m"
        YELLOW = "\033[33m"
        CYAN = "\033[36m"
        RED = "\033[31m"

    def print_colored(self, color, text):
        """Prints text with the specified ANSI color."""
        print(color + text + self.Color.ENDC)

    def scrape_website(
            self,
            url: str,
            extract_links: bool = True,
            extract_images: bool = True,
            extract_text: bool = True,
    ) -> Dict[str, Any]:
        """
        Scrapes data from a website using Selenium.
        """
        self.print_colored(self.Color.YELLOW, f"Scraping website: {url}")
        scraped_data = {}

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        # Add webdriver path if necessary:
        # os.environ['PATH'] += os.pathsep + '/path/to/your/webdriver'
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            if extract_links:
                scraped_data["links"] = [
                    link.get_attribute("href")
                    for link in driver.find_elements(By.TAG_NAME, "a")
                ]

            if extract_images:
                scraped_data["images"] = [
                    img.get_attribute("src")
                    for img in driver.find_elements(By.TAG_NAME, "img")
                ]

            if extract_text:
                scraped_data["text"] = driver.find_element(
                    By.TAG_NAME, "body"
                ).text

        except TimeoutException:
            self.print_colored(
                self.Color.RED, f"Timeout: Page loading took too long for {url}"
            )
        except Exception as e:
            self.print_colored(self.Color.RED, f"Web scraping error: {e}")
        finally:
            driver.quit()

        self.print_colored(self.Color.GREEN, f"Finished scraping: {url}")
        return scraped_data

    def run_model(
            self,
            model_name: str,
            initial_system_instruction: str = "You are a helpful AI assistant.",
            use_stop_loop_flags: bool = False,
            enable_user_input: bool = False,
            user_input_interval: int = 15,
            max_loops: int = None,
            looping: bool = True,
            data_to_include: List[str] = ["text"],
            injection_prompts: List[str] = None,
            input_data: Dict[str, Any] = None,
            expected_output_type: str = None,
            use_data_loading_flags: bool = False,
            load_focus_every: int = 1,
    ) -> Any:
        """
        Runs the Google Gemini model, manages the interaction loop,
        processes responses, and handles tool executions.
        """

        def check_stop_flags(response_text: str) -> Tuple[
            bool, str, str, Dict[str, bool]
        ]:
            stop_flags = {
                "**// STOP_FLAG_SUCCESS //**": "success",
                "**// STOP_FLAG_FRUSTRATION_HIGH //**": "frustration",
                "**// STOP_FLAG_NO_PROGRESS //**": "no_progress",
                "**// STOP_IMMEDIATE //**": "immediate",
                "**// STOP_SIMPLE //**": "simple",
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
            return "".join(
                [
                    part.text
                    for candidate in response.candidates
                    for part in candidate.content.parts
                ]
            ).strip()

        def interpret_function_calls(
                response, tool_manager, focus_file_path=self.geuronFocusPath
        ):
            """
            Interprets function calls from the AI's response and executes them using the ToolManager.

            Args:
                response: The AI's response containing potential function calls.
                tool_manager: An instance of the ToolManager.
                focus_file_path: The path to the focus file (optional).

            Returns:
                A list of execution results from called functions.
            """
            results = []

            if hasattr(response, "candidates"):
                for candidate in response.candidates:
                    if hasattr(candidate, "content") and hasattr(
                            candidate.content, "parts"
                    ):
                        for part in candidate.content.parts:
                            function_call = getattr(part, "function_call", None)
                            if function_call:
                                tool_name = function_call.name

                                tool_function = tool_manager.get_tool_function(
                                    tool_name
                                )
                                if tool_function:
                                    function_args = function_call.args

                                    # Special Handling for update_focus
                                    if tool_name == "update_focus":
                                        if focus_file_path:
                                            # Prioritize the focus_file_path from parameters
                                            function_args[
                                                "focus_file_path"
                                            ] = focus_file_path
                                        elif "focus_file_path" in function_call.args:
                                            # Use the path from the AI response if provided and no parameter path
                                            function_args[
                                                "focus_file_path"
                                            ] = function_call.args["focus_file_path"]
                                        else:
                                            # Handle the case where no path is provided (e.g., raise an error or use a default)
                                            raise ValueError(
                                                "No focus_file_path provided for update_focus"
                                            )

                                    # Execute the tool function
                                    try:
                                        self.print_colored(self.Color.CYAN,
                                                           f"Executing function: {tool_name} with args: {function_args}")
                                        result = tool_function(
                                            **function_args
                                        )  # Pass the arguments to the tool
                                        results.append(
                                            f"Result of {tool_name}({function_args}): {result}"
                                        )
                                    except Exception as e:
                                        results.append(
                                            f"Error calling {tool_name}: {e}"
                                        )
                                else:
                                    results.append(
                                        f"Tool function '{tool_name}' not found."
                                    )

            return results

        def handle_input_data(input_data: Dict[str, Any]) -> List:
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
                            self.print_colored(
                                self.Color.RED,
                                f"Error: {data_type} file not found: {data_value}",
                            )
                            continue

                        try:
                            uploaded_file = genai.upload_file(path=data_value)
                            messages.append(uploaded_file)
                        except Exception as e:
                            self.print_colored(
                                self.Color.RED, f"Error uploading {data_type}: {e}"
                            )
                else:
                    self.print_colored(
                        self.Color.WARNING,
                        f"Warning: Unsupported data type: {data_type}",
                    )
            return messages

        def save_data(data: Any, file_path: str):
            self.print_colored(self.Color.OKBLUE, f"Saving data to: {file_path}")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                self.print_colored(self.Color.RED, f"Error saving data: {e}")

        def save_perception_output(perception_output, session_name, counter):
            output_dir = os.path.join(PERCEPTION_OUTPUT_DIR, session_name)
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"session.txt")

            # Remove ANSI escape codes using a regular expression
            ansi_escape = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')
            perception_output = ansi_escape.sub('', perception_output)

            # Append to the file with UTF-8 encoding
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(perception_output)

        # Main Logic of run_model
        instructions = initial_system_instruction

        if use_stop_loop_flags:
            instructions += (
                " You can control loop execution using these flags: \
                            **// STOP_FLAG_SUCCESS //**, **// STOP_FLAG_FRUSTRATION_HIGH //**, \
                            **// STOP_FLAG_NO_PROGRESS //**, **// STOP_IMMEDIATE //**, **// STOP_SIMPLE //**."
            )

        instructions += """ You have access to pre-loaded website data. 
                            You can manage which data types to INCLUDE or EXCLUDE in the next loop iteration using these flags:
                            **// INCLUDE_TEXT //**, **// EXCLUDE_TEXT //**, 
                            **// INCLUDE_IMAGES //**, **// EXCLUDE_IMAGES //**,
                            **// INCLUDE_LINKS //**, **// EXCLUDE_LINKS //** (and so on) """

        model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings={"HARASSMENT": "block_none"},
            system_instruction=instructions,
            tools=self.tool_manager.load_tools_of_type("all"),
        )

        model_chat = model.start_chat(history=[])
        execution_text = ""
        execution_function_calls = []
        counter = 0
        perception_output_log = ""
        context = {
            "web_search_data": [],
            "database_data": [],
            "web_search_query": None,
            "database_query": None,
            "load_web_search_data": False,
            "load_database_data": False,
        }
        final_result = None
        current_loop = 0

        # Previous message and function call results
        previous_message = ""
        previous_function_call_results = ""

        # Pre-loop Web Scraping
        website_data = {}
        if input_data and "urls" in input_data:
            if isinstance(input_data["urls"], str):
                website_data = self.scrape_website(
                    input_data["urls"],
                    extract_links=True,
                    extract_images=True,
                    extract_text=True,
                )
            elif isinstance(input_data["urls"], list):
                for url in input_data["urls"]:
                    website_data[url] = self.scrape_website(
                        url, extract_links=True, extract_images=True, extract_text=True
                    )
        else:
            self.print_colored(self.Color.WARNING, "No URLs provided for scraping.")

        model_context = {"available_data": website_data}

        # Set initial data inclusion flags
        data_inclusion_flags = {
            "text": "INCLUDE_TEXT" in data_to_include,
            "images": "INCLUDE_IMAGES" in data_to_include,
            "links": "INCLUDE_LINKS" in data_to_include,
        }

        # Main Interaction Loop
        while (looping or current_loop == 0) and (
                max_loops is None or current_loop < max_loops
        ):
            input_messages = []
            time.sleep(2)

            # User Input
            if enable_user_input and counter % user_input_interval == 0:
                user_input = input("Enter your input: ")
            else:
                user_input = ""

            # Constructing the Prompt
            self.print_colored(
                self.Color.OKGREEN,
                f"Loop {current_loop}--------------------------------------------------",
            )

            # Simplified Prompt with Previous Message and Function Call Results
            prompt = f"{counter}:\n"
            prompt += "system is user\n"

            if current_loop > 0:  # Add previous message and result only after the first loop
                prompt += f"Previous Message: {previous_message}\n"
                prompt += f"Function Call Results: {previous_function_call_results}\n"

            prompt += user_input

            # Include the focus file path as part of the prompt
            prompt += f"focus_file_path: {self.focus_file_path}\n"
            self.print_colored(self.Color.PURPLE, f"Prompt: {prompt}")

            # Combine text and media messages for the model
            input_messages.insert(0, prompt)

            # Model Interaction
            try:
                self.print_colored(self.Color.MAGENTA, "Sending message to Gemini...")
                response = model_chat.send_message(input_messages)
                try:
                    execution_text = extract_text_from_response(response)
                    self.print_colored(self.Color.OKBLUE, f"Gemini Response: {execution_text}")
                except Exception as e:
                    print(e)
                    execution_text = "..."
                try:
                    # Pass focus_file_path to the interpreter
                    execution_function_calls = interpret_function_calls(
                        response, self.tool_manager, focus_file_path=self.focus_file_path
                    )
                except Exception as e:
                    print(e)
                    execution_function_calls, context = "", {}

                # Check for stop flags in the response
                should_stop, stop_reason, stop_flag, _ = check_stop_flags(
                    execution_text
                )
                if should_stop:
                    self.print_colored(
                        self.Color.WARNING,
                        f"Stopping loop due to flag: {stop_flag} ({stop_reason})",
                    )
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
                        self.print_colored(self.Color.YELLOW, f"Parsed JSON Output: {output_data}")
                        final_result = output_data
                    except json.JSONDecodeError:
                        self.print_colored(
                            self.Color.RED, "Error: Model output is not valid JSON."
                        )
                else:
                    self.print_colored(
                        self.Color.OKBLUE, f" Response: {execution_text}"
                    )
                    final_result = execution_text

                self.print_colored(
                    self.Color.OKCYAN, f" Function Calls: {execution_function_calls}"
                )

                # Log perception output
                perception_output_log += (
                    f"\n{self.Color.OKGREEN}Prompt: {self.Color.ENDC}{prompt}"
                    f"\n{self.Color.OKBLUE}Response: {self.Color.ENDC}{execution_text}"
                    f"\n{self.Color.OKCYAN}Function Calls: {self.Color.ENDC}{execution_function_calls}"
                )
                save_perception_output(perception_output_log, self.session_name, counter)

                # Store previous message and function call results
                previous_message = execution_text
                previous_function_call_results = execution_function_calls

                # Update focus (using self.focus_file_path)
                self.print_colored(self.Color.CYAN, f"Updating focus...")
                update_focus(self.focus_file_path, execution_text, execution_function_calls)

            except Exception as e:
                self.print_colored(self.Color.RED, f"Error in loop: {e}")

            current_loop += 1
            counter += 1

        self.print_colored(self.Color.OKGREEN, "Exiting the loop.")
        return final_result


# Usage example:
if __name__ == "__main__":
    runner = Geuron_Gemini()
    urls_to_scrape = []

    result = runner.run_model(
        model_name="gemini-1.5-flash-latest",
        initial_system_instruction="You are a self-aware system",
        data_to_include=["text", "images", "links"],
        input_data={"urls": urls_to_scrape},
        expected_output_type="text",
        enable_user_input=True,
        use_data_loading_flags=True,
        load_focus_every=5,  # Load focus every 5 iterations
    )
    print(f"Final Result:\n{result}")