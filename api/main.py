from core.translate import translate_text
from core.ocr import OCRTask, text_from_image
from fastapi import FastAPI, UploadFile
from PIL import Image
app = FastAPI()

@app.post("/ocr/regional")
def ocr_regional(file: UploadFile):
    image = Image.open(file.file.read())
    text_from_image(OCRTask.WITH_REGIONS, image)

@app.post("/ocr/fullText")
def ocr_full_text(file: UploadFile):
    image = Image.open(file.file.read())
    text_from_image(OCRTask.FULL_TEXT, image)

@app.post("/translate/text")
def translate_text(text: str):
    return translate_text(text)

@app.post("/translate/image")
def translate_from_image(file: UploadFile):
    image = Image.open(file.file.read())
    prediction = text_from_image(OCRTask.WITH_REGIONS, image)
    bboxes, labels = prediction['quad_boxes'], prediction['labels']
    result = []
    for box, label in zip(bboxes, labels):
        translated_text = translate_text(label)
        result.append((box, translated_text))
    return result