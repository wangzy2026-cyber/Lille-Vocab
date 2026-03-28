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
    .stButton>button { width: 100%; height: 120px; font-size: 100px; background: none; border: none; }
    .emoji-display { font-size: 150px; text-align: center; margin: 10px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 70px; font-weight: bold; }
    .cn-text { text-align: center; color: #666; font-size: 30px; margin-bottom: 20px;}
    audio { display: none; } /* 隐藏播放条，让它看起来更像原生 App */
    </style>
    """, unsafe_allow_html=True)

# 3. 核心交互
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
            
            # 生成音频
            audio_content = asyncio.run(generate_voice(fr))
            b64_audio = base64.b64encode(audio_content).decode()
            
            # --- 强力 JS 自动播放逻辑 ---
            # 通过生成一个唯一的 ID 并利用 JS 的 play() 方法强制执行
            audio_id = f"audio_{int(time.time())}"
            audio_html = f"""
                <audio id="{audio_id}">
                    <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
                <script>
                    var audio = document.getElementById('{audio_id}');
                    audio.play().catch(function(error) {{
                        console.log("浏览器拦截了自动播放，尝试静音播放后唤醒或等待用户再次交互");
                    }});
                </script>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            
    except Exception as e:
        st.error("再点一次试试")
