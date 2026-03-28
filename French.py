import streamlit as st
from openai import OpenAI
import emoji
import random
import edge_tts
import asyncio
import base64
import io

# 1. 核心配置
client = OpenAI(
    api_key=st.secrets["api_key"], 
    base_url="https://api.deepseek.com"
)

# 异步生成语音函数 (使用微软 Edge 接口)
async def generate_voice(text):
    # fr-FR-EloiseNeural 是一个非常地道的法国女声
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

def get_french_name(emoj_char):
    prompt = f"针对符号 '{emoj_char}'，给出一个法语名词和对应的中文。格式：法语|中文"
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            max_tokens=40
        )
        return response.choices[0].message.content.strip().split("|")
    except:
        return ["Bonjour", "你好"]

# 2. 极致简样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 120px; font-size: 100px; 
        background: none; border: none;
    }
    .emoji-display { font-size: 150px; text-align: center; margin: 10px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 70px; font-weight: bold; }
    .cn-text { text-align: center; color: #666; font-size: 30px; margin-bottom: 20px;}
    audio { display: block; margin: 0 auto; width: 250px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 核心交互
if st.button("🇫🇷"):
    all_emojis = list(emoji.EMOJI_DATA.keys())
    random_emoji = random.choice(all_emojis)
    
    res = get_french_name(random_emoji)
    if len(res) >= 2:
        fr, cn = res[0].strip(), res[1].strip()
        
        # 显示 Emoji 和文字
        st.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="fr-text">{fr}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="cn-text">{cn}</p>', unsafe_allow_html=True)
        
        # 🔊 使用 Edge TTS 生成语音
        try:
            audio_content = asyncio.run(generate_voice(fr))
            b64_audio = base64.b64encode(audio_content).decode()
            
            # 自动播放 HTML
            audio_html = f"""
                <audio autoplay="true" controls>
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
        except Exception as e:
            st.error("语音生成暂时不可用，请稍后再试")
