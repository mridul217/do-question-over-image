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

model=genai.GenerativeModel('models/gemini-1.5-flash')

def get_gemeni_response(input,image, prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

# def input_image_details(uploaded_file):
#     if uploaded_file is not None:
#         bytes_data = uploaded_file.getvalue()

#         image_parts=[
#             {
#                 "mime_type": uploaded_file.type,
#                 "data": bytes_data
#             }
#         ]
#                 # Add support for PDF files
#         if uploaded_file.type == 'application/pdf':
#             # You can perform additional processing for PDFs if needed
#             image_parts[0]['is_pdf'] = True

#         return image_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

def input_file_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        file_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]

        # Check if the uploaded file is an image
        if uploaded_file.type.startswith('image/'):
            try:
                image = Image.open(BytesIO(bytes_data))
                file_parts[0]['is_image'] = True
                file_parts[0]['image_size'] = image.size  # Optionally get image size
            except UnidentifiedImageError:
                raise ValueError("Uploaded file is not a valid image.")

        # Check if the uploaded file is a PDF
        elif uploaded_file.type == 'application/pdf':
            file_parts[0]['is_pdf'] = True
            # You can add more processing for PDFs if needed

        else:
            raise ValueError("Unsupported file type.")

        return file_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit app

st.set_page_config(page_title="Multilingual invoice extraxtor")

st.header("Multilingual invoice extraxtor")
input = st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("choose an image of the invoice...",type=["jpg","jpeg","png","pdf"])
image = ""
# if uploaded_file is not None:
#     image=Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image.", use_column_width=True)
if uploaded_file is not None:
    # Handle image files
    if uploaded_file.type.startswith('image/'):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Handle PDF files
    elif uploaded_file.type == 'application/pdf':
        st.write("Uploaded PDF file. Please process the PDF as needed.")
        # You can implement PDF processing logic here (e.g., extract text)

    else:
        st.error("Unsupported file type.")


submit= st.button("Tell me about the invoice")

input_prompt="""
I will upload pdf document, you are perfect in analysing and giving response. you need to provide the concise information related to the query.
"""
# You are an expert in understanding invoices. We will upload a image as invoice and you will have to answer any questions based on the uploaded invoice image

## if submit button is clicked

if submit:
    image_data=input_file_details(uploaded_file)
    response = get_gemeni_response(input_prompt, image_data,input)
    st.subheader("The response is: ")
    st.write(response)


