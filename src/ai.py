import requests
import json
import os


class AIModelPredictor:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/"
        self.api_key = os.getenv("HF_API_KEY")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def generate(self, prompt):
        # model = "google/flan-t5-small"
        # model = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
        # model = "gpt2-large"
        # model = "bigscience/bloom-560m"
        # model = "EleutherAI/gpt-neo-2.7B"
        model = "microsoft/DialoGPT-medium"

        data = json.dumps(
            {
                "inputs": prompt,
                "temperature": 0.9,
                "max_length": 1000,
                "max_new_tokens": 1000,
            }
        )

        response = requests.request(
            "POST", self.api_url + model, headers=self.headers, data=data
        )

        content = response.content.decode("utf-8")

        try:
            data = json.loads(content[1:][:-1])
            return data
        except:
            return content

    def summarize(self, prompt):
        model = "philschmid/bart-large-cnn-samsum"

        data = json.dumps(
            {
                "inputs": prompt,
                "temperature": 0.8,
                "max_length": 1000,
                "min_length": 30,
                "do_sample": False,
            }
        )

        response = requests.request(
            "POST", self.api_url + model, headers=self.headers, data=data
        )

        content = response.content.decode("utf-8")
        return content

    def chat(self, prompt):
        model = "facebook/blenderbot-400M-distill"

        data = json.dumps(
            {
                "inputs": prompt,
                "temperature": 0.8,
                "max_length": 1000,
                "min_length": 30,
                "do_sample": False,
            }
        )

        response = requests.request(
            "POST", self.api_url + model, headers=self.headers, data=data
        )

        content = response.content.decode("utf-8")
        return content

    def code_completition(self, prompt):
        # model = "bigcode/santacoder"
        model = "bigcode/starcoder"

        data = json.dumps(
            {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 1256,
                    "do_sample": True,
                    "top_p": 0.95,
                    "temperature": 0.75,
                    "num_return_sequences": 1,
                    "stop_sequence": "\n\n",
                },
            }
        )

        response = requests.request(
            "POST", self.api_url + model, headers=self.headers, data=data
        )

        content = response.content.decode("utf-8")
        return content
