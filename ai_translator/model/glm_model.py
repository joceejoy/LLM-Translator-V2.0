import os
import requests
import simplejson

from model import Model
from zhipuai import ZhipuAI

class GLMModel(Model):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.client = ZhipuAI(api_key=os.getenv("GLM_API_KEY"))

    def make_request(self, prompt):
        try:
            if self.model == 'glm-4-flash':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                translation = response.choices[0].message.content.strip()
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    prompt=prompt,
                    max_tokens=150,
                    temperature=0
                )
                translation = response.choices[0].message.content.strip()
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
