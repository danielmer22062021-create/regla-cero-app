import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración Pro
st.set_page_config(page_title="Regla Cero V3.0 - Auditoría Local", layout="wide")

# Estilo Dark Pro
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    div.stButton > button:first-child { background-color: #00ff41; color: black; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: DATOS MAESTROS ---
st.sidebar.header("🛡️ Auditoría Regla Cero")

with st.sidebar.expander("1. Energía (CME/COT)", expanded=True):
    cot_bias = st.selectbox("Sesgo Semanal COT", ["Comprador (Long)", "Vendedor (Short)", "Neutral"])
    oi_delta = st.number_input("Variación OI (Contratos)", value=0, step=1000)
    dxy_state = st.selectbox("Estado DXY", ["Distribución (Baja)", "Acumulación (Sube)", "Rango"])

with st.sidebar.expander("2. Mapa Maestro (TV)", expanded=True):
    price_zone = st.select_slider("Zona de Precio", options=["Discount", "Equilibrium", "Premium"], value="Equilibrium")
    liquidity_target = st.selectbox("Objetivo (ERL)", ["PDH", "PDL", "Asia H/L", "Equal Highs/Lows"])

with st.sidebar.expander("3. Confirmación (ATAS)", expanded=True):
    cvd_behavior = st.selectbox("Comportamiento CVD", ["Divergencia Bullish", "Divergencia Bearish", "Absorción", "Agresión a Favor"])
    dom_wall = st.number_input("Muro 300+ en:", format="%.5f", value=0.00000)

# --- LÓGICA DE ESCENARIOS ---
decision = "ESPERAR"
confidence = "Baja"
if cot_bias == "Comprador (Long)" and oi_delta > 5000 and dxy_state == "Distribución (Baja)":
    decision = "COMPRA (LONG A+)" if price_zone == "Discount" else "EVITAR COMPRAS (CARO)"
    confidence = "Alta" if "COMPRA" in decision else "Nula"
elif cot_bias == "Vendedor (Short)" and oi_delta > 5000 and dxy_state == "Acumulación (Sube)":
    decision = "VENTA (SHORT A+)" if price_zone == "Premium" else "EVITAR VENTAS (BARATO)"
    confidence = "Alta" if "VENTA" in decision else "Nula"

# --- DASHBOARD ---
st.title("🏹 Sistema de Auditoría de Sesión")
c1, c2, c3 = st.columns(3)
c1.metric("GATILLO", decision)
c2.metric("CONFIANZA", confidence)
c3.metric("OI DETECTADO", f"{oi_delta} CTR")

st.divider()

# --- PREPARACIÓN DE DESCARGA ---
# Creamos un diccionario con los datos actuales
data_to_save = {
    "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")],
    "Sesgo_COT": [cot_bias],
    "Variacion_OI": [oi_delta],
    "DXY": [dxy_state],
    "Zona_Precio": [price_zone],
    "CVD_ATAS": [cvd_behavior],
    "Muro_DOM": [dom_wall],
    "Decision_Final": [decision]
}
df = pd.DataFrame(data_to_save)
csv = df.to_csv(index=False).encode('utf-8')

# --- INTERFAZ DE CIERRE ---
st.subheader("📝 Plan y Registro")
st.info(f"Escenario actual detectado bajo la Regla Cero: **{decision}**. Objetivo principal: **{liquidity_target}**.")

# BOTÓN DE DESCARGA
st.download_button(
    label="📥 DESCARGAR REPORTE DE SESIÓN (CSV)",
    data=csv,
    file_name=f"auditoria_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    mime="text/csv",
)

st.caption("Nota: Al hacer clic, se guardará un archivo CSV con todos los parámetros técnicos de hoy.")
