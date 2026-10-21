import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

# Налаштування сторінки Streamlit на один екран без скролінгу
st.set_page_config(
    page_title="CryptoMinter Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Стилі Binance для мобільного екрана
st.markdown("""
    <style>
    .main {
        background-color: #181a20;
        color: #ffffff;
        padding: 2px !important;
    }
    .stApp {
        background-color: #181a20;
    }
    h1, h2, h3, p, label, span {
        color: #ffffff !important;
    }
    div[data-baseweb="select"] > div, button, .stRadio label {
        font-size: 11px !important;
        min-height: 24px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Жорсткий поділ екрана на дві частини для смартфона
left_col, right_col = st.columns([1.1, 2.5], gap="small")

# --- ЛІВА СТОРОНА: Меню, кнопка Виконати поряд і ШІ-помічник ---
with left_col:
    # Рядок з Меню та кнопкою Виконати поруч
    menu_col, btn_col = st.columns([1.3, 1], gap="small")
    with menu_col:
        st.markdown("<h3 style='font-size: 13px; margin: 0;'>⚙️ Меню</h3>", unsafe_allow_html=True)
    with btn_col:
        exec_button = st.button("🚀 Виконати", use_container_width=True)

    if exec_button:
        st.success("Виконано!")
    
    section = st.selectbox(
        "Режим:",
        ["Ф'ючерси", "Спот", "Опціони", "Боти", "Копітрейдинг"],
        index=0,
        label_visibility="collapsed"
    )

    tf = st.radio(
        "⏱ Таймфрейм:",
        ["1г", "4г", "1д", "1тиж", "2тиж", "1міс"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<hr style='margin: 4px 0px; border-color: #2b313a;'>", unsafe_allow_html=True)
    st.markdown("<span style='font-size: 11px; color: #f0b90b;'>🤖 **ШІ-Помічник (Міша)**</span>", unsafe_allow_html=True)

    # 1. Текстове запитання до ШІ
    user_query = st.text_input("Запитати ШІ:", placeholder="Введіть питання...", label_visibility="collapsed")

    # 2. Рядок з мікрофоном та кнопкою відправки поруч
    col_mic, col_send = st.columns([1.5, 1], gap="small")
    with col_mic:
        voice_input = st.audio_input("Голос")
    with col_send:
        send_button = st.button("➤ Надіслати", use_container_width=True)

    # Відповіді Міші згідно з новими правилами
    if send_button or user_query:
        query_text = user_query.lower() if user_query else "голосовий запит"
        if "біткоїн" in query_text or "btc" in query_text or "ріст" in query_text or "купу" in query_text:
            st.info("🟢 🟢 **Все ок, купуємо.**\n\n*(Ринок бадьоро росте — зелене світло, можна залітати).*")
        elif "дамп" in query_text or "панік" in query_text or "пада" in query_text or "шторм" in query_text:
            st.info("🔴 🔴 **Нічого не робимо!**\n\n*(Потужний дамп або паніка — краще перечекати в безпеці. Дамп (Dump) у криптовалюті — це різке та масштабне падіння ціни активу).*")
        else:
            st.info(f"🟡 🟡 **Туман на горизонті, тримаємось берега.**\n\n*(На ринку невизначеність у режимі [{section}], флет або шторм — краще зайняти вичікувальну позицію).*")
    elif voice_input:
        st.info("🟢 🟢 **Все ок, купуємо.**\n\n*(Голосовий запит розпізнано! Ринок бадьоро росте).*")


# --- ПРАВА СТОРОНА: Великий робочий простір (Ціни + 2 графіки з чітким дном) ---
with right_col:
    st.markdown("<h3 style='font-size: 13px; margin: 0;'>🚀 CryptoMinter Pro</h3>", unsafe_allow_html=True)

    # Ціни в один мікро-рядок
    cp1, cp2, cp3 = st.columns([1.2, 1.2, 1])
    with cp1:
        st.markdown("<span style='color: #0ecb81; font-size: 10px; font-weight: bold;'>BTC: $84,666 (+2.4%)</span>", unsafe_allow_html=True)
    with cp2:
        st.markdown("<span style='color: #0ecb81; font-size: 10px; font-weight: bold;'>ETH: $2,506 (+2.4%)</span>", unsafe_allow_html=True)
    with cp3:
        st.markdown(f"<span style='color: #f0b90b; font-size: 9px;'>Режим: {section}</span>", unsafe_allow_html=True)

    # Генерація даних для графіків з більш помітною волатильністю, щоб падіння було видно
    def generate_time_series(base_price, timeframe):
        now = datetime.now()
        points = 5
        
        if timeframe == "1г":
            delta = timedelta(minutes=15)
        elif timeframe == "4г":
            delta = timedelta(hours=1)
        elif timeframe == "1д":
            delta = timedelta(hours=6)
        elif timeframe == "1тиж":
            delta = timedelta(days=2)
        elif timeframe == "2тиж":
            delta = timedelta(days=3.5)
        else:
            delta = timedelta(days=7)

        times = [(now - delta * i).strftime("%H:%M" if timeframe in ["1г", "4г"] else "%d.%m") for i in range(points - 1, -1, -1)]
        
        # Трохи збільшимо розкид, щоб падіння та мінімуми чітко кидалися в очі на графіку
        volatility_map = {"1г": 0.001, "4г": 0.003, "1д": 0.008, "1тиж": 0.02, "2тиж": 0.035, "1міс": 0.06}
        vol = volatility_map.get(timeframe, 0.015)
        
        data = [base_price * (1 - vol)]
        for _ in range(points - 1):
            change = data[-1] * random.uniform(-vol, vol)
            data.append(data[-1] + change)
        data[-1] = base_price
        return times, data

    times_btc, btc_data = generate_time_series(84666.0, tf)
    times_eth, eth_data = generate_time_series(2506.0, tf)

    min_btc = min(btc_data)
    min_eth = min(eth_data)

    # Мікро-графіки поруч із виразною червоною лінією дна
    gc1, gc2 = st.columns(2, gap="small")

    with gc1:
        st.markdown(f"<span style='font-size: 9px; color: #f0b90b;'>**BTC ({tf}) 📉 Дно: ${min_btc:,.0f}**</span>", unsafe_allow_html=True)
        fig_btc, ax_btc = plt.subplots(figsize=(2.2, 1.2))
        fig_btc.patch.set_facecolor('#1e2329')
        ax_btc.set_facecolor('#1e2329')
        
        ax_btc.plot(times_btc, btc_data, color='#f0b90b', linewidth=1.2, marker='o', markersize=2.5)
        
        # Жирна червона пунктирна лінія рівнів мінімуму
        ax_btc.axhline(y=min_btc, color='#ff4d4d', linestyle='--', linewidth=1.2, alpha=0.9)
        
        ax_btc.fill_between(times_btc, min_btc * 0.995, btc_data, color='#f0b90b', alpha=0.12)
        
        ax_btc.tick_params(colors='#848e9c', labelsize=4)
        plt.setp(ax_btc.get_xticklabels(), rotation=5)
        ax_btc.spines['top'].set_visible(False)
        ax_btc.spines['left'].set_visible(False)
        ax_btc.spines['right'].set_color('#2b313a')
        ax_btc.spines['bottom'].set_color('#2b313a')
        fig_btc.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.22)
        st.pyplot(fig_btc)

    with gc2:
        st.markdown(f"<span style='font-size: 9px; color: #0ecb81;'>**ETH ({tf}) 📉 Дно: ${min_eth:,.0f}**</span>", unsafe_allow_html=True)
        fig_eth, ax_eth = plt.subplots(figsize=(2.2, 1.2))
        fig_eth.patch.set_facecolor('#1e2329')
        ax_eth.set_facecolor('#1e2329')
        
        ax_eth.plot(times_eth, eth_data, color='#0ecb81', linewidth=1.2, marker='o', markersize=2.5)
        
        # Жирна червона пунктирна лінія рівнів мінімуму
        ax_eth.axhline(y=min_eth, color='#ff4d4d', linestyle='--', linewidth=1.2, alpha=0.9)
        
        ax_eth.fill_between(times_eth, min_eth * 0.995, eth_data, color='#0ecb81', alpha=0.12)
        
        ax_eth.tick_params(colors='#848e9c', labelsize=4)
        plt.setp(ax_eth.get_xticklabels(), rotation=5)
        ax_eth.spines['top'].set_visible(False)
        ax_eth.spines['left'].set_visible(False)
        ax_eth.spines['right'].set_color('#2b313a')
        ax_eth.spines['bottom'].set_color('#2b313a')
        fig_eth.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.22)
        st.pyplot(fig_eth)
