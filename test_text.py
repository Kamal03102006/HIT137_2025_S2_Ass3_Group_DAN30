from transformers import pipeline

pipe = pipeline("text-generation", model="distilbert/distilgpt2")
result = pipe("Hello My name is Kamalpreet,", max_length=50, do_sample=True)
print(result[0]["generated_text"])