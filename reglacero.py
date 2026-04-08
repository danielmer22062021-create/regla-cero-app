import streamlit as st
from datetime import datetime

# Configuración de Terminal V5.0
st.set_page_config(page_title="REGLA CERO V5.0 | Pro Terminal", layout="wide")

# --- ESTÉTICA NEÓN PROFESIONAL ---
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; }
    .snapshot-card { background-color: #111827; padding: 20px; border: 2px solid #374151; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUTS TÉCNICOS ---
st.sidebar.title("🛠️ PANEL DE DATOS")

# 1. ARBITRAJE FUTUROS/SPOT
with st.sidebar.expander("1. ARBITRAJE & BASIS", expanded=True):
    f_price = st.number_input("Precio Futuros (CME)", format="%.5f", value=1.09100)
    s_price = st.number_input("Precio Spot (Broker)", format="%.5f", value=1.09085)
    basis = (f_price - s_price) * 10000  # Cálculo en Pips/Puntos
    st.caption(f"Basis Actual: {basis:.2f} pips")

# 2. NIVELES DE AYER (H1/D1)
with st.sidebar.expander("2. PREVIOUS DAY LEVELS", expanded=True):
    p_high = st.number_input("PDH (Máximo)", format="%.5f", value=1.09500)
    p_low = st.number_input("PDL (Mínimo)", format="%.5f", value=1.08500)
    p_poc = st.number_input("POC (Punto Control)", format="%.5f", value=1.09000)

# 3. ASIA RANGE
with st.sidebar.expander("3. ASIA SESSION", expanded=True):
    a_high = st.number_input("Asia High", format="%.5f", value=1.09200)
    a_low = st.number_input("Asia Low", format="%.5f", value=1.08800)

# 4. CONTEXTO ACTUAL
with st.sidebar.expander("4. CONTEXTO & PRECIO", expanded=True):
    c_price = st.number_input("Precio Actual", format="%.5f", value=1.09050)
    d_bias = st.selectbox("Marco Diario", ["Expansión Alcista", "Expansión Bajista", "Consolidación", "Reversa HTF"])
    oi_val = st.number_input("Variación OI", value=0)

# 5. RIESGO
with st.sidebar.expander("5. GESTIÓN", expanded=False):
    balance = st.number_input("Balance ($)", value=10000)
    sl_pips = st.number_input("SL (Pips)", value=10)

# --- LÓGICA DE ESCENARIOS V5.0 ---
# Definición de zonas
posicion_asia = "Dentro del Rango"
if c_price > a_high: posicion_asia = "Liquidando Asia High (S)"
elif c_price < a_low: posicion_asia = "Liquidando Asia Low (B)"

# Determinación del Gatillo
gatillo = "MONITORIZANDO"
color = "#f59e0b"

if d_bias == "Expansión Alcista" and c_price < a_low and c_price >= p_poc:
    gatillo = "COMPRA (JUDAS SWEEP)"
    color = "#00ff41"
elif d_bias == "Expansión Bajista" and c_price > a_high and c_price <= p_poc:
    gatillo = "VENTA (JUDAS SWEEP)"
    color = "#ff4b4b"

# --- DASHBOARD PRINCIPAL ---
st.title("🏹 TERMINAL REGLA CERO V5.0")
st.subheader(f"Contexto: {d_bias} | {posicion_asia}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("GATILLO", gatillo)
m2.metric("ARBITRAJE (BASIS)", f"{basis:.2f}")
m3.metric("LOTAJE", f"
