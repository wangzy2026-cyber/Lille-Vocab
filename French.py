import streamlit as st
from openai import OpenAI
import emoji
import random
import edge_tts
import asyncio
import base64

# 1. 核心配置
client = OpenAI(
    api_key=st.secrets["api_key"], 
    base_url="https://api.deepseek.com"
)

async def generate_voice(text):
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

# 2. 极致简样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    /* 按钮：增加点击时的阴影反馈，让你知道点中了 */
    .stButton>button { 
        width: 100%; height: 120px; font-size: 100px; 
        background: rgba(255,255,255,0.1); 
        border: 1px solid #f0f2f6;
        border-radius: 20px;
        transition: all 0.2s;
    }
    .stButton>button:active { transform: scale(0.95); background: #f0f2f6; }
    
    .emoji-display { font-size: 150px; text-align: center; margin: 10px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 70px; font-weight: bold; line-height: 1.1; }
    .cn-text { text-align: center; color: #666; font-size: 30px; margin-top: 5px; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# 3. 交互逻辑
# 使用 st.button 的原生反馈
if st.button("🇫🇷"):
    # 在加载时显示一个小提示，防止用户觉得没反应
    with st.spinner(''):
        all_emojis = list(emoji.EMOJI_DATA.keys())
        random_emoji = random.choice(all_emojis)
        
        try:
            # 获取翻译
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": f"符号 '{random_emoji}'，法语|中文"}],
                temperature=1.0,
                max_tokens=40
            )
            res = response.choices[0].message.content.strip().split("|")
            
            if len(res) >= 2:
                fr, cn = res[0].strip(), res[1].strip()
                
                # 显示内容
                st.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="fr-text">{fr}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="cn-text">{cn}</p>', unsafe_allow_html=True)
                
                # 🔊 语音：回归稳健的 HTML5 播放，兼容性最强
                audio_content = asyncio.run(generate_voice(fr))
                b64_audio = base64.b64encode(audio_content).decode()
                audio_html = f"""
                    <audio autoplay="true" style="display:none;">
                        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
        except:
            st.error("网络堵塞，再点一下？")
