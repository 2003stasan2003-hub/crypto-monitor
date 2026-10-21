import streamlit as st
import matplotlib.pyplot as plt
import random

# Налаштування сторінки Streamlit для мобільного екрана
st.set_page_config(
    page_title="CryptoMinter Pro",
    page_icon="📈",
    layout="centered",
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

# 1. ВЕРХНІ ВКЛАДКИ (РОБОЧІ)
section = st.selectbox(
    "Виберіть режим торгівлі:",
    ["Ф'ючерси", "Спот", "Опціони", "Торгові боти", "Копітрейдинг"],
    index=0
)

# 2. ПАНЕЛЬ ЦІН (BTC та ETH)
col_price1, col_price2 = st.columns(2)
with col_price1:
    st.markdown("### **BTC/USDT**")
    st.markdown("<span style='color: #0ecb81; font-size: 20px; font-weight: bold;'>$84,666.00 (+2.44%)</span>", unsafe_allow_html=True)

with col_price2:
    st.markdown("### **ETH/USDT**")
    st.markdown("<span style='color: #0ecb81; font-size: 20px; font-weight: bold;'>$2,506.08 (+2.48%)</span>", unsafe_allow_html=True)

st.markdown("---")

# 3. ПАНЕЛЬ ТАЙМФРЕЙМІВ (ВІД 1 ГОДИНИ ДО 1 МІСЯЦЯ)
st.markdown("### Часова рамка:")
tf = st.radio(
    "Оберіть масштаб:",
    ["1г", "4г", "1д", "1тиж", "2тиж", "1міс"],
    horizontal=True,
    label_visibility="collapsed"
)

# 4. ГЕНЕРАЦІЯ ДАНИХ ДЛЯ ГРАФІКІВ
def generate_data(base_price, timeframe):
    volatility_map = {
        "1г": 0.0003,
        "4г": 0.001,
        "1д": 0.005,
        "1тиж": 0.015,
        "2тиж": 0.025,
        "1міс": 0.05
    }
    vol = volatility_map.get(timeframe, 0.01)
    points = 30
    data = [base_price * (1 - vol)]
    for _ in range(points - 1):
        change = data[-1] * random.uniform(-vol, vol)
        data.append(data[-1] + change)
    data[-1] = base_price
    return data

btc_data = generate_data(84666.0, tf)
eth_data = generate_data(2506.0, tf)

# 5. ДВА ГРАФІКИ ПОРУЧ (BTC та ETH)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown(f"**Bitcoin (BTC) — [{tf}]**")
    fig_btc, ax_btc = plt.subplots(figsize=(4, 2.5))
    fig_btc.patch.set_facecolor('#1e2329')
    ax_btc.set_facecolor('#1e2329')
    ax_btc.plot(btc_data, color='#f0b90b', linewidth=1.5)
    ax_btc.fill_between(range(len(btc_data)), min(btc_data)*0.99, btc_data, color='#f0b90b', alpha=0.12)
    ax_btc.tick_params(colors='#848e9c', labelsize=7)
    ax_btc.spines['top'].set_visible(False)
    ax_btc.spines['left'].set_visible(False)
    ax_btc.spines['right'].set_color('#2b313a')
    ax_btc.spines['bottom'].set_color('#2b313a')
    st.pyplot(fig_btc)

with col_chart2:
    st.markdown(f"**Ethereum (ETH) — [{tf}]**")
    fig_eth, ax_eth = plt.subplots(figsize=(4, 2.5))
    fig_eth.patch.set_facecolor('#1e2329')
    ax_eth.set_facecolor('#1e2329')
    ax_eth.plot(eth_data, color='#0ecb81', linewidth=1.5)
    ax_eth.fill_between(range(len(eth_data)), min(eth_data)*0.99, eth_data, color='#0ecb81', alpha=0.12)
    ax_eth.tick_params(colors='#848e9c', labelsize=7)
    ax_eth.spines['top'].set_visible(False)
    ax_eth.spines['left'].set_visible(False)
    ax_eth.spines['right'].set_color('#2b313a')
    ax_eth.spines['bottom'].set_color('#2b313a')
    st.pyplot(fig_eth)

# 6. КНОПКИ ДІЙ ТА СТАТУС
st.markdown("---")
if st.button(f"Виконати операцію у розділі: {section}", use_container_width=True):
    st.success(f"Успішно опрацьовано запит для режиму: {section}!")
