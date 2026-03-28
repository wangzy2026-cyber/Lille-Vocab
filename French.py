import streamlit as st
import random

# 1. 精选词库 (先放一部分测试)
VOCAB = [
    ["🥐", "Croissant", "羊角面包"], ["☕", "Café", "咖啡"], ["🥖", "Baguette", "法棍"],
    ["🐱", "Chat", "猫"], ["🐶", "Chien", "狗"], ["🚗", "Voiture", "汽车"],
    ["🏠", "Maison", "房子"], ["☀️", "Soleil", "太阳"], ["🍎", "Pomme", "苹果"]
]

# 2. 样式：强制清除所有边距，让按钮铺满
st.set_page_config(page_title="Lille", page_icon="🇫🇷", layout="centered")

st.markdown("""
    <style>
    /* 隐藏所有干扰项 */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .reportview-container .main .block-container {padding-top: 0rem;}
    
    /* 按钮基础样式 */
    div.stButton > button:first-child {
        width: 100%;
        height: 150px;
        font-size: 100px !important;
        border-radius: 30px;
        border: 2px solid #002395;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* 结果展示样式 */
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 150px; }
    .fr-font { font-size: 80px; font-weight: bold; color: #002395; margin: 10px 0; }
    .cn-font { font-size: 40px; color: #666; }
    </style>
    """, unsafe_allow_html=True)

# 3. 逻辑控制
# 初始化 session_state 防止页面刷新丢失数据
if 'current_item' not in st.session_state:
    st.session_state.current_item = None

if st.button("🇫🇷"):
    st.session_state.current_item = random.choice(VOCAB)

# 渲染部分
if st.session_state.current_item:
    icon, fr, cn = st.session_state.current_item
    
    st.markdown(f"""
        <div class="result-container">
            <div class="emoji-font">{icon}</div>
            <div class="fr-font">{fr}</div>
            <div class="cn-font">{cn}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 🔊 语音：直接嵌入 HTML5 Audio 标签，确保手机端兼容
    # 加入了随机数 v 防止缓存
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={fr}&tl=fr&client=tw-ob&v={random.random()}"
    st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <audio controls autoplay name="media" style="width: 280px;">
                <source src="{tts_url}" type="audio/mpeg">
            </audio>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<h3 style='text-align:center; color:#ccc; margin-top:100px;'>点击国旗开始</h3>", unsafe_allow_html=True)
