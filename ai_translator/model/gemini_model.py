import os
import requests
import simplejson

from model import Model
import google.generativeai as genai


class GeminiModel(Model):
    def __init__(self, model: str, api_key: str):
        self.model = model
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


    def make_request(self, prompt):
        try:
            if self.model == 'gemini-1.5-flash':
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        # Only one candidate for now.
                        # candidate_count=1,
                        temperature=0,
                    ),                                                         
                )
                translation = response.text

            else:
                response = model.generate_content(
                    prompt                                 
                )
                translation = response.text

            # if self.model == 'gemini-1.5-flash':
            #     response = self.client.chat.completions.create(
            #         model=self.model,
            #         messages=[
            #             {"role": "user", "content": prompt}
            #         ]
            #     )
            #     translation = response.choices[0].message.content.strip()
            # else:
            #     response = self.client.chat.completions.create(
            #         model=self.model,
            #         prompt=prompt,
            #         max_tokens=150,
            #         temperature=0
            #     )
            #     translation = response.choices[0].message.content.strip()

            return translation, True
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求异常：{e}")
        except requests.exceptions.Timeout as e:
            raise Exception(f"请求超时：{e}")
        except simplejson.errors.JSONDecodeError as e:
            raise Exception("Error: response is not valid JSON format.")
        except Exception as e:
            raise Exception(f"发生了未知错误：{e}")
        return "", False
