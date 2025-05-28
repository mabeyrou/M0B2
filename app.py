import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("OpenCV Filters on Video Stream")

webrtc_streamer(key="streamer", sendback_audio=False)
