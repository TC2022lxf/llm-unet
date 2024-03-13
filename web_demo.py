import gradio as gr
import os
import time
import requests
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
    print(history)
    return history, gr.Textbox(value="", interactive=False)


def add_file(history, file):
    history = history + [(("R-C.jpg",), None)]
    print(history)
    return history

def is_TF(pt):
    pt = """如果以下的问题不是要求返回文字回答而是要求返回其他类型，如图片、表格等信息的话，请你回复“True”，否则回复“False”，请你一定要准许这个回复规则，我只想在你的回答中看到一次True或者一次False，不可以都同时出现。
    问题：
    """+pt
    pt = pt+"答案(True or False):"
    response = llm.invoke(pt)
    return response
def bot1(history):
    print(history)
    response = "**That's cool!**"
    if "True" in "True":
        history[-1][1] =("R-C.jpg",)
        print(history)
    return history
def bot(history):
    print(history)
    question = history[-1][0]
    if isinstance(question, tuple):
        if os.path.exists(question[0]):
            print(question[0])
            question = prompt(question[0])
    if "True" in "True":
        history[-1][1] =("R-C.jpg",)
        print(history)
    else:
        print("2")
        response = "llm.invoke(question)"
        history[-1][1] = response
    return history

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
        bot, chatbot, chatbot
    )
    # bt = gr.Button("📁")
    # file_msg1 = bt.click(add_file, [chatbot, btn], [chatbot], queue=False)
    chatbot.like(print_like_dislike, None, None)


demo.queue()
demo.launch(share = True)

