
from transformers import pipeline

class DescriptionService:
  def __init__(self):
    self.pipeline = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

  def describe(self, image):
    result = self.pipeline(image)

    return result[0].get('generated_text')

