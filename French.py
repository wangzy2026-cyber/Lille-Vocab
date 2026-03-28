import streamlit as st
import random

# 1. 扩充后的里尔生存词库 (涵盖生活方方面面)
# [图标, 法语, 中文]
VOCAB_LIST = [
    ["🍎", "Pomme", "苹果"], ["🥐", "Croissant", "羊角面包"], ["☕", "Café", "咖啡"],
    ["🥖", "Baguette", "法棍"], ["🧀", "Fromage", "奶酪"], ["🐶", "Chien", "狗"],
    ["🐱", "Chat", "猫"], ["🚗", "Voiture", "汽车"], ["🚲", "Vélo", "自行车"],
    ["🏠", "Maison", "房子"], ["🌳", "Arbre", "树"], ["☀️", "Soleil", "太阳"],
    ["🌧️", "Pluie", "雨"], ["🍷", "Vin", "葡萄酒"], ["🥛", "Lait", "牛奶"],
    ["🥚", "Œuf", "鸡蛋"], ["🍅", "Tomate", "番茄"], ["✈️", "Avion", "飞机"],
    ["🏙️", "Ville", "城市"], ["🏫", "École", "学校"], ["📚", "Livre", "书"],
    ["💻", "Ordinateur", "电脑"], ["📱", "Téléphone", "电话"], ["🎁", "Cadeau", "礼物"],
    ["🍰", "Gâteau", "蛋糕"], ["🍦", "Glace", "冰淇淋"], ["🍓", "Fraise", "草莓"],
    ["🦁", "Lion", "狮子"], ["🐘", "Éléphant", "大象"], ["🐰", "Lapin", "兔子"],
    ["🌸", "Fleur", "花"], ["🌊", "Mer", "大海"], ["🎨", "Art", "艺术"],
    ["🎵", "Musique", "音乐"], ["⚽", "Football", "足球"], ["🍔", "Hamburger", "汉堡"],
    ["🍕", "Pizza", "披萨"], ["🍇", "Raisin", "葡萄"], ["🐻", "Ours", "熊"],
    ["🍁", "Feuille", "叶子"], ["🏔️", "Montagne", "山"], ["🌙", "Lune", "月亮"],
    ["👗", "Robe", "连衣裙"], ["👞", "Chaussures", "鞋子"], ["🧥", "Manteau", "外套"],
    ["🧴", "Savon", "肥皂"], ["🔑", "Clé", "钥匙"], ["🛏️", "Lit", "床"],
    ["🍴", "Fourchette", "叉子"], ["🥄", "Cuillère", "勺子"], ["🥗", "Salade", "沙拉"]
]

# 2. 极致简样式
st.set_page_config(page_title="Lille Survival", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 120px; font-size: 100px; 
        background: #fdfdfd; border: 1px solid #eee; border-radius: 20px;
    }
    .emoji-display { font-size: 150px; text-align: center; margin: 20px 0; }
    .fr-text { text-align: center; color: #002395; font-size: 75px; font-weight: bold; margin-bottom: 0px;}
    .cn-text { text-align: center; color: #666; font-size: 35px; margin-top: 10px; margin-bottom: 30px;}
    
    /* 强制音频居中并加大 */
    div[data-testid="stAudio"] {
        max-width: 300px;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 核心交互
if st.button("🇫🇷"):
    # 随机抽取一个
    item = random.choice(VOCAB_LIST)
    icon, fr, cn = item[0], item[1], item[2]
    
    # 渲染内容
    st.markdown(f'<div class="emoji-display">{icon}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="fr-text">{fr}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="cn-text">{cn}</p>', unsafe_allow_html=True)
    
    # 🔊 语音：使用最稳的谷歌接口（国内可用，国外秒开）
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={fr}&tl=fr&client=tw-ob"
    st.audio(tts_url, format='audio/mp3', autoplay=True)

else:
    st.markdown("<p style='text-align:center; color:#999; margin-top:50px;'>点击国旗，开启法语盲盒</p>", unsafe_allow_html=True)
