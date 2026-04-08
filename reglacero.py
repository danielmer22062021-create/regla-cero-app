import streamlit as st
from datetime import datetime
import pandas as pd

# Configuración de Terminal Pro
st.set_page_config(page_title="REGLA CERO | Trading Terminal", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (ESTÉTICA NEÓN) ---
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    div.stButton > button:first-child { background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); color: black; border: none; font-weight: bold; border-radius: 8px; }
    .status-box { padding: 15px; border-radius: 10px; border-left: 5px solid; margin-bottom: 20px; background-color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: AUDITORÍA DE DATOS ---
st.sidebar.title("📑 AUDITORÍA")

with st.sidebar.expander("1. GASOLINA (CME/COT)", expanded=True):
    cot_bias = st.selectbox("Sesgo Semanal", ["Comprador", "Vendedor", "Neutral"])
    oi_val = st.number_input("Variación OI", value=0, step=500)
    dxy_trend = st.selectbox("DXY Trend", ["Bajista 📉", "Alcista 📈", "Lateral ↔️"])

with st.sidebar.expander("2. UBICACIÓN (TV)", expanded=True):
    zone = st.select_slider("Zona", options=["Discount", "Equilibrium", "Premium"], value="Equilibrium")
    target = st.selectbox("Target ERL", ["PDH", "PDL", "Asia High", "Asia Low", "Equal Highs"])

with st.sidebar.expander("3. GESTIÓN DE RIESGO", expanded=True):
    balance = st.number_input("Balance Cuenta ($)", value=10000, step=1000)
    risk_pct = st.slider("Riesgo por Trade (%)", 0.1, 2.0, 0.5)
    sl_pips = st.number_input("Stop Loss (Pips)", value=10, step=1)

# --- LÓGICA DE ESCENARIOS ---
is_a_plus = False
if cot_bias == "Comprador" and oi_val >= 5000 and dxy_trend == "Bajista 📉" and zone == "Discount":
    is_a_plus = True
    signal = "COMPRA A+"
    color = "#00ff41"
elif cot_bias == "Vendedor" and oi_val >= 5000 and dxy_trend == "Alcista 📈" and zone == "Premium":
    is_a_plus = True
    signal = "VENTA A+"
    color = "#ff4b4b"
else:
    signal = "ESPERAR / NO TRADE"
    color = "#f59e0b"

# --- LAYOUT PRINCIPAL ---
st.title("🛡️ TERMINAL REGLA CERO")
st.caption(f"Sesión: {datetime.now().strftime('%A, %d %B %Y')} | NY Time")

# Métricas Principales
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("GATILLO", signal)
with col2:
    # Cálculo de lotaje: (Balance * %Riesgo) / (SL * 10) para EURUSD
    lotaje = (balance * (risk_pct/100)) / (sl_pips * 10)
    st.metric("LOTAJE SUGERIDO", f"{lotaje:.2f}")
with col3:
    st.metric("ENERGÍA (OI)", f"{oi_val} CTR")
with col4:
    st.metric("RIESGO $", f"${balance * (risk_pct/100):.2g}")

st.divider()

# --- PANEL CENTRAL: NARRATIVA Y FICHA ---
c_left, c_right = st.columns([2, 1])

with c_left:
    st.subheader("📖 Plan de Ejecución")
    if is_a_plus:
        st.markdown(f"""
        <div class="status-box" style="border-color: {color};">
            <h3 style="color: {color}; margin-top:0;">🔥 ESCENARIO DE ALTA PROBABILIDAD</h3>
            <p>Confluencia detectada entre <b>CME ({cot_bias})</b> y <b>Zona de Precio ({zone})</b>. 
            El DXY apoya el movimiento. Busca confirmación en ATAS (CVD/DOM) para entrar.</p>
            <b>Objetivo Principal:</b> {target}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Sin confluencia clara. El algoritmo recomienda paciencia. No fuerces entradas en zonas de Equilibrium.")

    # Checklist Dinámico
    st.write("### ✅ Checklist de Confirmación")
    st.checkbox("¿Hubo toma de liquidez previa (Liquidity Sweep)?")
    st.checkbox("¿El Smart DOM muestra muros >300 defendiendo mi zona?")
    st.checkbox("¿CVD en ATAS muestra absorción/agresión a mi favor?")

with c_right:
    st.subheader("📸 Snapshot")
    # Ficha técnica compacta para captura
    st.markdown(f"""
    <div style="background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d;">
        <p style="margin:0; font-size:0.8em; color:#8b949e;">AUDITORÍA DIARIA</p>
        <hr style="margin:10px 0; border-color:#30363d;">
        <p><b>Bias:</b> {cot_bias}</p>
        <p><b>DXY:</b> {dxy_state if 'dxy_state' in locals() else dxy_trend}</p>
        <p><b>Zona:</b> {zone}</p>
        <p><b>Lots:</b> {lotaje:.2f}</p>
        <p style="color:{color}; font-weight:bold; font-size:1.2em; text-align:center; margin-top:10px;">{signal}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("Foco Técnico | Rigor Matemático | Regla Cero")
