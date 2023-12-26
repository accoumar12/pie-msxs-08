import gradio as gr

import argparse
import logging

from utils.utils import load_model, generate_answer
from utils.constants import MODEL_NAMES, DEFAULT_MODEL, PRECISIONS, DEFAULT_PRECISION


# ---------------------------------------------------------------------------
# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# ---------------------------------------------------------------------------
# predict function for gradio's chat interface
def predict(message, history, model_name):
    yield from generate_answer(model_name, message, history)


# ---------------------------------------------------------------------------
# Gradio app
def gradio_app():
    global model, tokenizer
    model, tokenizer = None, None

    # Create a Gradio Chatbat Interface
    with gr.Blocks() as iface:
        with gr.Tab("Teacher Assistant"):
            gr.ChatInterface(
                predict,
                additional_inputs=[model_name_chosen],
            )

        with gr.Tab("Model choice and Options"):
            model_name_chosen = gr.Dropdown(
                choices=MODEL_NAMES,
                value=DEFAULT_MODEL,
                label="Choose a model",
            )
            precision_chosen = gr.Dropdown(
                choices=PRECISIONS,
                value=DEFAULT_PRECISION,
                label="Choose a quantization precision (HF-models only)",
            )
            gpu_layers_chosen = gr.Slider(
                minimum=0,
                maximum=50,
                step=1,
                info="#layers to off-load on GPU (GGUF-models only)",
            )
            b1 = gr.Button("Load model")
            b1.click(
                load_model,
                inputs=[model_name_chosen, precision_chosen, gpu_layers_chosen],
            )

    # Launch Gradio Interface
    logger.info("Launching Gradio Interface...")
    iface.launch()


# ---------------------------------------------------------------------------
# CLI entrypoint
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web-app to interact with a LLM")
    gradio_app()
