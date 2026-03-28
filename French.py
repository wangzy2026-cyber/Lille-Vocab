import streamlit as st
import random
import edge_tts
import asyncio
import base64
import time

# 1. 终极分类词库 (120个高频词汇)
VOCAB_DATA = [
    # --- 超市与美食 (Eating & Shopping) ---
    ["🥐", "Croissant", "羊角面包"], ["🥖", "Baguette", "法棍"], ["☕", "Café", "咖啡"], 
    ["🧀", "Fromage", "奶酪"], ["🍷", "Vin", "葡萄酒"], ["🍳", "Œuf", "鸡蛋"], 
    ["🥛", "Lait", "牛奶"], ["🍰", "Gâteau", "蛋糕"], ["🥗", "Salade", "沙拉"],
    ["🍅", "Tomate", "番茄"], ["🥩", "Viande", "肉"], ["🍟", "Frites", "薯条"],
    ["🍨", "Glace", "冰淇淋"], ["🍫", "Chocolat", "巧克力"], ["🛒", "Panier", "购物车"],
    ["🍕", "Pizza", "披萨"], ["🍺", "Bière", "啤酒"], ["🍎", "Pomme", "苹果"],
    ["🍓", "Fraise", "草莓"], ["🍌", "Banane", "香蕉"], ["🍚", "Riz", "米饭"],
    ["🧂", "Sel", "盐"], ["🍯", "Miel", "蜂蜜"], ["🍵", "Thé", "茶"],
    # --- 交通与城市 (City & Transport) ---
    ["🏠", "Maison", "房子"], ["🏙️", "Ville", "城市"], ["🏫", "École", "学校"],
    ["🚉", "Gare", "火车站"], ["🚲", "Vélo", "自行车"], ["🚗", "Voiture", "汽车"],
    ["🚇", "Métro", "地铁"], ["✈️", "Avion", "飞机"], ["🔑", "Clé", "钥匙"],
    ["🗺️", "Carte", "地图"], ["🛍️", "Magasin", "商店"], ["🏥", "Hôpital", "医院"],
    ["🌳", "Parc", "公园"], ["🏛️", "Musée", "博物馆"], ["⛪", "Cathédrale", "大教堂"],
    ["🎭", "Théâtre", "剧院"], ["🏦", "Banque", "银行"], ["📮", "Poste", "邮局"],
    ["🚥", "Feu", "红绿灯"], ["🚕", "Taxi", "出租车"], ["⛵", "Bateau", "船"],
    # --- 校园与学习 (School & Study) ---
    ["📚", "Livre", "书"], ["💻", "Ordinateur", "电脑"], ["📱", "Téléphone", "电话"],
    ["🖋️", "Stylo", "笔"], ["📋", "Note", "笔记"], ["🕒", "Heure", "时间"],
    ["💼", "Travail", "工作"], ["💡", "Idée", "主意"], ["📅", "Date", "日期"],
    ["🎒", "Sac", "书包"], ["🎓", "Diplôme", "毕业证"], ["💵", "Argent", "钱"],
    ["⌨️", "Clavier", "键盘"], ["🖱️", "Souris", "鼠标"], ["🔋", "Batterie", "电池"],
    ["📧", "Email", "邮件"], ["🏢", "Bureau", "办公室"], ["🧑‍🎓", "Étudiant", "学生"],
    # --- 居家与日常 (Home & Daily) ---
    ["👗", "Robe", "连衣裙"], ["🧥", "Manteau", "外套"], ["👞", "Chaussures", "鞋子"],
    ["☂️", "Parapluie", "雨伞"], ["🕶️", "Lunettes", "眼镜"], ["🚿", "Douche", "洗澡"],
    ["🛏️", "Lit", "床"], ["🍴", "Fourchette", "叉子"], ["🥄", "Cuillère", "勺子"],
    ["🧼", "Savon", "肥皂"], ["🦷", "Dent", "牙齿"], ["🧶", "Laine", "羊毛"],
    ["🧺", "Lessive", "洗衣液"], ["🪞", "Miroir", "镜子"], ["🪑", "Chaise", "椅子"],
    ["🛋️", "Canapé", "沙发"], ["🕯️", "Bougie", "蜡烛"], ["🔥", "Feu", "火"],
    # --- 自然与天气 (Nature & Weather) ---
    ["☀️", "Soleil", "太阳"], ["🌙", "Lune", "月亮"], ["☁️", "Nuage", "云"],
    ["🌧️", "Pluie", "雨"], ["❄️", "Neige", "雪"], ["🌬️", "Vent", "风"],
    ["🌈", "Arc-en-ciel", "彩虹"], ["🌸", "Fleur", "花"], ["🌲", "Forêt", "森林"],
    ["🌊", "Mer", "大海"], ["🏔️", "Montagne", "山"], ["⚡", "Orage", "雷暴"],
    # --- 动物与心情 (Animals & Emotions) ---
    ["🐱", "Chat", "猫"], ["🐶", "Chien", "狗"], ["🐦", "Oiseau", "鸟"],
    ["🦁", "Lion", "狮子"], ["🐘", "Éléphant", "大象"], ["🐰", "Lapin", "兔子"],
    ["❤️", "Cœur", "心"], ["😊", "Content", "高兴"], ["😴", "Fatigué", "疲惫"],
    ["😡", "Colère", "愤怒"], ["🤝", "Ami", "朋友"], ["🎁", "Cadeau", "礼物"],
    ["🎈", "Fête", "派对"], ["😭", "Triste", "伤心"], ["🤔", "Doute", "怀疑"],
    ["🔥", "Chaud", "热"], ["❄️", "Froid", "冷"], ["✨", "Étoile", "星星"]
]

# 2. 语音生成逻辑 (Edge TTS + Base64)
async def get_voice_b64(text):
    # 使用 EloiseNeural，发音非常地道
    communicate = edge_tts.Communicate(text, "fr-FR-EloiseNeural", rate="-5%")
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return base64.b64encode(audio_data).decode()

# 3. 样式配置
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
if st.button("🇫🇷 Clique ici ! (下一词)"):
    # 随机抽一个
    icon, fr, cn = random.choice(VOCAB_DATA)
    
    # 渲染内容
    st.markdown(f"""
        <div class="result-container">
            <div class="emoji-font">{icon}</div>
            <div class="fr-font">{fr}</div>
            <div class="cn-font">{cn}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 动态生成随机 ID 破解缓存
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
                var audio = document.getElementById('audio_{nonce}');
                audio.play().catch(function(error) {{
                    console.log("手机端需手动点播放");
                }});
            </script>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning("语音正在努力加载中...")

else:
    st.markdown("<h3 style='text-align:center; color:#ccc; margin-top:100px;'>🇫🇷 欢迎来到里尔！<br>点按按钮开始学习吧</h3>", unsafe_allow_html=True)
