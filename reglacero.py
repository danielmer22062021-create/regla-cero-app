
import streamlit as st
from datetime import datetime

# 1. Configuración Base
st.set_page_config(page_title="REGLA CERO V5.3", layout="wide")

# 2. Estética Pro
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; }
    .card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Datos de Auditoría
st.sidebar.title("📊 AUDITORÍA")

with st.sidebar.expander("1. ARBITRAJE (BASIS)", expanded=True):
    fut_p = st.number_input("Futuros", format="%.5f", value=1.09100)
    spot_p = st.number_input("Spot", format="%.5f", value=1.09085)
    v_basis = (fut_p - spot_p) * 10000

with st.sidebar.expander("2. NIVELES AYER", expanded=True):
    h_p = st.number_input("PDH", format="%.5f", value=1.09500)
    l_p = st.number_input("PDL", format="%.5f", value=1.08500)
    poc_p = st.number_input("POC", format="%.5f", value=1.09000)

with st.sidebar.expander("3. ASIA RANGE", expanded=True):
    ah_p = st.number_input("Asia High", format="%.5f", value=1.09200)
    al_p = st.number_input("Asia Low", format="%.5f", value=1.08800)

with st.sidebar.expander("4. CONTEXTO", expanded=True):
    now_p = st.number_input("Precio Actual", format="%.5f", value=1.09050)
    bias_d = st.selectbox("Bias Diario", ["Alcista", "Bajista", "Rango"])
    oi_c = st.number_input("OI CME", value=0)

with st.sidebar.expander("5. GESTIÓN", expanded=False):
    cap = st.number_input("Capital", value=10000)
    sl_p = st.number_input("SL Pips", value=10)

# --- LÓGICA DE TRADING ---
signal = "ESPERA"
s_color = "#f59e0b"

# Cálculo de Lotes (Seguro)
divisor = (sl_p * 10)
lots = (cap * 0.01) / divisor if divisor > 0 else 0.0

if bias_d == "Alcista" and now_p < al_p and now_p >= l_p:
    signal = "COMPRA (JUDAS)"
    s_color = "#00ff41"
elif bias_d == "Bajista" and now_p > ah_p and now_p <= h_p:
    signal = "VENTA (JUDAS)"
    s_color = "#ff4b4b"

# --- INTERFAZ ---
st.title("🛡️ TERMINAL REGLA CERO")

c1, c2, c3, c4 = st.columns(4)
c1.metric("GATILLO", signal)
c2.metric("BASIS", f"{v_basis:.2f}")
c3.metric("LOTS", f"{lots:.2f}")
c4.metric("OI", f"{oi_c}")

st.divider()

col_l, col_r = st.columns([1.5, 1])

with col_l:
    st.subheader("Análisis de Flujo")
    p_dist = (now_p - poc_p) * 10000
    st.write(f"Distancia al POC: {p_dist:.1f} pips")
    
    if abs(v_basis) > 2.5:
        st.error(f"BASIS ALTO: {v_basis:.2f}")
    else:
        st.success("BASIS ESTABLE")
    
    st.write("---")
    st.checkbox("¿Precio en Zona de Valor?")
    st.checkbox("¿Confirmación ATAS?")

with col_r:
    st.subheader("📸 Snapshot")
    # Fecha formateada antes para evitar errores en el f-string
    fecha_h = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Construcción limpia de la ficha
    ficha_html = f"""
    <div class="card">
        <h2 style="color:{s_color};">{signal}</h2>
        <hr style="border-color:#374151;">
        <p><b>Precio:</b> {now_p:.5f}</p>
        <p><b>Asia:</b> {al_p:.5f} / {ah_p:.5f}</p>
        <p><b>POC:</b> {poc_p:.5f}</p>
        <p><b>Basis:</b> {v_basis:.2f}</p>
        <hr style="border-color:#374151;">
        <p style="font-size:0.8em; color:#8b949e;">{fecha_h}</p>
    </div>
    """
    st.markdown(ficha_html, unsafe_allow_html=True)
