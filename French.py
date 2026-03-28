import streamlit as st
import random
import edge_tts
import asyncio
import base64

# 1. 扩充后的百词词库 (按类别组织，方便你以后维护)
VOCAB_DATA = [
    # 美食与购物
    ["🥐", "Croissant", "羊角面包"], ["🥖", "Baguette", "法棍"], ["☕", "Café", "咖啡"], 
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🥚", "Œuf", "鸡蛋"], 
    ["🥛", "Lait", "牛奶"], ["🍰", "Gâteau", "蛋糕"], ["🥗", "Salade", "沙拉"],
    ["🍅", "Tomate", "番茄"], ["🥩", "Viande", "肉"], ["🍟", "Frites", "薯条"],
    ["🍨", "Glace", "冰淇淋"], ["🍫", "Chocolat", "巧克力"], ["🛒", "Panier", "购物车"],
    # 城市生活与交通
    ["🏠", "Maison", "房子"], ["🏙️", "Ville", "城市"], ["🏫", "École", "学校"],
    ["🚉", "Gare", "火车站"], ["🚲", "Vélo", "自行车"], ["🚗", "Voiture", "汽车"],
    ["🚇", "Métro", "地铁"], ["✈️", "Avion", "飞机"], ["🔑", "Clé", "钥匙"],
    ["🗺️", "Carte", "地图"], ["🛍️", "Magasin", "商店"], ["🏥", "Hôpital", "医院"],
    ["🌳", "Parc", "公园"], ["🏛️", "Musée", "博物馆"], ["⛪", "Cathédrale", "大教堂"],
    # 学习与日常
    ["📚", "Livre", "书"], ["💻", "Ordinateur", "电脑"], ["📱", "Téléphone", "电话"],
    ["🖋️", "Stylo", "笔"], ["📋", "Note", "笔记"], ["🕒", "Heure", "时间"],
    ["💼", "Travail", "工作"], ["💡", "Idée", "主意"], ["📅", "Date", "日期"],
    ["🎒", "Sac", "书包"], ["🎓", "Diplôme", "毕业证"], ["💵", "Argent", "钱"],
    # 情绪与社交
    ["❤️", "Cœur", "心"], ["😊", "Content", "高兴"], ["😴", "Fatigué", "疲惫"],
    ["😡", "Colère", "愤怒"], ["🤝", "Ami", "朋友"], ["🎁", "Cadeau", "礼物"],
    ["🎈", "Fête", "派对"], ["💬", "Mot", "单词"], ["☀️", "Soleil", "太阳"],
    # 常见物品
    ["👗", "Robe", "连衣裙"], ["🧥", "Manteau", "外套"], ["👞", "Chaussures", "鞋子"],
    ["☂️", "Parapluie", "雨伞"], ["🕶️", "Lunettes", "眼镜"], ["🚿", "Douche", "洗澡"],
    ["🛏️", "Lit", "床"], ["🍴", "Fourchette", "叉子"], ["🥄", "Cuillère", "勺子"],
    ["🧼", "Savon", "肥皂"], ["🦷", "Dent", "牙齿"], ["🧶", "Laine", "羊毛"]
]

# 2. 核心语音逻辑 (Edge TTS + Base64)
async def get_voice_b64(text):
    # 使用 EloiseNeural，这是公认最好听、最地道的法国女声
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural", rate="-5%")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return base64.b64encode(audio_data).decode()

# 3. 样式配置
st.set_page_config(page_title="Bonjour Lille", page_icon="🇫🇷")
st.markdown("""
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    .stButton>button { 
        width: 100%; height: 80px; font-size: 35px !important; 
        border-radius: 20px; border: 2px solid #002395; 
        background: #f8f9fa; color: #002395; font-weight: bold;
    }
    .result-container { text-align: center; margin-top: 20px; }
    .emoji-font { font-size: 140px; margin-bottom: 0px; }
    .fr-font { font-size: 75px; font-weight: bold; color: #002395; margin: 5px 0; }
    .cn-font { font-size: 35px; color: #666; margin-top: 0px; }
    audio { display: block; margin: 20px auto; width: 280px; }
    </style>
    """, unsafe_allow_html=True)

# 4. 逻辑处理
if 'current' not in st.session_state:
    st.session_state.current = None

if st.button("🇫🇷 Clique ici ! (点我)"):
    st.session_state.current = random.choice(VOCAB_DATA)

if st.session_state.current:
    icon, fr, cn = st.session_state.current
    
    # 渲染文字
    st.markdown(f"""
        <div class="result-container">
            <div class="emoji-font">{icon}</div>
            <div class="fr-font">{fr}</div>
            <div class="cn-font">{cn}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 语音渲染 (Base64 嵌入)
    try:
        b64_str = asyncio.run(get_voice_b64(fr))
        audio_html = f"""
            <div style="display: flex; justify-content: center;">
                <audio controls autoplay>
                    <source src="data:audio/mp3;base64,{b64_str}" type="audio/mp3">
                </audio>
            </div>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning("法语君去喝咖啡了，请重试...")

else:
    st.markdown("<h3 style='text-align:center; color:#ccc; margin-top:100px;'>点按国旗开始法语时间</h3>", unsafe_allow_html=True)
