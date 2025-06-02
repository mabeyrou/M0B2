import streamlit as st
from loguru import logger
import requests

logger.remove()

logger.add("logs/dev_streamlit.log",
          rotation="10 MB",
          retention="7 days",
          compression="zip",
          level="TRACE",
          enqueue=True,
          format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

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

def describe_snapshot():
    response = requests.get(url=f'{API_URL}/description')

    return response.json()

def main():
    st.header('Live Object Recognition App')

    is_active = get_cam_status().get('is_active')


    st.markdown('✅ Webcam ON' if is_active else '❌ Webcam OFF')


    if is_active:
        st.image(image=f'{API_URL}/stream')
        st.button(label='⏹️ Stop', on_click=lambda:stop_cam())
    else:
        st.empty()
        st.button(label='▶️ Start', on_click=lambda:start_cam())

    with st.form('snapshot'):
        submitted = st.form_submit_button(label='📸 Snapshot', disabled=not is_active)
        if submitted:
            description = describe_snapshot()
            st.write(description.get('description'))
    

if __name__ == "__main__":
    main()
