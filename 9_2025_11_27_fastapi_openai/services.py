from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class InferenceService:
    def __init__(self, model_selector):
        self.selector = model_selector

    async def run(self, task, prompt):
        model = self.selector.choose(task)

        response = client.responses.create(
            model=model,
            input=prompt
        )

        return {
            "model_used": model,
            "output": response.output_text
        }
