import streamlit as st
from datetime import datetime

# 1. Configuración Base
st.set_page_config(page_title="REGLA CERO V7.0 | Judas Hunter", layout="wide")

# 2. Estética Terminal
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; text-align: center; }
    .card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; }
    .session-header { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
    .level-box { padding: 10px; border-radius: 5px; margin: 5px 0; text-align: center; font-weight: bold; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUTS DE ASIA ---
st.sidebar.title("🎮 LONDRES ESTRATEGY")

with st.sidebar.expander("📦 CAJA DE ASIA (INPUT)", expanded=True):
    a_h = st.number_input("Asia High", format="%.5f", value=1.09200)
    a_l = st.number_input("Asia Low", format="%.5f", value=1.08800)
    range_size = a_h - a_l
    st.caption(f"Tamaño del Rango: {range_size*10000:.1f} pips")

with st.sidebar.expander("⚡ CONTEXTO ACTUAL", expanded=True):
    now_p = st.number_input("Precio Actual", format="%.5f", value=1.09050)
    bias_d = st.selectbox("Bias Diario", ["Alcista", "Bajista", "Consolidación"])

# --- CÁLCULO AUTOMÁTICO DE DESVIACIONES (SD) ---
def calc_sd(val): return a_h + (range_size * val) if val > 0 else a_l + (range_size * val)

devs = {
    "2.5": calc_sd(2.5), "2.0": calc_sd(2.0), "1.5": calc_sd(1.5), "1.0": calc_sd(1.0),
    "-1.0": calc_sd(-1.0), "-1.5": calc_sd(-1.5), "-2.0": calc_sd(-2.0), "-2.5": calc_sd(-2.5)
}

# --- LÓGICA DE ESCENARIOS (JUDAS VS CONTINUACIÓN) ---
signal = "ESPERA"
narrativa = "El precio está dentro del rango de Asia. No hay ventaja estadística."
s_color = "#f59e0b"

# Escenario Judas Swing Long (Reversión)
if now_p < a_l and now_p >= devs["-1.5"] and bias_d == "Alcista":
    signal = "JUDAS SWEEP (REVERSIÓN LONG)"
    narrativa = "Manipulación detectada por debajo de Asia Low. El precio está en zona de OTE institucional (-1 a -1.5 SD). Busca MSS para largos."
    s_color = "#00ff41"

# Escenario Judas Swing Short (Reversión)
elif now_p > a_h and now_p <= devs["1.5"] and bias_d == "Bajista":
    signal = "JUDAS SWEEP (REVERSIÓN SHORT)"
    narrativa = "Manipulación detectada por encima de Asia High. El precio está en zona de OTE institucional (1 a 1.5 SD). Busca MSS para cortos."
    s_color = "#ff4b4b"

# Escenarios de Continuación
elif now_p > devs["2.0"] and bias_d == "Alcista":
    signal = "CONTINUACIÓN ALCISTA"
    narrativa = "Fuerza extrema. El precio rompió la desviación 2.0 con intención. No busques reversiones, el Order Flow es alcista."
    s_color = "#3b82f6"
elif now_p < devs["-2.0"] and bias_d == "Bajista":
    signal = "CONTINUACIÓN BAJISTA"
    narrativa = "Fuerza extrema. El precio rompió la desviación -2.0. El mercado está en modo expansión, busca retrocesos para seguir vendiendo."
    s_color = "#3b82f6"

# --- INTERFAZ PRINCIPAL ---
st.markdown('<div class="session-header"><h1>🇬🇧 LONDON TERMINAL: JUDAS HUNTER</h1></div>', unsafe_allow_html=True)

st.metric("ESTADO DEL MERCADO", signal)
st.info(f"📝 **Narrativa:** {narrativa}")

st.divider()

col_devs, col_map = st.columns([1, 1.5])

with col_devs:
    st.subheader("📏 Desviaciones Proyectadas")
    
    st.write("**ZONA DE VENTAS (Standard Deviations)**")
    st.markdown(f'<div class="level-box" style="color: #ff4b4b;">2.5 SD: {devs["2.5"]:.5f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="level-box" style="color: #ff4b4b;">1.5 SD: {devs["1.5"]:.5f} (Judas Target)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="level-box" style="color: #ff4b4b;">1.0 SD: {devs["1.0"]:.5f}</div>', unsafe_allow_html=True)
    
    st.write("**ZONA DE COMPRAS (Standard Deviations)**")
    st.markdown(f'<div class="level-box" style="color: #00ff41;">-1.0 SD: {devs["-1.0"]:.5f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="level-box" style="color: #00ff41;">-1.5 SD: {devs["-1.5"]:.5f} (Judas Target)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="level-box" style="color: #00ff41;">-2.5 SD: {devs["-2.5"]:.5f}</div>', unsafe_allow_html=True)

with col_map:
    st.subheader("🕵️ Radar de Sesión")
    st.write(f"**Asia High:** {a_h:.5f} | **Asia Low:** {a_l:.5f}")
    st.write(f"**Precio Actual:** {now_p:.5f}")
    
    dist_high = (now_p - a_h) * 10000
    dist_low = (now_p - a_l) * 10000
    
    st.write(f"Distancia a Asia High: {dist_high:.1f} pips")
    st.write(f"Distancia a Asia Low: {dist_low:.1f} pips")
    
    st.divider()
    st.write("### ✅ Regla Cero - Confirmaciones")
    st.checkbox("¿El DXY está alineado con el movimiento?")
    st.checkbox("¿El OI del CME aumentó en esta zona?")
    st.checkbox("¿Hay absorción de órdenes en ATAS?")
