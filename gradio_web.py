import gradio as gr
import os
import time
from utils.llm import load_llm
from utils.unet import predict


#llm = load_llm()

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def prompt(file):
    pt = "帮我重新简明的分析一下一张菌落图片的分析数据："
    pt += predict(file)
    print(pt)
    return pt
def add_text(history, text):

    history = history + [(text, None)]

    return history, gr.Textbox(value="", interactive=False)


def add_file(history, file):
    history = history + [((file.name,), None)]
    print(history)
    return history


def bot(history):
    response = history[-1][0]
    #response = llm.invoke(response)
    response = "1231231231"
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history

def bot1(history):
    response = prompt(history[-1][0])
    print(response)
    #response = llm.invoke(response)
    response = "1231231231"
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "R-C.jpg"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot, api_name="bot_response"
    )
    txt_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot1, chatbot, chatbot
    )
    # bt = gr.Button("📁")
    # file_msg1 = bt.click(add_file, [chatbot, btn], [chatbot], queue=False)
    chatbot.like(print_like_dislike, None, None)


demo.queue()
demo.launch(share= True)

