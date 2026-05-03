import json
from groq import Groq
from config import config
from ai.prompts import SYSTEM_PROMPT, build_user_prompt

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)

    def generate_carousel_content(self, topic: str, tone: str = "engaging", slide_count: int = 6):
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(topic, tone, slide_count)}
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Error generating content: {e}")
            raise e

groq_client = GroqClient()
