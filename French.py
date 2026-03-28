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

# 简化语音生成：直接返回 base64 字符串
def get_voice_b64(text):
    async def _generate():
        communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return base64.b64encode(audio_data).decode()
    
    # 在同步环境下运行异步任务的稳妥方法
    return asyncio.run(_generate())

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

# 3. 核心交互
if st.button("🇫🇷"):
    # 随机选 Emoji
    all_emojis = list(emoji.EMOJI_DATA.keys())
    random_emoji = random.choice(all_emojis)
    
    # 占位符：先清空之前的，再放新的
    display_area = st.empty()
    
    try:
        # 第一步：调 DeepSeek (加个超时控制)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"符号 '{random_emoji}'，法语|中文"}],
            timeout=10 
        )
        res = response.choices[0].message.content.strip().split("|")
        
        if len(res) >= 2:
            fr, cn = res[0].strip(), res[1].strip()
            
            # 第二步：生成语音
            b64_audio = get_voice_b64(fr)
            
            # 第三步：一次性渲染所有内容
            with display_area.container():
                st.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="fr-text">{fr}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="cn-text">{cn}</p>', unsafe_allow_html=True)
                
                # 语音 HTML
                audio_html = f"""
                    <audio autoplay="true" controls style="display:block; margin: 0 auto; width: 250px;">
                        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"出错啦: {e}")
