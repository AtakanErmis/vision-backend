from typing import Optional

from google.cloud import translate_v3

PROJECT_ID = "nku-proje-i-vision"
DEFAULT_LANGUAGE = "tr"

# Initialize Translation client
def translate_text(
        text: str = "YOUR_TEXT_TO_TRANSLATE",
        language_code: str = DEFAULT_LANGUAGE,
        source_language_code: Optional[str] = None,
) -> translate_v3.TranslationServiceClient:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/global"
    # Translate text from English to chosen language
    # Supported mime types: # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        contents=[text],
        target_language_code=language_code,
        parent=parent,
        mime_type="text/plain",
        source_language_code=source_language_code,
    )

    return response