import streamlit as st
from datetime import datetime
import pytz
import time

# 1. TIEMPO NY (Reloj en vivo)
tz_ny = pytz.timezone('America/New_York')
now_ny = datetime.now(tz_ny)
h_ny = now_ny.strftime("%H:%M:%S")
f_ny = now_ny.strftime("%Y-%m-%d")

# 2. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="REGLA CERO V11 | Manual Arbitrage", layout="wide")

# 3. ESTILOS TERMINAL
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

# MODO LIVE
st.sidebar.divider()
st.sidebar.subheader("📡 MODO LIVE")
auto_refresh = st.sidebar.toggle("Activar Auto-Refresco", value=False)
refresh_rate = st.sidebar.slider("Segundos", 5, 60, 10)
st.sidebar.divider()

if sesion == "🇬🇧 LONDRES":
    with st.sidebar.expander("1. CAJA ASIA (4D)", expanded=True):
        ah = st.sidebar.number_input("Asia High", format="%.4f", value=1.0920)
        al = st.sidebar.number_input("Asia Low", format="%.4f", value=1.0880)
        r_size = ah - al

    with st.sidebar.expander("2. VALOR AYER (4D)", expanded=True):
        pdh = st.sidebar.number_input("PDH", format="%.4f", value=1.0950)
        pdl = st.sidebar.number_input("PDL", format="%.4f", value=1.0850)
        poc = st.sidebar.number_input("POC", format="%.4f", value=1.0900)
    
    with st.sidebar.expander("3. ARBITRAJE & PRECIO", expanded=True):
        # ENTRADA MANUAL DE ARBITRAJE
        basis = st.sidebar.number_input("Arbitraje (Diferencia Puntos)", value=10.0, step=1.0)
        now = st.sidebar.number_input("Precio Actual", format="%.4f", value=1.0905)
        bias = st.sidebar.selectbox("Bias Diario", ["Alcista", "Bajista", "Rango"])

    # --- CÁLCULOS TÉCNICOS ---
    sd_15_p = ah + (r_size * 1.5)
    sd_15_n = al - (r_size * 1.5)
    
    # Lógica de Estado
    state, color = "ESPERA", "#f59e0b"
    if now < al:
        state = "JUDAS LONG" if now >= sd_15_n else "CONTINUACIÓN BAJA"
        color = "#00ff41" if "LONG" in state else "#ef4444"
    elif now > ah:
        state = "JUDAS SHORT" if now <= sd_15_p else "CONTINUACIÓN ALZA"
        color = "#ef4444" if "SHORT" in state else "#00ff41"

    # --- INTERFAZ PRINCIPAL ---
    st.markdown(f'<div class="session-header"><h1>🇬🇧 LONDON TERMINAL | NY: {h_ny}</h1></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("ESTADO", state)
    c2.metric("ARBITRAJE MANUAL", f"{basis:.1f} PTS")
    c3.metric("BIAS", bias)

    st.divider()

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.subheader("🕵️ Radar de Valor")
        dist_poc = (now - poc) * 10000
        st.write(f"**Vs POC Ayer:** {abs(dist_poc):.1f} pips ({'Sobre' if dist_poc > 0 else 'Bajo'})")
        
        # LÓGICA SOLICITADA: < 40 ESTABLE
        if abs(basis) < 4
