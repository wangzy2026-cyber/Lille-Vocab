import streamlit as st
from openai import OpenAI
import emoji
import random

# 1. 核心配置
try:
    client = OpenAI(
        api_key=st.secrets["api_key"], 
        base_url="https://api.deepseek.com"
    )
except Exception as e:
    st.error(f"Secrets 配置错误: {e}")

# 2. 极致简样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 120px; font-size: 100px; 
        background: #fdfdfd; border: 1px solid #eee; border-radius: 20px;
    }
    .emoji-display { font-size: 150px; text-align: center; margin: 10px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 60px; font-weight: bold; }
    .cn-text { text-align: center; color: #666; font-size: 30px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 核心交互逻辑
if st.button("🇫🇷"):
    # 第一步：瞬间选出一个 Emoji 并显示（不等待 API，确保点完就有反应）
    all_emojis = list(emoji.EMOJI_DATA.keys())
    random_emoji = random.choice(all_emojis)
    
    # 创建三个占位符，按顺序填入
    emoji_spot = st.empty()
    text_spot = st.empty()
    audio_spot = st.empty()
    
    # 先把图标甩出来
    emoji_spot.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
    
    # 第二步：尝试获取翻译
    try:
        # 增加超时控制，防止死锁
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"符号 '{random_emoji}'，法语|中文"}],
            timeout=8
        )
        res = response.choices[0].message.content.strip().split("|")
        
        if len(res) >= 2:
            fr, cn = res[0].strip(), res[1].strip()
            
            # 填入文字
            text_spot.markdown(f'<p class="fr-text">{fr}</p><p class="cn-text">{cn}</p>', unsafe_allow_html=True)
            
            # 第三步：填入语音 (Google TTS 接口，国内可用)
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={fr}&tl=fr&client=tw-ob"
            audio_spot.audio(tts_url, format='audio/mp3', autoplay=True)
            
    except Exception as e:
        # 如果 API 超时或报错，至少显示个提示
        text_spot.markdown(f'<p class="cn-text">网络连接中... ({str(e)[:20]})</p>', unsafe_allow_html=True)
