from dotenv import load_dotenv
load_dotenv() ## load all the env variable from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemeni Pro Vision

## to print the list of models 
# for model in genai.list_models():
#     print(model)

model=genai.GenerativeModel('models/gemini-pro-vision')

def get_gemeni_response(input,image, prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit app

st.set_page_config(page_title="Multilingual invoice extraxtor")

st.header("Multilingual invoice extraxtor")
input = st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("choose an image of the invoice...",type=["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit= st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload a image as invoice and you will have to answer any questions based on the uploaded invoice image

"""

## if submit button is clicked

if submit:
    image_data=input_image_details(uploaded_file)
    response = get_gemeni_response(input_prompt, image_data,input)
    st.subheader("The response is: ")
    st.write(response)