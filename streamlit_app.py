import streamlit as st
from google.cloud import vision
from google.oauth2 import service_account
from PIL import Image
import io

def get_vision_client():
    credentials_info = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    return client

client = get_vision_client()

st.title('Food Image Detection')

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Classifying...")

    content = io.BytesIO()
    image.save(content, format="JPEG")
    content = content.getvalue()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    dish_names = [label.description for label in labels]
    st.write("Detected dishes:")
    st.write(dish_names)
s