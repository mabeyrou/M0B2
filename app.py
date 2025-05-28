import streamlit as st

st.title('Live Objet Recognition App')

webrtc_streamer(key="streamer", sendback_audio=False)
