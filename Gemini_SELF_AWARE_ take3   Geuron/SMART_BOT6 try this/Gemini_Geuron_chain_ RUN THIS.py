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
import logging
import base64
import cv2

logging.basicConfig(filename='geuron.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

from TOOL_MANAGER import ToolManager
from tools.ai.update_focus import update_focus
from tools.ai.update_own_config import update_own_config

from keys import googleKey as API_KEY

genai.configure(api_key=API_KEY)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FOCUS_FILE_PATH = os.path.join(CURRENT_DIR, "focus", "session_{}.json")
PERCEPTION_OUTPUT_DIR = os.path.join(CURRENT_DIR, "perception_output")
CONFIG_DIR = "CONFIG"  # Directory to store configurations
INITIAL_CONFIG_FILE = "Initial_Config.json"  # Initial configuration file
CURRENT_CONFIG_FILE = "Current_Config.json"  # Current configuration file

import google.cloud.texttospeech as tts


def generate_audio_tts(text: str, output_file: str, language_code: str = "en-US", voice_name: str = None) -> str:
    try:
        client = tts.TextToSpeechClient()
        synthesis_input = tts.SynthesisInput(text=text)
        voice = tts.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        with open(output_file, "wb") as out:
            out.write(response.audio_content)

        return output_file

    except Exception as e:
        return f"Error generating audio: {e}"


def loadConfig(config_file=CURRENT_CONFIG_FILE):
    """Loads the configuration from the specified file.

    Args:
        config_file (str, optional): The name of the configuration file to load. Defaults to "Current_Config.json".

    Returns:
        dict: The loaded configuration.
    """
    config_path = os.path.join(CONFIG_DIR, config_file)
    if not os.path.exists(config_path):
        if config_file == CURRENT_CONFIG_FILE:
            # Create a default Current_Config.json based on Initial_Config.json
            create_default_current_config()
        else:
            return None  # Or raise an exception if the specified config doesn't exist

    with open(config_path, "r") as f:
        return json.load(f)


def create_default_current_config():
    """Creates a default Current_Config.json based on Initial_Config.json."""
    initial_config = loadConfig(INITIAL_CONFIG_FILE)
    if initial_config:
        with open(os.path.join(CONFIG_DIR, CURRENT_CONFIG_FILE), "w") as f:
            json.dump(initial_config, f, indent=4)


class Geuron_Gemini:
    def save_data(self, data: Any, file_path: str):
        logging.info(f"Saving data to: {file_path}")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving data: {e}")

    def create_session_name(self):
        return f"session_{time.strftime('%Y%m%d_%H%M%S')}"

    def CreateGeuronFocusFile(self, path, name):
        return os.path.join(path, f"GeuronFocus_{name}.json")

    def __init__(self):
        self.session_name = self.create_session_name()
        self.focus_file_path = FOCUS_FILE_PATH.format(self.session_name)
        self.tools_folder = "tools"
        self.tool_manager = ToolManager(self.tools_folder)
        genai.configure(api_key=API_KEY)

        os.makedirs(os.path.dirname(self.focus_file_path), exist_ok=True)

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

        self.geuronFocusPath = self.CreateGeuronFocusFile(
            os.path.join(CURRENT_DIR, "focus"), self.session_name
        )

    def print_colored(self, color, text):
        print(color + text + self.Color.ENDC)

    def scrape_website(self, url: str, extract_links: bool = True, extract_images: bool = True,
                       extract_text: bool = True) -> Dict[str, Any]:
        logging.info(f"Scraping website: {url}")
        scraped_data = {}
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            if extract_links:
                scraped_data["links"] = [link.get_attribute("href") for link in driver.find_elements(By.TAG_NAME, "a")]

            if extract_images:
                scraped_data["images"] = [img.get_attribute("src") for img in driver.find_elements(By.TAG_NAME, "img")]

            if extract_text:
                scraped_data["text"] = driver.find_element(By.TAG_NAME, "body").text

        except TimeoutException:
            logging.error(f"Timeout: Page loading took too long for {url}")
        except Exception as e:
            logging.error(f"Web scraping error: {e}")
        finally:
            driver.quit()

        logging.info(f"Finished scraping: {url}")
        return scraped_data

    def extract_text_from_response(self, response) -> str:
        return "".join([part.text for candidate in response.candidates for part in candidate.content.parts]).strip()

    def interpret_function_calls(self, response, tool_manager, focus_file_path=None):
        results = []

        if hasattr(response, "candidates"):
            for candidate in response.candidates:
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                    for part in candidate.content.parts:
                        function_call = getattr(part, "function_call", None)
                        if function_call:
                            tool_name = function_call.name
                            tool_function = tool_manager.get_tool_function(tool_name)

                            if tool_function:
                                function_args = function_call.args

                                if tool_name == "update_focus":
                                    if focus_file_path:
                                        function_args["focus_file_path"] = focus_file_path
                                    elif "focus_file_path" in function_call.args:
                                        function_args["focus_file_path"] = function_call.args["focus_file_path"]
                                    else:
                                        raise ValueError("No focus_file_path provided for update_focus")

                                try:
                                    logging.info(f"Executing function: {tool_name} with args: {function_args}")
                                    result = tool_function(**function_args)

                                    if tool_name in ("load_image", "load_images", "load_audio", "load_video"):
                                        if result["status"] == "success":
                                            if "image_data" in result:
                                                _, image_encoded = cv2.imencode('.jpg', result["image_data"])
                                                result["image_data_base64"] = base64.b64encode(image_encoded).decode(
                                                    'utf-8')
                                            elif "loaded_images" in result:
                                                for img_data in result["loaded_images"]:
                                                    _, img_encoded = cv2.imencode('.jpg', img_data["image_data"])
                                                    img_data["image_data_base64"] = base64.b64encode(img_encoded).decode(
                                                        'utf-8')
                                            elif "audio_data" in result:
                                                result["audio_data_base64"] = base64.b64encode(
                                                    result["audio_data"]).decode('utf-8')
                                            elif "video_data" in result:
                                                result["video_data_base64"] = base64.b64encode(
                                                    result["video_data"]).decode('utf-8')

                                    results.append(f"Result of {tool_name}({function_args}): {result}")
                                except Exception as e:
                                    results.append(f"Error calling {tool_name}: {e}")
                            else:
                                results.append(f"Tool function '{tool_name}' not found.")

        return results

    def load_focus_file(self, file_path):
        try:
            with open(file_path, "r") as f:
                focus_data = json.load(f)
                return focus_data
        except FileNotFoundError:
            logging.error(f"Focus file not found: {file_path}")
            return {}
        except Exception as e:
            logging.error(f"Error loading focus file: {e}")
            return {}

    def run_chained_models(self, models_config: List[Dict], input_data: Dict[str, Any] = None, max_loops: int = None):
        context = ""
        current_loop = 0
        loop_type = models_config.get("loop_type", "fixed")
        num_loops = models_config.get("num_loops", 1)
        max_loops = models_config.get("max_loops", None)

        while (loop_type == "infinite" or current_loop < num_loops) and (max_loops is None or current_loop < max_loops):
            time.sleep(5)
            logging.info(f"------------Loop {current_loop} --------------------------------------------------")

            for model_config in models_config["models"]:
                model_ID = model_config["model_ID"]
                logging.info(f"Model ID: {model_ID}")

                loadFocus = model_config["loadFocus"]
                model_name = model_config["model_name"]
                system_instruction = model_config["system_instruction"]
                allowed_tools = model_config["allowed_tools"]
                prompt_injector = model_config.get("prompt_injector", "")
                generateAudio = model_config.get("generateAudio", False)

                use_flags = model_config.get("useFlags", False)
                if use_flags:
                    flag_instruction = model_config.get("STOP_FLAGS_instruction", "")
                    prompt = f"\n{flag_instruction}"

                model = genai.GenerativeModel(
                    model_name=model_name,
                    safety_settings={"HARASSMENT": "block_none"},
                    system_instruction=system_instruction,
                    tools=self.tool_manager.load_tools_of_type(allowed_tools),
                )

                model_chat = model.start_chat(history=[])

                prompt = f"Previous Context: {context}\n{prompt_injector}"
                if loadFocus == "True":
                    focus_data = self.load_focus_file(self.focus_file_path)
                    prompt += f"\nCurrent Focus: {focus_data}"

                try:
                    logging.info(f"Sending message to {model_name}...")

                    response = model_chat.send_message(prompt)
                    text = self.extract_text_from_response(response)
                    logging.info(f"{model_name} Response: {text}")

                    if allowed_tools:
                        function_results = self.interpret_function_calls(
                            response, self.tool_manager, focus_file_path=self.focus_file_path
                        )
                        logging.info(f"Function Calls: {function_results}")
                        text += f"\nFunction Results: {function_results}"

                    if generateAudio and text is not None:
                        audio_file_path = os.path.join(
                            PERCEPTION_OUTPUT_DIR, self.session_name, f"{self.session_name}_loop{current_loop}_{model_ID}.mp3"
                        )
                        generate_audio_tts(text, audio_file_path)
                        logging.info(f"Audio generated and saved to: {audio_file_path}")

                    if use_flags:
                        flag_pattern = model_config.get("STOP_FLAGS_pattern", None)
                        if flag_pattern:
                            match = re.search(flag_pattern, text)
                            if match:
                                flag_value = match.group(1).strip()
                                logging.info(f"Stopping loop due to STOP flag: {flag_value}")
                                return context

                    context += f"\n{text}\nFunction Results: {function_results}"

                except Exception as e:
                    logging.error(f"Error in {model_name}: {e}")

            current_loop += 1

            # Reload the config after each loop
            models_config = loadConfig()  # Load Current_Config.json by default

        logging.info("Exiting the loop.")
        return context


class Color:
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



if __name__ == "__main__":
    runner = Geuron_Gemini()
    urls_to_scrape = []

    # Load the configuration here before starting the loop
    models_config = loadConfig()

    # The initial models_config is loaded at the start
    runner.run_chained_models(models_config)