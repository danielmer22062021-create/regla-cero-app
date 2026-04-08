import streamlit as st
from datetime import datetime

# 1. Configuración Base
st.set_page_config(page_title="REGLA CERO V6.1 | London Clean", layout="wide")

# 2. Estética Terminal Minimalista
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; text-align: center; }
    .card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; text-align: center; }
    .session-header { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
    /* Centrar la métrica única */
    [data-testid="column"] { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: CENTRO DE MANDO ---
st.sidebar.title("🎮 CENTRO DE MANDO")
sesion_activa = st.sidebar.radio("Elegir Sesión:", ["🇬🇧 LONDRES", "🇺🇸 NUEVA YORK"])

st.sidebar.divider()

if sesion_activa == "🇬🇧 LONDRES":
    st.sidebar.subheader("Configuración Londres")
    with st.sidebar.expander("1. NIVELES ASIA & AYER", expanded=True):
        a_h = st.sidebar.number_input("Asia High", format="%.5f", value=1.09200)
        a_l = st.sidebar.number_input("Asia Low", format="%.5f", value=1.08800)
        p_poc = st.sidebar.number_input("POC Ayer", format="%.5f", value=1.09000)
    
    with st.sidebar.expander("2. ARBITRAJE (CME)", expanded=
