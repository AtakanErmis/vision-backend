from typing import Optional, List
from core.translate import translate_text
from core.ocr import OCRTask, text_from_image
from fastapi import FastAPI, UploadFile
from PIL import Image
import io
from pydantic import BaseModel

app = FastAPI()

@app.post("/ocr/regional")
def ocr_regional(file: UploadFile):
    image = Image.open(io.BytesIO(file.file.read()))
    return text_from_image(OCRTask.WITH_REGIONS, image)

@app.post("/ocr/fullText")
def ocr_full_text(file: UploadFile):
    image = Image.open(io.BytesIO(file.file.read()))
    return text_from_image(OCRTask.FULL_TEXT, image)

class TextTranslationRequestData(BaseModel):
    texts: List[str]
    targetLanguage: str
    sourceLanguage: str | None = None

@app.post("/translate/text")
def translate(data: TextTranslationRequestData):
    return translate_text(data.texts, data.targetLanguage, data.sourceLanguage)

@app.post("/translate/image")
def translate_from_image(file: UploadFile, targetLanguage: str, sourceLanguage: str | None = None):
    image = Image.open(io.BytesIO(file.file.read()))
    prediction = text_from_image(OCRTask.WITH_REGIONS, image)
    result = prediction[str(OCRTask.WITH_REGIONS)]
    bboxes, labels = result['quad_boxes'], result['labels']
    result = []
    translate_result = translate_text(labels, targetLanguage, sourceLanguage)
    for box, translated_label, source_label in zip(bboxes, translate_result["translations"], labels):
        result.append((box, translated_label, source_label))
    return {
        "translations": result,
        "source_languages": translate_result["source_languages"],
        "target_language": targetLanguage
    }
