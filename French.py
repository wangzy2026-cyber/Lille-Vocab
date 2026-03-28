import streamlit as st
from openai import OpenAI
import emoji
import random

# 1. 核心配置
client = OpenAI(
    api_key=st.secrets["api_key"], 
    base_url="https://api.deepseek.com"
)

# 2. 页面样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 120px; font-size: 100px; 
        background: #fdfdfd; border: 1px solid #eee; border-radius: 20px;
    }
    .emoji-display { font-size: 150px; text-align: center; margin: 10px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 65px; font-weight: bold; line-height: 1.1; }
    .cn-text { text-align: center; color: #666; font-size: 28px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 交互逻辑
if st.button("🇫🇷"):
    # --- 第一步：瞬间随机抽取 Emoji ---
    # 我们从 emoji 库里随机抓一个真正的图标
    emoji_list = list(emoji.EMOJI_DATA.keys())
    random_emoji = random.choice(emoji_list)
    
    # 建立三个占位符，防止页面闪烁
    spot_emoji = st.empty()
    spot_text = st.empty()
    spot_audio = st.empty()
    
    # 立即把 Emoji 甩到屏幕上，给用户即时反馈
    spot_emoji.markdown(f'<div class="emoji-display">{random_emoji}</div>', unsafe_allow_html=True)
    
    # --- 第二步：去问 AI 这个东西法语怎么说 ---
    try:
        # 这里的 timeout 很重要，防止手机端无限等待
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"符号 '{random_emoji}'，给出一个对应的法语名词和中文。格式：法语|中文"}],
            timeout=8 
        )
        res = response.choices[0].message.content.strip().split("|")
        
        if len(res) >= 2:
            fr, cn = res[0].strip(), res[1].strip()
            
            # 显示文字
            spot_text.markdown(f'<p class="fr-text">{fr}</p><p class="cn-text">{cn}</p>', unsafe_allow_html=True)
            
            # --- 第三步：生成语音 ---
            # 直接使用 Google TTS 链接，这种方式在手机上加载最快
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={fr}&tl=fr&client=tw-ob"
            spot_audio.audio(tts_url, format='audio/mp3', autoplay=True)
        else:
            spot_text.write("这个单词太难了，换一个试试？")
            
    except Exception as e:
        # 如果 AI 报错或超时，提示用户
        spot_text.markdown(f'<p style="text-align:center; color:red;">[法语君去里尔喝咖啡了，再点一次试试]</p>', unsafe_allow_html=True)

else:
    st.markdown("<p style='text-align:center; color:#999; margin-top:50px;'>点击国旗，开启全宇宙 Emoji 盲盒</p>", unsafe_allow_html=True)
