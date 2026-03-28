import streamlit as st
import random
import streamlit.components.v1 as components

# 1. 词库
VOCAB = [
    ["🥐", "Croissant", "羊角面包"], ["☕", "Café", "咖啡"], ["🥖", "Baguette", "法棍"],
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🍳", "Œuf", "鸡蛋"],
    ["🚗", "Voiture", "汽车"], ["🚲", "Vélo", "自行车"], ["🏠", "Maison", "房子"],
    ["🏙️", "Ville", "城市"], ["🍎", "Pomme", "苹果"], ["🐱", "Chat", "猫"]
]

# 2. 样式
st.set_page_config(page_title="Lille", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 80px; font-size: 30px !important; 
        border-radius: 20px; border: 2px solid #002395; 
    }
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 130px; margin-bottom: 0px;}
    .fr-font { font-size: 70px; font-weight: bold; color: #002395; margin: 0px; }
    .cn-font { font-size: 35px; color: #666; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# 3. 逻辑
if 'item' not in st.session_state:
    st.session_state.item = None

if st.button("🇫🇷 抽取新单词"):
    st.session_state.item = random.choice(VOCAB)

if st.session_state.item:
    icon, fr, cn = st.session_state.item
    
    # 渲染基础内容
    st.markdown(f"""
        <div class="result-container">
            <div class="emoji-font">{icon}</div>
            <p class="fr-font">{fr}</p>
            <p class="cn-font">{cn}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 🔊 语音组件：使用 components.v1.html 确保 JS 正常运行
    js_code = f"""
        <div style="display: flex; justify-content: center;">
            <button id="speak-btn" style="
                background-color: #002395; color: white; padding: 15px 40px; 
                border-radius: 50px; font-size: 22px; border: none; cursor: pointer;
                width: 250px; font-family: sans-serif;
            ">🔊 听发音 (Écouter)</button>
        </div>

        <script>
        const btn = document.getElementById('speak-btn');
        const synth = window.speechSynthesis;

        btn.onclick = () => {{
            if (synth.speaking) {{ synth.cancel(); }}
            const utter = new SpeechSynthesisUtterance("{fr}");
            utter.lang = 'fr-FR';
            utter.rate = 0.8;
            synth.speak(utter);
        }};
        
        // 自动尝试播一次
        setTimeout(() => btn.click(), 500);
        </script>
    """
    # 渲染这个带有 JS 的 HTML 组件
    components.html(js_code, height=100)

else:
    st.markdown("<h3 style='text-align:center; color:#ccc; margin-top:100px;'>点按国旗开始</h3>", unsafe_allow_html=True)
