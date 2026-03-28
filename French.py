import streamlit as st
import random

# 1. 词库
VOCAB = [
    ["🥐", "Croissant", "羊角面包"], ["☕", "Café", "咖啡"], ["🥖", "Baguette", "法棍"],
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🍳", "Œuf", "鸡蛋"],
    ["🚗", "Voiture", "汽车"], ["🚲", "Vélo", "自行车"], ["🏠", "Maison", "房子"],
    ["🏙️", "Ville", "城市"], ["🍎", "Pomme", "苹果"], ["🐱", "Chat", "猫"]
]

# 2. 页面配置
st.set_page_config(page_title="Lille", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 80px; font-size: 30px !important; 
        border-radius: 20px; border: 2px solid #002395; 
    }
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 130px; }
    .fr-font { font-size: 70px; font-weight: bold; color: #002395; margin: 10px 0; cursor: pointer; }
    .cn-font { font-size: 35px; color: #666; }
    .play-btn { 
        background-color: #002395; color: white; padding: 15px 30px; 
        border-radius: 50px; font-size: 20px; border: none; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 逻辑
if 'item' not in st.session_state:
    st.session_state.item = None

if st.button("🇫🇷 抽取新单词"):
    st.session_state.item = random.choice(VOCAB)

if st.session_state.item:
    icon, fr, cn = st.session_state.item
    
    st.markdown(f"""
        <div class="result-container">
            <div class="emoji-font">{icon}</div>
            <div class="fr-font" id="fr-text">{fr}</div>
            <div class="cn-font">{cn}</div>
            
            <button class="play-btn" onclick="speak()">🔊 听发音 (Écouter)</button>
        </div>

        <script>
        function speak() {{
            var msg = new SpeechSynthesisUtterance();
            msg.text = "{fr}";
            msg.lang = 'fr-FR'; // 设置为地道法语
            msg.rate = 0.8;      // 语速稍慢
            window.speechSynthesis.speak(msg);
        }}
        // 尝试自动播放（部分手机支持）
        setTimeout(speak, 500);
        </script>
    """, unsafe_allow_html=True)
