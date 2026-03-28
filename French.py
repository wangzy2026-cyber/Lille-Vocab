import streamlit as st
from openai import OpenAI
import emoji
import random
import edge_tts
import asyncio
import base64
import time

# 1. 核心配置
client = OpenAI(
    api_key=st.secrets["api_key"], 
    base_url="https://api.deepseek.com"
)

# 异步生成语音
async def generate_voice(text):
    # 改用较快的语音包，缩短生成时间
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# 2. 样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { width: 100%; height: 120px; font-size: 100px; background: none; border: none; }
    .emoji-display { font-size: 150px; text-align: center; margin: 10px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 60px; font-weight: bold; line-height: 1.1; }
    .cn-text { text-align: center; color: #666; font-size: 30px; margin-top: 5px; margin-bottom: 20px;}
    
    /* 调整手机端音频条宽度 */
    div[data-testid="stAudio"] {
        max-width: 280px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 逻辑逻辑
if st.button("🇫🇷"):
    all_emojis = list(emoji.EMOJI_DATA.keys())
    random_emoji = random.choice(all_emojis)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"符号 '{random_emoji}'，法语|中文"}],
            temperature=1.2,
            max_tokens=40
        )
        res = response.choices[0].message.content.strip().split("|")
        
        if len(res) >= 2:
            fr, cn = res[0].strip(), res[1].strip()
            
            st.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
            st.markdown(f'<p class="fr-text">{fr}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="cn-text">{cn}</p>', unsafe_allow_html=True)
            
            # 🔊 语音逻辑优化
            # 1. 异步生成字节流
            audio_content = asyncio.run(generate_voice(fr))
            
            # 2. 直接使用 Streamlit 原生音频组件（它对手机浏览器兼容性更好）
            # 使用时间戳作为 key，强制刷新组件，解决“一直加载”或“播旧语音”的问题
            st.audio(audio_content, format='audio/mp3', autoplay=True)
            
    except Exception as e:
        st.error("网络开小差了，再点一次试试？")
