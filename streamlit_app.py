import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

# Налаштування сторінки Streamlit для повного розміщення на одному екрані
st.set_page_config(
    page_title="CryptoMinter Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Темний стиль біржі Binance через CSS
st.markdown("""
    <style>
    .main {
        background-color: #181a20;
        color: #ffffff;
    }
    .stApp {
        background-color: #181a20;
    }
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Головний заголовок
st.markdown("## 🚀 CryptoMinter Pro — Професійний Термінал")
st.markdown("---")

# Розподіл екрана на дві частини (ЛІВА — управління та ШІ, ПРАВА — графіки та ціни)
left_control, right_display = st.columns([1.2, 2.8])

with left_control:
    st.markdown("### ⚙️ Панель управління")
    
    # 1. Режими торгівлі
    section = st.selectbox(
        "Режим торгівлі:",
        ["Ф'ючерси", "Спот", "Опціони", "Торгові боти", "Копітрейдинг"],
        index=0
    )

    # 2. Часова рамка
    tf = st.radio(
        "⏱ Масштаб графіків:",
        ["1г", "4г", "1д", "1тиж", "2тиж", "1міс"],
        horizontal=True
    )

    st.markdown("---")
    
    # 3. НОВА КНОПКА: ШІ-помічник з базою знань
    st.markdown("### 🤖 ШІ-Помічник (Торгова База)")
    if st.button("Запустити ШІ-Аналіз ринку", use_container_width=True):
        ai_tips = {
            "Ф'ючерси": "💡 **База ШІ (Ф'ючерси):** Тренд бичачий. Рекомендовано використовувати крос-маржу 10x та ставити стоп-лосс нижче локального мінімуму.",
            "Спот": "💡 **База ШІ (Спот):** Сприятливий момент для накопичення активов. Купуйте частинами (дзвіночок DCA).",
            "Опціони": "💡 **База ШІ (Опціони):** Висока волатильність. Стратегія Кол (Call) на пробій рівня дає перевагу.",
            "Торгові боти": "💡 **База ШІ (Боти):** Увімкніть спотову сітку з діапазоном ±15% від поточної ціни.",
            "Копітрейдинг": "💡 **База ШІ (Копітрейдинг):** Обирайте топ-трейдерів із просадкою менше 20% за останній місяць."
        }
        st.info(ai_tips.get(section, "💡 **База ШІ:** Аналізую ринкові дані у реальному часі..."))

    # 4. Кнопка виконання
    if st.button(f"Виконати ({section})", use_container_width=True):
        st.success(f"Успішно опрацьовано для: {section}!")


with right_display:
    st.markdown("### 📈 Ринковий моніторинг (BTC & ETH)")

    # Поточні ціни у великому полі справа
    cp1, cp2 = st.columns(2)
    with cp1:
        st.markdown("**BTC/USDT:** <span style='color: #0ecb81; font-size: 18px; font-weight: bold;'>$84,666.00 (+2.44%)</span>", unsafe_allow_html=True)
    with cp2:
        st.markdown("**ETH/USDT:** <span style='color: #0ecb81; font-size: 18px; font-weight: bold;'>$2,506.08 (+2.48%)</span>", unsafe_allow_html=True)

    st.markdown("")

    # Генерація даних та точного часу для осі X
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
        else:  # "1міс"
            delta = timedelta(days=6)

        times = [(now - delta * i).strftime("%H:%M" if timeframe in ["1г", "4г"] else "%d.%m") for i in range(points - 1, -1, -1)]
        
        volatility_map = {"1г": 0.0003, "4г": 0.001, "1д": 0.005, "1тиж": 0.015, "2тиж": 0.025, "1міс": 0.05}
        vol = volatility_map.get(timeframe, 0.01)
        
        data = [base_price * (1 - vol)]
        for _ in range(points - 1):
            change = data[-1] * random.uniform(-vol, vol)
            data.append(data[-1] + change)
        data[-1] = base_price  # Фіксація поточної ціни «зараз» у кінці
        
        return times, data

    times_btc, btc_data = generate_time_series(84666.0, tf)
    times_eth, eth_data = generate_time_series(2506.0, tf)

    # Паралельні графіки всередині правої панелі (компактні, на одному екрані)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown(f"**Bitcoin (BTC) — [{tf}]**")
        fig_btc, ax_btc = plt.subplots(figsize=(3.8, 2.2))
        fig_btc.patch.set_facecolor('#1e2329')
        ax_btc.set_facecolor('#1e2329')
        
        ax_btc.plot(times_btc, btc_data, color='#f0b90b', linewidth=1.5, marker='o', markersize=4)
        ax_btc.fill_between(times_btc, min(btc_data)*0.99, btc_data, color='#f0b90b', alpha=0.12)
        
        ax_btc.tick_params(colors='#848e9c', labelsize=7)
        plt.setp(ax_btc.get_xticklabels(), rotation=15)
        ax_btc.spines['top'].set_visible(False)
        ax_btc.spines['left'].set_visible(False)
        ax_btc.spines['right'].set_color('#2b313a')
        ax_btc.spines['bottom'].set_color('#2b313a')
        st.pyplot(fig_btc)

    with col_chart2:
        st.markdown(f"**Ethereum (ETH) — [{tf}]**")
        fig_eth, ax_eth = plt.subplots(figsize=(3.8, 2.2))
        fig_eth.patch.set_facecolor('#1e2329')
        ax_eth.set_facecolor('#1e2329')
        
        ax_eth.plot(times_eth, eth_data, color='#0ecb81', linewidth=1.5, marker='o', markersize=4)
        ax_eth.fill_between(times_eth, min(eth_data)*0.99, eth_data, color='#0ecb81', alpha=0.12)
        
        ax_eth.tick_params(colors='#848e9c', labelsize=7)
        plt.setp(ax_eth.get_xticklabels(), rotation=15)
        ax_eth.spines['top'].set_visible(False)
        ax_eth.spines['left'].set_visible(False)
        ax_eth.spines['right'].set_color('#2b313a')
        ax_eth.spines['bottom'].set_color('#2b313a')
        st.pyplot(fig_eth)
