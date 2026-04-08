import streamlit as st
from datetime import datetime
import pytz

# 1. TIEMPO NY
ny_zone = pytz.timezone('America/New_York')
ahora = datetime.now(ny_zone)
h_ny = ahora.strftime("%H:%M")
f_ny = ahora.strftime("%Y-%m-%d")

# 2. CONFIGURACIÓN
st.set_page_config(page_title="REGLA CERO V9.4", layout="wide")

# 3. CSS SEGURO
st.markdown("""
<style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; }
    .card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; text-align: center; }
    .session-header { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
    .level-box { padding: 8px; border-radius: 5px; margin: 4px 0; text-align: center; font-size: 0.9em; border: 1px solid #30363d; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("🎮 CENTRO DE MANDO")
sesion = st.sidebar.radio("Elegir Sesión:", ["🇬🇧 LONDRES", "🇺🇸 NUEVA YORK"])
st.sidebar.divider()

if sesion == "🇬🇧 LONDRES":
    with st.sidebar.expander("1. CAJA ASIA", expanded=True):
        ah = st.sidebar.number_input("Asia High", format="%.4f", value=1.0920)
        al = st.sidebar.number_input("Asia Low", format="%.4f", value=1.0880)
        r_size = ah - al

    with st.sidebar.expander("2. VALOR AYER", expanded=True):
        pdh = st.sidebar.number_input("PDH", format="%.4f", value=1.0950)
        pdl = st.sidebar.number_input("PDL", format="%.4f", value=1.0850)
        poc = st.sidebar.number_input("POC", format="%.4f", value=1.0900)
    
    with st.sidebar.expander("3. ARBITRAJE & PRECIO", expanded=True):
        fp = st.sidebar.number_input("Futuros", format="%.4f", value=1.0910)
        sp = st.sidebar.number_input("Spot", format="%.4f", value=1.0908)
        basis = (fp - sp) * 100000 
        now = st.sidebar.number_input("Precio Actual", format="%.4f", value=1.0905)
        bias = st.sidebar.selectbox("Bias Diario", ["Alcista", "Bajista", "Rango"])

    # --- LÓGICA SD ---
    def sd_calc(v): return ah + (r_size * v) if v > 0 else al + (r_size * v)
    
    # --- ESTADO ---
    state = "ESPERA"
    color = "#f59e0b"
    if now < al:
        state = "JUDAS LONG" if now >=
