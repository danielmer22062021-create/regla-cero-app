import streamlit as st
from datetime import datetime
import pytz

# 1. ZONA HORARIA NY
tz_ny = pytz.timezone('America/New_York')
now_ny = datetime.now(tz_ny)
h_ny = now_ny.strftime("%H:%M")
f_ny = now_ny.strftime("%Y-%m-%d")

# 2. CONFIGURACIÓN
st.set_page_config(page_title="REGLA CERO | One-Page Terminal", layout="wide")

# 3. ESTILO MINIMALISTA NEÓN
st.markdown("""
<style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; }
    .card { background-color: #111827; padding: 25px; border: 1px solid #374151; border-radius: 20px; text-align: center; margin-top: 20px; }
    .status-msg { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; margin: 10px 0; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #3b82f6, #2563eb); color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.title("🏹 TERMINAL REGLA CERO")
st.subheader(f"NY Time: {h_ny} | {f_ny}")
st.write("Introduce los datos de la sesión y presiona el botón para auditar.")

# --- AMBIENTE ÚNICO DE ENTRADA (FORMULARIO) ---
with st.form("audit_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("###
