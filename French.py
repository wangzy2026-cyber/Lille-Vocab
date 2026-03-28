import streamlit as st
import random
import edge_tts
import asyncio
import base64

# 1. 词库
VOCAB = [
    ["🥐", "Croissant", "羊角面包"], ["☕", "Café", "咖啡"], ["🥖", "Baguette", "法棍"],
    ["🐱", "Chat", "猫"], ["🐶", "Chien", "狗"], ["🚗", "Voiture", "汽车"],
    ["🏠", "Maison", "房子"], ["☀️", "Soleil", "太阳"], ["🍎", "Pomme", "苹果"],
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🚲", "Vélo", "自行车"]
]

# 异步生成语音
async def get_voice_bytes(text):
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural")
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
    return audio_bytes

# 2. 样式
st.set_page_config(page_title="Lille", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    div.stButton > button {
        width: 100px; height: 50px; font-size: 30px !important;
        border-radius: 20px; border: 2px solid #002395;
    }
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 150px; }
    .fr-font { font-size: 80px; font-weight: bold; color: #002395; margin: 10px 0; }
    .cn-font { font-size: 40px; color: #666; }
    </style>
    """, unsafe_allow_html=True)

# 3. 逻辑
if 'item' not in st.session_state:
    st.session_state.item = None

if st.button("🇫🇷"):
    st.session_state.item = random.choice(VOCAB)

if st.session_state.item:
    icon, fr, cn = st.session_state.item
    
    # 渲染文字和图标
    st.markdown(f"""
        <div class="result-container">
            <div class="emoji-font">{icon}</div>
            <div class="fr-font">{fr}</div>
            <div class="cn-font">{cn}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 生成并播放语音 (Edge TTS 不需要梯子)
    try:
        audio_data = asyncio.run(get_voice_bytes(fr))
        st.audio(audio_data, format='audio/mp3', autoplay=True)
    except Exception as e:
        st.write("语音加载中...")
