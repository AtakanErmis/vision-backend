import enum
from typing import Optional
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch
import re


class OCRTask(enum.Enum):
    FULL_TEXT = "<OCR>"
    WITH_REGIONS = "<OCR_WITH_REGION>"
    def __str__(self):
        return str(self.value)

model_id = 'microsoft/Florence-2-large'
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype='auto').eval().cuda()
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

def florence_infer(task_prompt, text_input: Optional[str] = None, image = None):
    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt").to('cuda', torch.float16)
    generated_ids = model.generate(
      input_ids=inputs["input_ids"].cuda(),
      pixel_values=inputs["pixel_values"].cuda(),
      max_new_tokens=1024,
      early_stopping=False,
      do_sample=False,
      num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(
        generated_text,
        task=task_prompt,
        image_size=(image.width, image.height)
    )

    return parsed_answer


def sanitize_text(text: str):
    pattern = r"<[^>]+>"
    if not isinstance(text, str) or not isinstance(pattern, str):
        print("Invalid input: Both text and pattern must be strings.")
        return None

    try:
        compiled_pattern = re.compile(pattern)  # Compile for efficiency if used repeatedly
        return compiled_pattern.sub("", text)  # Replace matches with empty string
    except re.error as e:
        print(f"Invalid regex pattern: {e}")
        return text  # Return original string on regex error


def text_from_image(task: OCRTask, image: Image):
    match str(task):
        case str(OCRTask.FULL_TEXT):
            prediction = florence_infer(str(task), None, image)
            result = prediction[str(OCRTask.FULL_TEXT)]
            return {
                str(OCRTask.FULL_TEXT): sanitize_text(result)
            }
        case str(OCRTask.WITH_REGIONS):
            prediction = florence_infer(str(task), None, image)
            result = prediction[str(OCRTask.WITH_REGIONS)]
            bboxes, labels = result['quad_boxes'], result['labels']
            for bbox, label in zip(bboxes, labels):
                sanitized_label = sanitize_text(label)
                if (len(sanitized_label) == 0):
                    labels.remove(label)
                    bboxes.remove(bbox)
            return {
                str(OCRTask.WITH_REGIONS): {
                    "quad_boxes": bboxes,
                    "labels": labels
                }
            }