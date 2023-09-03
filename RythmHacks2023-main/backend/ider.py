from PIL import Image
from transformers import AutoImageProcessor, ResNetForImageClassification
import torch
import requests

processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")

def identify_image(url):
    image = Image.open(requests.get(url, stream=True).raw)
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    # model predicts one of the 1000 ImageNet classes
    predicted_label = logits.argmax(-1).item()
    return model.config.id2label[predicted_label]