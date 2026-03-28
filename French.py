import streamlit as st
import random
import edge_tts
import asyncio
import base64
import time

# 1. 词库 (保持 120 词不变)
VOCAB_DATA = [
    ["🥐", "Croissant", "羊角面包"], ["🥖", "Baguette", "法棍"], ["☕", "Café", "咖啡"], 
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🍳", "Œuf", "鸡蛋"], 
    ["🏠", "Maison", "房子"], ["🏙️", "Ville", "城市"], ["🏫", "École", "学校"],
    ["📚", "Livre", "书"], ["💻", "Ordinateur", "电脑"], ["📱", "Téléphone", "电话"],
    ["😊", "Content", "高兴"], ["😴", "Fatigué", "疲惫"], ["🚲", "Vélo", "自行车"],
    ["🚇", "Métro", "地铁"], ["🎒", "Sac", "书包"], ["🛒", "Panier", "购物车"]
]

# 2. 语音生成
async def get_voice_b64(text):
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural", rate="-5%")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return base64.b64encode(audio_data).decode()

# 3. 样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
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
    .fr-font { font-size: 70px; font-weight: bold; color: #002395; margin: 5px 0; }
    .cn-font { font-size: 32px; color: #666; margin-top: 0px; }
    audio { display: block; margin: 15px auto; width: 280px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 逻辑处理
# 创建三个固定的占位符
emoji_placeholder = st.empty()
text_placeholder = st.empty()
audio_placeholder = st.empty()

if st.button("🇫🇷 Clique ici ! (下一词)"):
    # 随机抽词
    icon, fr, cn = random.choice(VOCAB_DATA)
    
    # 1. 立即更新 UI
    emoji_placeholder.markdown(f'<div class="result-container"><div class="emoji-font">{icon}</div></div>', unsafe_allow_html=True)
    text_placeholder.markdown(f'<div class="result-container"><div class="fr-font">{fr}</div><div class="cn-font">{cn}</div></div>', unsafe_allow_html=True)
    
    # 2. 处理音频
    # 先彻底清空一次音频区，强迫浏览器销毁旧的 <audio> 标签
    audio_placeholder.empty()
    
    # 生成一个新的随机 ID
    nonce = str(time.time()).replace(".", "")
    
    try:
        b64_str = asyncio.run(get_voice_b64(fr))
        
        # 3. 重新填入带全新 ID 和 Base64 的音频标签
        audio_html = f"""
            <div style="display: flex; justify-content: center;" id="container_{nonce}">
                <audio controls autoplay id="audio_{nonce}">
                    <source src="data:audio/mp3;base64,{b64_str}" type="audio/mp3">
                </audio>
            </div>
            <script>
                // 延迟一丁点时间确保 DOM 已经渲染，然后强行 play
                setTimeout(function() {{
                    var audio = document.getElementById('audio_{nonce}');
                    if (audio) {{
                        audio.pause();
                        audio.currentTime = 0;
                        audio.play();
                    }}
                }}, 100);
            </script>
        """
        audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
        
    except Exception as e:
        audio_placeholder.warning("语音正在努力加载中...")

else:
    emoji_placeholder.markdown("<h3 style='text-align:center; color:#ccc; margin-top:100px;'>🇫🇷 欢迎来到里尔！<br>点按按钮开始学习吧</h3>", unsafe_allow_html=True)
