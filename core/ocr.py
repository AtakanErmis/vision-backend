import enum
from typing import Optional, TypedDict

from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch

class OCRTask(enum.Enum):
    FULL_TEXT = "<OCR>"
    WITH_REGIONS = "<OCR_WITH_REGION>"

model_id = 'microsoft/Florence-2-large'
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, torch_dtype='auto').eval().cuda()
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

def florence_infer(task_prompt, text_input: Optional[str] = None, image: Optional[Image] = None):
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


def text_from_image(task: OCRTask, image: Image):
    match task:
        case OCRTask.FULL_TEXT:
            return florence_infer(task, None, image)
        case OCRTask.WITH_REGIONS:
            return florence_infer(task, None, image)
        case _:
            raise ValueError("Invalid OCR task")
