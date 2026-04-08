import streamlit as st
from datetime import datetime

# Configuración Pro
st.set_page_config(page_title="Regla Cero V3.1 - Snapshot Ready", layout="wide")

# Estilo Dark Pro
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: DATOS MAESTROS ---
st.sidebar.header("🛡️ Auditoría Regla Cero")

with st.sidebar.expander("1. Energía (CME/COT)", expanded=True):
    cot_bias = st.selectbox("Sesgo COT", ["Comprador (Long)", "Vendedor (Short)", "Neutral"])
    oi_delta = st.number_input("Variación OI", value=0, step=1000)
    dxy_state = st.selectbox("DXY", ["Baja", "Sube", "Rango"])

with st.sidebar.expander("2. Mapa Maestro (TV)", expanded=True):
    price_zone = st.select_slider("Zona", options=["Discount", "Equilibrium", "Premium"], value="Equilibrium")
    liquidity_target = st.selectbox("Objetivo (ERL)", ["PDH", "PDL", "Asia H/L", "Equal Highs"])

with st.sidebar.expander("3. Confirmación (ATAS)", expanded=True):
    cvd_behavior = st.selectbox("CVD", ["Divergencia Bullish", "Divergencia Bearish", "Absorción", "Agresión"])
    dom_wall = st.number_input("Muro DOM en:", format="%.5f", value=0.00000)

# --- LÓGICA DE ESCENARIOS ---
decision = "ESPERAR"
confidence = "Baja"
if cot_bias == "Comprador (Long)" and oi_delta > 5000 and dxy_state == "Baja":
    decision = "COMPRA A+" if price_zone == "Discount" else "EVITAR COMPRAS"
    confidence = "Alta" if "COMPRA" in decision else "Nula"
elif cot_bias == "Vendedor (Short)" and oi_delta > 5000 and dxy_state == "Sube":
    decision = "VENTA A+" if price_zone == "Premium" else "EVITAR VENTAS"
    confidence = "Alta" if "VENTA" in decision else "Nula"

# --- DASHBOARD DE TRABAJO ---
st.title("🏹 Sistema de Auditoría V3.1")
c1, c2, c3 = st.columns(3)
c1.metric("GATILLO", decision)
c2.metric("CONFIANZA", confidence)
c3.metric("OI DETECTADO", f"{oi_delta} CTR")

st.divider()

# --- FICHA TÉCNICA PARA CAPTURA DE PANTALLA ---
st.subheader("📸 Ficha de Cierre (Toma una captura de pantalla)")

# Colores para la ficha según el gatillo
if "COMPRA" in decision: card_color = "#00ff41" # Verde
elif "VENTA" in decision: card_color = "#ff4b4b" # Rojo
else: card_color = "#f59e0b" # Naranja (Espera)

# Generación de la Ficha en HTML (limpia para screenshot)
today_date = datetime.now().strftime("%Y-%m-%d %H:%M")
muro_text = "No reportado" if dom_wall == 0 else f"{dom_wall:.5f}"

html_card = f"""
<div style="font-family: Arial, sans-serif; padding: 25px; background-color: #161b22; color: white; border: 2px solid #30363d; border-radius: 15px; width: 450px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); margin: auto;">
    <h2 style="color: {card_color}; margin-top: 0; text-align: center;">Ficha Regla Cero</h2>
    <p style="margin: 5px 0; text-align: center;"><b>📅 Fecha:</b> {today_date}</p>
    <hr style="border: 1px solid #30363d; margin: 15px 0;">
    <p style="margin: 8px 0; font-size: 1.1em;"><b>🎯 GATILLO:</b> <span style="color: {card_color}; font-weight: bold;">{decision}</span></p>
    <p style="margin: 8px 0;"><b>🛡️ Confianza:</b> {confidence}</p>
    <p style="margin: 8px 0;"><b>⛽ OI Detectado:</b> {oi_delta} contratos</p>
    <p style="margin: 8px 0;"><b>🗺️ Zona de Precio:</b> {price_zone}</p>
    <p style="margin: 8px 0;"><b>🎯 Objetivo (ERL):</b> {liquidity_target}</p>
    <p style="margin: 8px 0;"><b>⚡ CVD ATAS:</b> {cvd_behavior}</p>
    <p style="margin: 8px 0;"><b>🧱 Muro DOM:</b> {muro_text}</p>
    <hr style="border: 1px solid #30363d; margin: 15px 0;">
    <p style="font-style: italic; color: #8b949e; font-size: 0.9em; text-align: center;">"La disciplina es la mejor estrategia."</p>
</div>
"""
st.markdown(html_card, unsafe_allow_html=True)
st.caption("Nota: Esta tarjeta está diseñada para que le hagas una captura de pantalla y la guardes como imagen.")
