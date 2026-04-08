import streamlit as st
from datetime import datetime

# 1. Configuración de la Terminal
st.set_page_config(page_title="REGLA CERO V5.2 | PRO", layout="wide")

# 2. Estética Profesional (CSS)
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; }
    .snapshot-card { background-color: #111827; padding: 20px; border: 2px solid #374151; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Auditoría Técnica
st.sidebar.title("AUDITORIA")

with st.sidebar.expander("1. BASIS (ARBITRAJE)", expanded=True):
    f_price = st.number_input("Futuros CME", format="%.5f", value=1.09100)
    s_price = st.number_input("Spot Broker", format="%.5f", value=1.09085)
    calc_basis = (f_price - s_price) * 10000 

with st.sidebar.expander("2. NIVELES HTF", expanded=True):
    p_high = st.number_input("PDH (Ayer)", format="%.5f", value=1.09500)
    p_low = st.number_input("PDL (Ayer)", format="%.5f", value=1.08500)
    p_poc = st.number_input("POC (Ayer)", format="%.5f", value=1.09000)

with st.sidebar.expander("3. RANGO ASIA", expanded=True):
    a_high = st.number_input("Asia High", format="%.5f", value=1.09200)
    a_low = st.number_input("Asia Low", format="%.5f", value=1.08800)

with st.sidebar.expander("4. CONTEXTO", expanded=True):
    c_price = st.number_input("Precio Actual", format="%.5f", value=1.09050)
    d_bias = st.selectbox("Sesgo Diario", ["Alcista", "Bajista", "Rango"])
    dxy_val = st.selectbox("DXY", ["Debil", "Fuerte", "Rango"])
    oi_contracts = st.number_input("OI CME", value=0)

with st.sidebar.expander("5. GESTION", expanded=False):
    balance = st.number_input("Capital $", value=10000)
    sl_input = st.number_input("SL Pips", value=10)

# --- LOGICA DE TRADING ---
gatillo = "ESPERA"
status_color = "#f59e0b"

# Filtro de seguridad para lotaje (evitar division por cero)
divisor = (sl_input * 10)
lotaje_final = (balance * 0.01) / divisor if divisor > 0 else 0.0

if d_bias == "Alcista" and c_price < a_low and c_price >= p_low:
    gatillo = "COMPRA (JUDAS)"
    status_color = "#00ff41"
elif d_bias == "Bajista" and c_price > a_high and c_price <= p_high:
    gatillo = "VENTA (JUDAS)"
    status_color = "#ff4b4b"

# --- INTERFAZ ---
st.title("🛡️ REGLA CERO - V5.2")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("GATILLO", gatillo)
col_m2.metric("BASIS", f"{calc_basis:.2f}")
col_m3.metric("LOTS", f"{lotaje_final:.2f}")
col_m4.metric("OI", f"{oi_contracts}")

st.divider()

left_col, right_col = st.columns([1.5, 1])

with left_col:
    st.subheader("Analisis de Flujo")
    distancia_poc = (c_price - p_poc) * 10000
    st.write(f"Distancia al POC: {distancia_poc:.1f} pips")
    
    if abs(calc_basis) > 2.5:
        st.warning(f"BASIS ALTO: {calc_basis:.2f}. Arbitraje bajo presion.")
    else:
        st.success("BASIS NORMAL. Arbitraje estable.")
    
    st.write("---")
    st.checkbox("¿El precio esta en zona de valor?")
    st.checkbox("¿Confirmacion en ATAS detectada?")

with right_col:
    # Ficha Snapshot limpia
    st.markdown(f"""
    <div class="snapshot-card">
        <h3 style="color:{status_color}; text-align:center;">{gatillo}</h3>
        <hr style="border-color:#374151;">
        <p><b>Precio:</b> {c_price:.5f}</p>
        <p><b>Asia:</b> {a_low:.5f} / {a_high:.5f}</p>
        <p><b>POC:</b> {p_poc:.5f}</p>
        <p><b>Basis:</b> {calc_basis
