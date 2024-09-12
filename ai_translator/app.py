from argparse import ArgumentParser
import gradio as gr
import os

from model.openai_model import OpenAIModel
from model.glm_model import GLMModel
from model.gemini_model import GeminiModel
from utils.config_loader import ConfigLoader
from utils.argument_parser import ArgumentParser
from translator.pdf_translator import PDFTranslator


def translate_file(file, model_type, format,language,page_num):

    # Initialize the model with API key
    if model_type == 'gemini-1.5-flash':
        model = GeminiModel(model=model_type, api_key=api_keys.get(model_type))
    elif model_type == 'gpt-3.5-turbo':
        model = OpenAIModel(model=model_type, api_key=api_keys.get(model_type))
    elif model_type =='glm-4-flash':
        model = GLMModel(model=model_type, api_key=api_keys.get(model_type))
    # Get the PDF file input path
    file_path = file.name
    print(
        f"pdf_file_path={file_path}, file_format={format}, target_language={language}, pages={page_num}")


    translator =PDFTranslator(model)

    if page_num is None:
        page_num = 1
    
    # Translate the file using the backend logic
    output_file_path = f"{file_path}_translated.{format}"
    translator.translate_pdf(file_path,format,language,output_file_path,page_num)


    # return file_path
    return output_file_path

def launch_gradio():
    with gr.Blocks() as demo:
        gr.Markdown(f'''# LLM Translator V2.0''')
        with gr.Row():
            file_input = gr.File(label="Upload PDF")
            file_output = gr.File(label="Download Translated File")

        with gr.Row():
            with gr.Column(scale=1):
                model_type=gr.Radio(["gemini-1.5-flash", "gpt-3.5-turbo", "glm-4-flash"], label="Choose LLM Model")
                format=gr.Radio(["pdf", "markdown"], label="Choose Output Format")
                language=gr.Radio(["中文"], label="Choose Target Language")
                page_num=gr.Number(label="Number of Pages (optional)", value=1)
                button = gr.Button("Click to translate PDF")
                button.click(
                    fn=translate_file,
                    inputs=[file_input, model_type, format, language, page_num],
                    outputs=[file_output]
                    )
    demo.launch()

if __name__ == "__main__":

    api_keys = {
        "gemini-1.5-flash": os.getenv("GEMINI_API_KEY"),
        "gpt-3.5-turbo": os.getenv("OPENAI_API_KEY"),
        "glm-4-flash": os.getenv("GLM_API_KEY")
    }

    launch_gradio()