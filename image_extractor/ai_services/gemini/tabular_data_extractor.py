from google import generativeai as genai
from django.conf import settings
from image_extractor.ai_services.gemini.config import (
    GEMINI_MODEL_NAME,
    GEMINI_GENERATION_CONFIG,
    GEMINI_SYSTEM_INSTRUCTION_FOR_TRANSACTIONS,
)


class GeminiTabularDataExtractor:
    def __init__(self):
        """Initialize with API key and model configuration."""
        self.api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)

        self.model_name = GEMINI_MODEL_NAME
        self.generation_config = GEMINI_GENERATION_CONFIG

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
            system_instruction=GEMINI_SYSTEM_INSTRUCTION_FOR_TRANSACTIONS,
        )

    def upload_file(self, file_path, mime_type="image/png"):
        """Uploads an image to Gemini."""
        file = genai.upload_file(file_path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    def extract_data(self, file_paths):
        """
        Processes multiple images and extracts tabular data.
        :param file_paths: List of image file paths
        :return: Dictionary of extracted data for each image
        """
        if not isinstance(file_paths, list):
            raise ValueError("file_paths must be a list of image paths.")

        uploaded_files = [self.upload_file(path) for path in file_paths]

        # Start a chat session and send all images in a single message
        chat_session = self.model.start_chat(
            history=[{"role": "user", "parts": uploaded_files}]
        )

        response = chat_session.send_message(
            "Extract tabular data from these images and return structured results."
        )

        return response.text
