import streamlit as st
from datetime import datetime

# 1. Configuración Base
st.set_page_config(page_title="REGLA CERO V6.1 | London Focus", layout="wide")

# 2. Estética Terminal Minimalista
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; text-align: center; }
    .card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; text-align: center; }
    .session-header { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
    /* Centrar la métrica de estado */
    [data-testid="column"] { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: CENTRO DE DATOS (Se mantienen aquí para la lógica) ---
st.sidebar.title("🎮 CONFIGURACIÓN")
sesion_activa = st.sidebar.radio("Elegir Sesión:", ["🇬🇧 LONDRES", "🇺🇸 NUEVA YORK"])

st.sidebar.divider()

if sesion_activa == "🇬🇧 LONDRES":
    # Inputs en el Sidebar (No se muestran en la principal pero alimentan la lógica)
    with st.sidebar.expander("1. NIVELES ASIA", expanded=True):
        a_h = st.number_input("Asia High", format="%.5f", value=1.09200)
        a_l = st.number_input("Asia Low", format="%.5f", value=1.08800)
    
    with st.sidebar.expander("2. ARBITRAJE & OI", expanded=True):
        f_p = st.number_input("Futuros", format="%.5f", value=1.09100)
        s_p = st.number_input("Spot", format="%.5f", value=1.09085)
        v_basis = (f_p - s_p) * 10000
        oi_c = st.number_input("OI CME", value=0)

    with st.sidebar.expander("3. PRECIO & BIAS", expanded=True):
        now_p = st.number_input("Precio Actual", format="%.5f", value=1.09050)
        bias_d = st.selectbox("Bias Diario", ["Alcista", "Bajista", "Rango"])
        lnd_open = st.number_input("London Open", format="%.5f", value=1.09000)

    # Cálculo de lotaje interno
    cap = st.sidebar.number_input("Capital $", value=10000)
    sl_p = st.sidebar.number_input("SL Pips", value=10)
    lotaje_interno = (cap * 0.01) / (sl_p * 10) if sl_p > 0 else 0

    # --- LÓGICA LONDRES ---
    signal = "ESPERA"
    s_color = "#f59e0b"
    
    if bias_d == "Alcista" and now_p < a_l and now_p >= (a_l - 0.0010):
        signal = "LONDON
