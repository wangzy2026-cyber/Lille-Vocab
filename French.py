import streamlit as st
from openai import OpenAI
import emoji
import random
from gtts import gTTS
import io

# 1. 核心配置
client = OpenAI(
    api_key=st.secrets["api_key"], 
    base_url="https://api.deepseek.com"
)

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
    except Exception as e:
        return [f"Error: {str(e)}", "错误"]

# 2. 样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { width: 100%; height: 100px; font-size: 80px; background: none; border: none; }
    .emoji-display { font-size: 150px; text-align: center; margin: 10px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 70px; font-weight: bold; }
    .cn-text { text-align: center; color: #666; font-size: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 逻辑
if st.button("🇫🇷"):
    all_emojis = list(emoji.EMOJI_DATA.keys())
    random_emoji = random.choice(all_emojis)
    
    res = get_french_name(random_emoji)
    if len(res) >= 2:
        fr, cn = res[0].strip(), res[1].strip()
        
        st.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="fr-text">{fr}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="cn-text">{cn}</p>', unsafe_allow_html=True)
        
        # --- 语音调试核心区 ---
        try:
            tts = gTTS(text=fr, lang='fr')
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            # 这里的 getvalue() 很关键
            st.audio(audio_bytes.getvalue(), format='audio/mp3', autoplay=True)
        except Exception as e:
            # 如果没声音，这里会显示具体的报错信息
            st.warning(f"语音生成失败，原因: {e}")
