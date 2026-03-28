import streamlit as st
import random

# 1. 词库 (保持之前的扩充内容)
VOCAB = [
    ["🥐", "Croissant", "羊角面包"], ["☕", "Café", "咖啡"], ["🥖", "Baguette", "法棍"],
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🍳", "Œuf", "鸡蛋"],
    ["🚗", "Voiture", "汽车"], ["🚲", "Vélo", "自行车"], ["🏠", "Maison", "房子"],
    ["🏙️", "Ville", "城市"], ["🍎", "Pomme", "苹果"], ["🐱", "Chat", "猫"]
]

# 2. 页面样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 80px; font-size: 30px !important; 
        border-radius: 20px; border: 2px solid #002395; background-color: #f8f9fa;
    }
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 130px; margin-bottom: 0px;}
    .fr-font { font-size: 70px; font-weight: bold; color: #002395; margin: 0px; }
    .cn-font { font-size: 35px; color: #666; margin-bottom: 20px;}
    
    /* 播放按钮样式 */
    .play-btn { 
        background-color: #002395; color: white; padding: 15px 40px; 
        border-radius: 50px; font-size: 22px; border: none; cursor: pointer;
        width: 280px; display: block; margin: 20px auto;
    }
    .play-btn:active { background-color: #001a70; transform: scale(0.95); }
    </style>
    """, unsafe_allow_html=True)

# 3. 核心交互
if 'item' not in st.session_state:
    st.session_state.item = None

if st.button("🇫🇷 抽取新单词"):
    st.session_state.item = random.choice(VOCAB)

if st.session_state.item:
    icon, fr, cn = st.session_state.item
    
    # 渲染结果 + 注入 JavaScript 播放脚本
    # 注意：这里的 unsafe_allow_html=True 是关键！
    st.markdown(f"""
        <div class="result-container">
            <div class="emoji-font">{icon}</div>
            <p class="fr-font">{fr}</p>
            <p class="cn-font">{cn}</p>
            
            <button class="play-btn" onclick="speak()">🔊 听发音 (Écouter)</button>
        </div>

        <script>
        function speak() {{
            // 每次点击创建一个新的语音对象
            const msg = new SpeechSynthesisUtterance();
            msg.text = "{fr}";
            msg.lang = 'fr-FR';  // 设置为标准法语
            msg.rate = 0.8;      // 语速稍慢，方便听清
            msg.pitch = 1.0;     // 音调
            
            // 执行播放
            window.speechSynthesis.cancel(); // 先停止之前的发音
            window.speechSynthesis.speak(msg);
        }}
        // 尝试加载后稍微延迟自动播一次
        setTimeout(speak, 300);
        </script>
    """, unsafe_allow_html=True)

else:
    st.markdown("<h3 style='text-align:center; color:#ccc; margin-top:100px;'>点按国旗开始</h3>", unsafe_allow_html=True)
