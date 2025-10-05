# author Mehakpreet kaur
# models_adapter.py
import warnings
warnings.filterwarnings("ignore")

from abc import ABC, abstractmethod
from transformers import pipeline
from decorators import log_call, catch_exceptions

class ModelAdapter(ABC):
    def __init__(self, model_name):
        self._model_name = model_name  # protected (encapsulation)
        self.__secret = None           # private attribute (encapsulation)

    def set_secret(self, s):
        self.__secret = s

    @abstractmethod
    def run(self, input_data):
        pass

    @abstractmethod
    def get_info(self):
        pass

# Mixin to show multiple inheritance
class HFModelMixin:
    def create_pipeline(self, task, model_name=None):
        if model_name:
            return pipeline(task, model=model_name)
        return pipeline(task)

# Text generation adapter (polymorphism: same interface as image adapter)
class TextGenAdapter(HFModelMixin, ModelAdapter):
    def __init__(self, model_name="distilgpt2"):
        super().__init__(model_name)
        # <<< Hugging Face model is INITIALIZED HERE >>>
        self._pipe = self.create_pipeline("text-generation", model_name)

    @log_call
    @catch_exceptions
    def run(self, prompt):
        if not prompt:
            prompt = "Hello from HIT137"
        res = self._pipe(prompt, max_length=60, do_sample=True)

        return res[0].get("generated_text", str(res))

    def get_info(self):
        return {"task": "text-generation", "model": self._model_name}

class ImageClassAdapter(HFModelMixin, ModelAdapter):
    def __init__(self, model_name="google/vit-base-patch16-224"):
        super().__init__(model_name)
        # <<< Hugging Face model is INITIALIZED HERE >>>
        self._pipe = self.create_pipeline("image-classification", model_name)

    @log_call
    @catch_exceptions
    def run(self, image_path_or_pil):
        res = self._pipe(image_path_or_pil)
        return res  # list of label dicts

    def get_info(self):
        return {"task": "image-classification", "model": self._model_name}
