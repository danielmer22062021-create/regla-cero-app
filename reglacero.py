import streamlit as st
from datetime import datetime

# Configuración Pro
st.set_page_config(page_title="REGLA CERO V5.1 | Stable Terminal", layout="wide")

# --- ESTÉTICA DARK MODE ---
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; }
    .snapshot-card { background-color: #111827; padding: 20px; border: 2px solid #374151; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: ENTRADA DE DATOS ---
st.sidebar.title("🛡️ AUDITORÍA TÉCNICA")

# 1. ARBITRAJE
with st.sidebar.expander("1. BASIS (FUTUROS/SPOT)", expanded=True):
    f_price = st.number_input("Precio Futuros (CME)", format="%.5f", value=1.09100)
    s_price = st.number_input("Precio Spot (Broker)", format="%.5f", value=1.09085)
    # Cálculo matemático del Arbitraje
    basis = (f_price - s_price) * 10000 

# 2. NIVELES HTF
with st.sidebar.expander("2. NIVELES DÍA ANTERIOR", expanded=True):
    p_high = st.number_input("Máximo (PDH)", format="%.5f", value=1.09500)
    p_low = st.number_input("Mínimo (PDL)", format="%.5f", value=1.08500)
    p_poc = st.number_input("Punto de Control (POC)", format="%.5f", value=1.09000)

# 3. ASIA RANGE
with st.sidebar.expander("3. RANGO DE ASIA", expanded=True):
    a_high = st.number_input("Asia High", format="%.5f", value=1.09200)
    a_low = st.number_input("Asia Low", format="%.5f", value=1.08800)

# 4. CONTEXTO ACTUAL
with st.sidebar.expander("4. PRECIO & SESGO", expanded=True):
    c_price = st.number_input("Precio Actual", format="%.5f", value=1.09050)
    d_bias = st.selectbox("Marco Diario", ["Expansión Alcista", "Expansión Bajista", "Consolidación", "Reversa"])
    dxy_trend = st.selectbox("DXY", ["Bajista 📉", "Alcista 📈", "Rango"])
    oi_val = st.number_input("Variación OI", value=0)

# 5. RIESGO
with st.sidebar.expander("5. GESTIÓN", expanded=False):
    balance = st.number_input("Balance ($)", value=10000)
    sl_pips = st.number_input("SL (Pips)", value=10)

# --- LÓGICA DE ESCENARIOS ---
gatillo = "MONITORIZANDO"
color = "#f59e0b" # Naranja (Espera)

# Lógica Judas Swing Alcista
if d_bias == "Expansión Alcista" and c_price < a_low and c_price >= p_low:
    gatillo = "COMPRA (JUDAS SWEEP)"
    color = "#00ff41" # Verde
# Lógica Judas Swing Bajista
elif d_bias == "Expansión Bajista" and c_price > a_high and c_price <= p_high:
    gatillo = "VENTA (JUDAS SWEEP)"
    color = "#ff4b4b" # Rojo

# --- INTERFAZ PRINCIPAL ---
st.title("🛡️ TERMINAL REGLA CERO V5.1")

# Métricas rápidas
m1, m2, m3, m4 = st.columns(4)
m1.metric("GATILLO", gatillo)
m2.metric("BASIS (PIPS)", f"{basis:.2f}")
m3.metric("LOTS", f"{(balance * 0.01) / (sl_pips * 10):.2f}")
m4.metric("OI INFO", f"{oi_val} CTR")

st.divider()

# Layout de Análisis
col_info, col_snap = st.columns([1.5, 1])

with col_info:
    st.subheader("📍 Análisis de Niveles")
    # Distancia al POC
    dist_poc = (c_price - p_poc) * 10000
    st.write(f"**Precio vs POC:** {'Sobre' if dist_poc > 0 else 'Bajo'} el valor medio ({abs(dist_poc):.1f} pips)")
    
    st.subheader("⛓️ Arbitraje (Order Flow)")
    if abs(basis) > 2.5:
        st.error(f"⚠️ BASIS ELEVADO: {basis:.2f}. Hay una gran
