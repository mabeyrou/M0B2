import streamlit as st
from loguru import logger
import requests

API_URL = 'http://localhost:8000/api/webcam'

def get_cam_status():
    response = requests.get(url=f'{API_URL}/status')

    return response.json()

def start_cam():
    response = requests.get(url=f'{API_URL}/start')

    return response.json()

def stop_cam():
    response = requests.get(url=f'{API_URL}/stop')

    return response.json()

st.header('Live Object Recognition App')

is_active = get_cam_status().get('is_active')

st.markdown('✅' if is_active else '❌')

st.button(label='Start', on_click=lambda:start_cam())
st.button(label='Stop', on_click=lambda:stop_cam())

if is_active:
    st.image(image=f'{API_URL}/stream')