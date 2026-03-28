import streamlit as st
import random
import edge_tts
import asyncio
import base64
import time
import emoji
from openai import OpenAI

# 1. 配置 DeepSeek (用于翻译全库随机出来的 Emoji)
client = OpenAI(
    api_key=st.secrets["api_key"], 
    base_url="https://api.deepseek.com"
)

# 2. 核心词库 (保留你最稳的基础词)
BASE_VOCAB = [
    ["🥐", "Croissant", "羊角面包"], ["🥖", "Baguette", "法棍"], ["☕", "Café", "咖啡"], 
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🍳", "Œuf", "鸡蛋"], 
    ["🏠", "Maison", "房子"], ["🏙️", "Ville", "城市"], ["🏫", "École", "学校"]
    # ... 其他 150 个词建议也保留在代码里作为“高频保底”
]

# 获取全部 Emoji 列表
ALL_EMOJIS = list(emoji.EMOJI_DATA.keys())

# 3. 语音生成逻辑
async def get_voice_b64(text):
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural", rate="-5%")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return base64.b64encode(audio_data).decode()

# 4. 样式配置
st.set_page_config(page_title="Lille Infinity", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 75px; font-size: 30px !important; 
        border-radius: 20px; border: 2px solid #002395; 
        background: #f8f9fa; color: #002395; font-weight: bold;
    }
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 130px; margin-bottom: 0px; }
    .fr-font { font-size: 65px; font-weight: bold; color: #002395; margin: 5px 0; }
    .cn-font { font-size: 32px; color: #666; margin-top: 0px; }
    audio { display: block; margin: 15px auto; width: 280px; }
    </style>
    """, unsafe_allow_html=True)

# 占位符
emoji_p = st.empty()
text_p = st.empty()
audio_p = st.empty()

# 5. 核心逻辑
if st.button("🇫🇷 开启无限法语盲盒"):
    # 80% 概率抽基础词，20% 概率抽全库盲盒
    if random.random() > 0.2:
        icon, fr, cn = random.choice(BASE_VOCAB)
    else:
        # 从 3000 个 Emoji 里盲抽
        icon = random.choice(ALL_EMOJIS)
        try:
            # 实时问 AI 这个 Emoji 怎么说
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": f"符号 '{icon}'，给出一个法语名词和中文。格式：法语|中文"}],
                timeout=5
            )
            res = response.choices[0].message.content.strip().split("|")
            fr, cn = (res[0], res[1]) if len(res) >= 2 else ("?", "?")
        except:
            fr, cn = "Erreur", "网络小卡顿"

    # 更新 UI
    emoji_p.markdown(f'<div class="result-container"><div class="emoji-font">{icon}</div></div>', unsafe_allow_html=True)
    text_p.markdown(f'<div class="result-container"><div class="fr-font">{fr}</div><div class="cn-font">{cn}</div></div>', unsafe_allow_html=True)
    
    # 音频处理
    audio_p.empty()
    nonce = str(time.time()).replace(".", "")
    try:
        b64_str = asyncio.run(get_voice_b64(fr))
        audio_html = f"""
            <div style="display: flex; justify-content: center;">
                <audio controls autoplay id="audio_{nonce}">
                    <source src="data:audio/mp3;base64,{b64_str}" type="audio/mp3">
                </audio>
            </div>
            <script>
                setTimeout(() => {{ document.getElementById('audio_{nonce}').play(); }}, 150);
            </script>
        """
        audio_p.markdown(audio_html, unsafe_allow_html=True)
    except:
        audio_p.info("语音加载中...")
