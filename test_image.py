# author Mehakpreet kaur
from transformers import pipeline

pipe = pipeline("image-classification", model="google/vit-base-patch16-224")
result = pipe("https://site-547756.mozfiles.com/files/547756/medium/catoutside.jpeg")
print(result)
