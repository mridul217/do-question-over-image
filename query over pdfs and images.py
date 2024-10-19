from dotenv import load_dotenv
load_dotenv()  # Load all the env variables from .env

import streamlit as st
import os
from PIL import Image
from io import BytesIO
import google.generativeai as genai
import PyPDF2

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('models/gemini-1.5-flash')

def get_gemeni_response(input_text, image, prompt):
    # Prepare content for the model
    contents = [input_text]
    if image:
        contents.append(image)
    contents.append(prompt)
    
    response = model.generate_content(contents)
    return response.text

def extract_text_from_pdf(pdf_bytes):
    # Extract text from PDF using PyPDF2
    text = ""
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"  # Adding a newline for separation
    return text.strip()  # Remove trailing whitespace

def input_file_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        # Check if the uploaded file is an image
        if uploaded_file.type.startswith('image/'):
            try:
                image = Image.open(BytesIO(bytes_data))
                return image  # Return the PIL image
            except UnidentifiedImageError:
                raise ValueError("Uploaded file is not a valid image.")

        # Check if the uploaded file is a PDF
        elif uploaded_file.type == 'application/pdf':
            text_content = extract_text_from_pdf(bytes_data)
            return text_content  # Return extracted text

        else:
            raise ValueError("Unsupported file type.")
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit app

st.set_page_config(page_title="Multilingual Invoice Extractor")

st.header("Multilingual Invoice Extractor")
input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png", "pdf"])

image = None
pdf_text = None

if uploaded_file is not None:
    # Handle image files
    if uploaded_file.type.startswith('image/'):
        image = input_file_details(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Handle PDF files
    elif uploaded_file.type == 'application/pdf':
        pdf_text = input_file_details(uploaded_file)
        st.write("Uploaded PDF file. Extracted text:")
        st.text_area("PDF Text", pdf_text, height=300)

submit = st.button("Tell me about the invoice")

# If the submit button is clicked
if submit:
    if image is not None:
        response = get_gemeni_response(input_prompt, image, "Analyze the invoice.")
        st.subheader("The response is: ")
        st.write(response)
    elif pdf_text is not None:
        response = get_gemeni_response(input_prompt, pdf_text, "Analyze the invoice.")
        st.subheader("The response is: ")
        st.write(response)
    else:
        st.error("Please upload an image or PDF file.")
