import streamlit as st
from openai import OpenAI
import emoji
import random
import base64
import requests

# 1. 核心配置
client = OpenAI(
    api_key=st.secrets["api_key"], 
    base_url="https://api.deepseek.com"
)

# 2. 样式优化
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 120px; font-size: 100px; 
        background: #fafafa; border: 1px solid #eee; border-radius: 20px;
    }
    .emoji-display { font-size: 150px; text-align: center; margin: 10px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 70px; font-weight: bold; }
    .cn-text { text-align: center; color: #666; font-size: 30px; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# 3. 核心逻辑
if st.button("🇫🇷"):
    # 随机选 Emoji
    all_emojis = list(emoji.EMOJI_DATA.keys())
    random_emoji = random.choice(all_emojis)
    
    placeholder = st.empty()
    
    try:
        # 第一步：调用 DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"符号 '{random_emoji}'，法语|中文"}],
            timeout=15
        )
        res = response.choices[0].message.content.strip().split("|")
        
        if len(res) >= 2:
            fr, cn = res[0].strip(), res[1].strip()
            
            # 第二步：使用一个不需要异步库的语音接口 (采用 Google TTS 的直接请求方式)
            # 这种方式不依赖 edge-tts 库的异步逻辑，更稳定
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={fr}&tl=fr&client=tw-ob"
            
            with placeholder.container():
                st.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="fr-text">{fr}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="cn-text">{cn}</p>', unsafe_allow_html=True)
                
                # 语音 HTML (使用原生音频链接)
                audio_html = f"""
                    <audio autoplay="true" controls style="display:block; margin: 0 auto; width: 250px;">
                        <source src="{tts_url}" type="audio/mpeg">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"连接超时，请再试一次 ➜ {e}")
