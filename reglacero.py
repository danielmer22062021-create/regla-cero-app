import streamlit as st
from datetime import datetime
import pytz

# 1. TIEMPO NY
tz_ny = pytz.timezone('America/New_York')
now_ny = datetime.now(tz_ny)
h_ny = now_ny.strftime("%H:%M")
f_ny = now_ny.strftime("%Y-%m-%d")

# 2. CONFIGURACIÓN
st.set_page_config(page_title="REGLA CERO V9.5", layout="wide")

# 3. CSS LIMPIO
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

    # --- CÁLCULO DE NIVELES (SIN FUNCIÓN DEF PARA EVITAR ERRORES) ---
    sd_15_p = ah + (r_size * 1.5)
    sd_25_p = ah + (r_size * 2.5)
    sd_15_n = al - (r_size * 1.5)
    sd_25_n = al - (r_size * 2.5)
    
    # --- LÓGICA DE ESTADO ---
    state = "ESPERA"
    color = "#f59e0b"
    
    if now < al:
        if now >= sd_15_n:
            state = "JUDAS SWEEP (LONG)"
            color = "#00ff41"
        else:
            state = "CONTINUACIÓN BAJA"
            color = "#ef4444"
    elif now > ah:
        if now <= sd_15_p:
            state = "JUDAS SWEEP (SHORT)"
            color = "#ef4444"
        else:
            state = "CONTINUACIÓN ALZA"
            color = "#00ff41"

    # --- INTERFAZ ---
    st.markdown(f'<div class="session-header"><h1>🇬🇧 LONDON TERMINAL | NY: {h_ny}</h1></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.
