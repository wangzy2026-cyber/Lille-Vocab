import streamlit as st
import random
import edge_tts
import asyncio
import base64
import time
import emoji
from openai import OpenAI

# 1. 核心配置
client = OpenAI(
    api_key=st.secrets["api_key"], 
    base_url="https://api.deepseek.com"
)

# 获取全部 Emoji 列表
ALL_EMOJIS = list(emoji.EMOJI_DATA.keys())

# 2. 语音生成函数
async def get_voice_b64(text):
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural", rate="-5%")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return base64.b64encode(audio_data).decode()

# 3. 样式配置
st.set_page_config(page_title="Lille Infinity", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    /* 居中大按钮 */
    .stButton { display: flex; justify-content: center; margin-top: 50px; }
    .stButton>button { 
        width: 120px; height: 120px; font-size: 70px !important; 
        border-radius: 50%; border: 1px solid #eee; 
        background: #ffffff; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    .stButton>button:active { transform: scale(0.9); border-color: #002395; }
    
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 150px; margin-bottom: 0px; }
    .fr-font { font-size: 65px; font-weight: bold; color: #002395; margin: 5px 0; }
    .cn-font { font-size: 30px; color: #666; margin-top: 0px; }
    audio { display: block; margin: 15px auto; width: 280px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 逻辑处理
# 创建占位符
emoji_spot = st.empty()
text_spot = st.empty()
audio_spot = st.empty()

# 按钮触发
if st.button("🇫🇷"):
    icon = random.choice(ALL_EMOJIS)
    
    # 立即展示图标
    emoji_spot.markdown(f'<div class="result-container"><div class="emoji-font">{icon}</div></div>', unsafe_allow_html=True)
    text_spot.markdown(f'<div class="result-container"><div class="cn-font">...</div></div>', unsafe_allow_html=True)
    
    try:
        # AI 实时翻译
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"符号 '{icon}'，给出最贴切的一个法语名词和中文。格式：法语|中文"}],
            timeout=8
        )
        res = response.choices[0].message.content.strip().split("|")
        
        if len(res) >= 2:
            fr, cn = res[0].strip(), res[1].strip()
            
            # 更新文字
            text_spot.markdown(f'<div class="result-container"><div class="fr-font">{fr}</div><div class="cn-font">{cn}</div></div>', unsafe_allow_html=True)
            
            # 生成并注入音频
            audio_spot.empty()
            nonce = str(time.time()).replace(".", "")
            b64_str = asyncio.run(get_voice_b64(fr))
            
            audio_html = f"""
                <div style="display: flex; justify-content: center;">
                    <audio controls autoplay id="audio_{nonce}">
                        <source src="data:audio/mp3;base64,{b64_str}" type="audio/mp3">
                    </audio>
                </div>
                <script>
                    setTimeout(() => {{ 
                        var a = document.getElementById('audio_{nonce}');
                        if(a) a.play();
                    }}, 200);
                </script>
            """
            audio_spot.markdown(audio_html, unsafe_allow_html=True)
            
    except:
        text_spot.warning("网络卡顿，请重试")
