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

# 获取全部 Emoji 列表（包含 3000+ 符号）
ALL_EMOJIS = list(emoji.EMOJI_DATA.keys())

# 2. 语音生成函数
async def get_voice_b64(text):
    # 使用地道的 Eloise 女声
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural", rate="-5%")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return base64.b64encode(audio_data).decode()

# 3. 样式配置 (极致简约)
st.set_page_config(page_title="Lille Infinity", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    /* 按钮只留一个 🇫🇷 */
    .stButton>button { 
        width: 120px; height: 120px; font-size: 70px !important; 
        border-radius: 50%; border: 2px solid #eee; 
        background: #ffffff; margin: 0 auto; display: block;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stButton>button:active { transform: scale(0.95); border-color: #002395; }
    
    .result-container { text-align: center; margin-top: 30px; }
    .emoji-font { font-size: 150px; margin-bottom: 10px; }
    .fr-font { font-size: 65px; font-weight: bold; color: #002395; margin: 10px 0; }
    .cn-font { font-size: 30px; color: #666; margin-top: 0px; }
    audio { display: block; margin: 20px auto; width: 280px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 逻辑处理
# 居中放置按钮
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    btn_clicked = st.button("🇫🇷")

# 预设展示位
emoji_spot = st.empty()
text_spot = st.empty()
audio_spot = st.empty()

if btn_clicked:
    # 彻底盲抽
    icon = random.choice(ALL_EMOJIS)
    
    # 立即展示图标，文字区域显示加载状态
    emoji_spot.markdown(f'<div class="result-container"><div class="emoji-font">{icon}</div></div>', unsafe_allow_html=True)
    text_spot.markdown(f'<div class="result-container"><div class="cn-font">正在翻译...</div></div>', unsafe_allow_html=True)
    
    try:
        # AI 实时翻译这个随机 Emoji
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
        else:
            text_spot.error("这个符号太神秘了，再抽一个！")
            
    except Exception as e:
        text_spot.warning("网络开小差了，再试一次吧")

else:
    # 初始状态什么都不显示，或者只显示一个小提示
    st.markdown("<p style='text-align:center; color:#ddd; margin-top:50px;'>点击 🇫🇷 开始无限挑战</p>", unsafe_allow_html=True)
