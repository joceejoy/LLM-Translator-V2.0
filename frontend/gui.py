import gradio as gr
import time


# Select the output format: support PDF or Markdown


# Process Upload File
def process_file(pdf_file, progress=gr.Progress()):
    if pdf_file is None:
        return None, "No file uploaded."
    progress(0, desc="Starting process...")
    time.sleep(0.5)  # Simulate some processing time

    # Parse and translate the the PDF file
    progress(0.25, desc="Analyzing and translating content from PDF...")


with gr.Blocks(title="LLM Translator V2.0", theme="Soft") as demo:
    gr.Markdown(f'''# LLM Translator V2.0''')

    with gr.Row():
        # lhs
        with gr.Column(scale=1, min_width=300):
            output_format = gr.Radio(
                ["PDF", "Markdown"], value="Output", label="Output Format")
            file_input = gr.File(label="Upload PDF File",
                                 file_count="multiple")

            translate_button = gr.Button("Translate", interactive=True)
            process_status = gr.Markdown("Upload a file and click 'Translate'")
            retriever_state = gr.State(None)

# def greet(name, intensity):
#     return "Hello " * intensity + name + "!"

# demo = gr.Interface(
#     fn=greet,
#     inputs=["text", "slider"],
#     outputs=["text"],
# )

demo.launch()
# demo.launch(share=True, debug=True)
