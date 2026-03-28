import streamlit as st
from openai import OpenAI
import emoji
import random
import os

# 1. 核心配置
client = OpenAI(
    api_key="sk-a54eade075e6408a9f1f32a1a3181f0e", 
    base_url="https://api.deepseek.com"
)

def get_french_name(emoj_char):
    prompt = f"针对符号 '{emoj_char}'，给出一个法语名词和中文。格式：法语|中文"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip().split("|")
    except:
        return ["Bonjour", "你好"]

# 2. 极致简样式
st.set_page_config(page_title="Lille", page_icon="🇫🇷")
st.markdown("""
    <style>
    /* 隐藏所有系统 UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* 按钮样式：纯透明底色，只有国旗 */
    .stButton>button { 
        width: 100%; 
        height: 150px; 
        font-size: 100px; 
        background: none; 
        border: none;
        box-shadow: none;
    }
    .stButton>button:active { background: none; }
    
    .emoji-display { font-size: 180px; text-align: center; margin: 20px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 90px; font-weight: bold; }
    .cn-text { text-align: center; color: #666; font-size: 40px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 核心交互
# 使用 container 确保布局干净
container = st.container()

if st.button("🇫🇷"):
    # 随机抽取一个 Emoji
    all_emojis = list(emoji.EMOJI_DATA.keys())
    random_emoji = random.choice(all_emojis)
    
    # 获取翻译
    res = get_french_name(random_emoji)
    if len(res) >= 2:
        fr, cn = res[0], res[1]
        
        # 直接显示内容，不带任何 loading 提示
        container.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
        container.markdown(f'<p class="fr-text">{fr}</p>', unsafe_allow_html=True)
        container.markdown(f'<p class="cn-text">{cn}</p>', unsafe_allow_html=True)
        
        # 🔊 Mac 系统原生发音 (Thomas 是地道的男声)
        os.system(f"say -v Thomas '{fr}'")