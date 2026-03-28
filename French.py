import streamlit as st
import random
import edge_tts
import asyncio
import base64

# 1. 词库 (保持之前的扩充内容)
VOCAB = [
    ["🥐", "Croissant", "羊角面包"], ["☕", "Café", "咖啡"], ["🥖", "Baguette", "法棍"],
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🍳", "Œuf", "鸡蛋"],
    ["🚗", "Voiture", "汽车"], ["🚲", "Vélo", "自行车"], ["🏠", "Maison", "房子"],
    ["🏙️", "Ville", "城市"], ["🍎", "Pomme", "苹果"], ["🐱", "Chat", "猫"]
]

# 2. 页面配置
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    div.stButton > button {
        width: 100%; height: 70px; font-size: 30px !important;
        border-radius: 15px; border: 2px solid #002395;
    }
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 120px; }
    .fr-font { font-size: 60px; font-weight: bold; color: #002395; margin: 10px 0; }
    .cn-font { font-size: 30px; color: #666; }
    /* 让音频播放条更显眼 */
    audio { width: 100%; max-width: 300px; margin: 10px auto; display: block; }
    </style>
    """, unsafe_allow_html=True)

# 3. 核心逻辑
if 'current_item' not in st.session_state:
    st.session_state.current_item = None

# 按钮：抽取新单词
if st.button("🇫🇷 抽取新单词"):
    st.session_state.current_item = random.choice(VOCAB)

if st.session_state.current_item:
    icon, fr, cn = st.session_state.current_item
    
    # 渲染文字
    st.markdown(f"""
        <div class="result-container">
            <div class="emoji-font">{icon}</div>
            <div class="fr-font">{fr}</div>
            <div class="cn-font">{cn}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- 语音处理部分：这是手机端修复的关键 ---
    try:
        # 使用异步函数生成音频
        async def generate_audio():
            communicate = edge_tts.Communicate(fr, "fr-FR-EloiseNeural")
            data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    data += chunk["data"]
            return data

        # 在手机端，我们显式地生成音频
        audio_bytes = asyncio.run(generate_audio())
        
        # 核心改动：不再强求自动播放（autoplay=False）
        # 让用户手动点击播放条上的“播放”按钮，这在手机上是 100% 成功的
        st.audio(audio_bytes, format='audio/mp3', autoplay=False)
        st.info("💡 手机端请手动点击上方播放键发音")
        
    except Exception as e:
        st.warning("语音生成中，请稍后再试...")

else:
    st.markdown("<h3 style='text-align:center; color:#ccc; margin-top:100px;'>点按上方按钮开始</h3>", unsafe_allow_html=True)
