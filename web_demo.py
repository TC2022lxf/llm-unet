import cv2
import gradio as gr
import os


def image_mod(inputs):
    img = cv2.imread("R-C.jpg")
    return img

demo = gr.Image.upload(fn=image_mod,inputs=[],ouputs="image")

if __name__ == "__main__":
    demo.launch()

