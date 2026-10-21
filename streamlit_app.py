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

# Стилі Binance та фіксація без скролінгу
st.markdown("""
    <style>
    .main {
        background-color: #181a20;
        color: #ffffff;
        overflow: hidden;
    }
    .stApp {
        background-color: #181a20;
    }
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Розподіл головного екрана на дві частини: ліва (вузьке меню) і права (велике поле)
left_menu, right_main = st.columns([1, 2.6])

# --- ЛІВА СТОРОНА: Вузька панель управління на одній сторінці ---
with left_menu:
    st.markdown("### ⚙️ Меню")
    
    section = st.selectbox(
        "Режим:",
        ["Ф'ючерси", "Спот", "Опціони", "Боти", "Копітрейдинг"],
        index=0
    )

    tf = st.radio(
        "⏱ Таймфрейм:",
        ["1г", "4г", "1д", "1тиж", "2тиж", "1міс"],
        horizontal=True
    )

    if st.button("🤖 ШІ-Аналіз", use_container_width=True):
        ai_tips = {
            "Ф'ючерси": "💡 Тренд бичачий. 10x крос.",
            "Спот": "💡 DCA накопичення.",
            "Опціони": "💡 Кол (Call) стратегія.",
            "Боти": "💡 Сітка ±15%.",
            "Копітрейдинг": "💡 Топ трейдери."
        }
        st.info(ai_tips.get(section, "💡 Аналіз ринку..."))

    if st.button("🚀 Виконати", use_container_width=True):
        st.success("Успішно!")


# --- ПРАВА СТОРОНА: Широке поле (Ціни + Графіки на одному екрані) ---
with right_main:
    st.markdown("### 🚀 CryptoMinter Pro")

    # Поточні ціни в один рядок
    cp1, cp2, cp3 = st.columns([1.2, 1.2, 1])
    with cp1:
        st.markdown("**BTC:** <span style='color: #0ecb81; font-size: 13px; font-weight: bold;'>$84,666 (+2.4%)</span>", unsafe_allow_html=True)
    with cp2:
        st.markdown("**ETH:** <span style='color: #0ecb81; font-size: 13px; font-weight: bold;'>$2,506 (+2.4%)</span>", unsafe_allow_html=True)
    with cp3:
        st.markdown(f"<span style='color: #f0b90b; font-size: 11px;'>Режим: {section}</span>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 2px 0px 8px 0px; border-color: #2b313a;'>", unsafe_allow_html=True)

    # Генерація даних для графіків
    def generate_time_series(base_price, timeframe):
        now = datetime.now()
        points = 5
        
        if timeframe == "1г":
            delta = timedelta(minutes=12)
        elif timeframe == "4г":
            delta = timedelta(minutes=48)
        elif timeframe == "1д":
            delta = timedelta(hours=4)
        elif timeframe == "1тиж":
            delta = timedelta(days=1.5)
        elif timeframe == "2тиж":
            delta = timedelta(days=3)
        else:
            delta = timedelta(days=6)

        times = [(now - delta * i).strftime("%H:%M" if timeframe in ["1г", "4г"] else "%d.%m") for i in range(points - 1, -1, -1)]
        volatility_map = {"1г": 0.0003, "4г": 0.001, "1д": 0.005, "1тиж": 0.015, "2тиж": 0.025, "1міс": 0.05}
        vol = volatility_map.get(timeframe, 0.01)
        
        data = [base_price * (1 - vol)]
        for _ in range(points - 1):
            change = data[-1] * random.uniform(-vol, vol)
            data.append(data[-1] + change)
        data[-1] = base_price
        return times, data

    times_btc, btc_data = generate_time_series(84666.0, tf)
    times_eth, eth_data = generate_time_series(2506.0, tf)

    # Два компактні графіки поруч у правій частині
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown(f"<span style='font-size: 11px; color: #f0b90b;'>**BTC — {tf}**</span>", unsafe_allow_html=True)
        fig_btc, ax_btc = plt.subplots(figsize=(3.0, 1.6))
        fig_btc.patch.set_facecolor('#1e2329')
        ax_btc.set_facecolor('#1e2329')
        
        ax_btc.plot(times_btc, btc_data, color='#f0b90b', linewidth=1.2, marker='o', markersize=2.5)
        ax_btc.fill_between(times_btc, min(btc_data)*0.99, btc_data, color='#f0b90b', alpha=0.12)
        
        ax_btc.tick_params(colors='#848e9c', labelsize=5)
        plt.setp(ax_btc.get_xticklabels(), rotation=10)
        ax_btc.spines['top'].set_visible(False)
        ax_btc.spines['left'].set_visible(False)
        ax_btc.spines['right'].set_color('#2b313a')
        ax_btc.spines['bottom'].set_color('#2b313a')
        fig_btc.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.2)
        st.pyplot(fig_btc)

    with col_chart2:
        st.markdown(f"<span style='font-size: 11px; color: #0ecb81;'>**ETH — {tf}**</span>", unsafe_allow_html=True)
        fig_eth, ax_eth = plt.subplots(figsize=(3.0, 1.6))
        fig_eth.patch.set_facecolor('#1e2329')
        ax_eth.set_facecolor('#1e2329')
        
        ax_eth.plot(times_eth, eth_data, color='#0ecb81', linewidth=1.2, marker='o', markersize=2.5)
        ax_eth.fill_between(times_eth, min(eth_data)*0.99, eth_data, color='#0ecb81', alpha=0.12)
        
        ax_eth.tick_params(colors='#848e9c', labelsize=5)
        plt.setp(ax_eth.get_xticklabels(), rotation=10)
        ax_eth.spines['top'].set_visible(False)
        ax_eth.spines['left'].set_visible(False)
        ax_eth.spines['right'].set_color('#2b313a')
        ax_eth.spines['bottom'].set_color('#2b313a')
        fig_eth.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.2)
        st.pyplot(fig_eth)
