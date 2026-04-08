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
        st.markdown("### 🌏 Caja de Asia")
        ah = st.number_input("Asia High", format="%.4f", value=1.0920)
        al = st.number_input("Asia Low", format="%.4f", value=1.0880)
        now_p = st.number_input("Precio Actual", format="%.4f", value=1.0905)

    with col2:
        st.markdown("### 📊 Valor de Ayer")
        pdh = st.number_input("PDH (Máximo)", format="%.4f", value=1.0950)
        pdl = st.number_input("PDL (Mínimo)", format="%.4f", value=1.0850)
        poc = st.number_input("POC (Valor)", format="%.4f", value=1.0900)

    with col3:
        st.markdown("### ⛓️ Contexto")
        basis = st.number_input("Arbitraje (Puntos)", value=10.0)
        bias = st.selectbox("Sesgo Diario", ["Alcista", "Bajista", "Rango"])
        session = st.selectbox("Sesión Actual", ["Londres", "Nueva York"])

    # BOTÓN DE ACCIÓN
    submitted = st.form_submit_button("AUDITAR SESIÓN")

# --- LÓGICA Y RESULTADOS (Solo se muestran al dar click) ---
if submitted:
    # Cálculos
    r_size = ah - al
    sd15_p = ah + (r_size * 1.5)
    sd15_n = al - (r_size * 1.5)
    dist_poc = (now_p - poc) * 10000
    
    # Lógica de Estado
    state = "ESPERA"
    color = "#f59e0b"
    if now_p < al:
        state = "JUDAS LONG" if now_p >= sd15_n else "EXPANSIÓN BAJA"
        color = "#00ff41" if "LONG" in state else "#ef4444"
    elif now_p > ah:
        state = "JUDAS SHORT" if now_p <= sd15_p else "EXPANSIÓN ALZA"
        color = "#ef4444" if "SHORT" in state else "#00ff41"

    st.divider()

    # Layout de Resultados
    res_col1, res_col2 = st.columns([1.5, 1])

    with res_col1:
        st.header("🎯 Veredicto Técnico")
        st.metric("ESTADO ACTUAL", state)
        
        # Sensor Arbitraje < 40
        if abs(basis) < 40:
            st.success(f"✅ ARBITRAJE ESTABLE: {basis:.1f} pts")
        else:
            st.error(f"🚨 PRESIÓN EN ARBITRAJE: {basis:.1f} pts")
            
        st.write(f"**Distancia al Valor (POC):** {abs(dist_poc):.1f} pips ({'Sobre' if dist_poc > 0 else 'Bajo'})")
        
        # Niveles Proyectados
        st.markdown("### 📏 Niveles de Referencia")
        st.write(f"Venta (1.5 SD): **{sd15_p:.4f}**")
        st.write(f"Compra (-1.5 SD): **{sd15_n:.4f}**")
        st.write(f"Rango HTF: **{pdl:.4f} - {pdh:.4f}**")

    with res_col2:
        st.header("📸 Snapshot")
        # Variables de texto para el Snapshot
        p_txt = f"{now_p:.4f}"
        b_txt = f"{basis:.1f}"
        poc_txt = f"{poc:.4f}"
        range_txt = f"{pdl:.4f}-{pdh:.4f}"
        
        st.markdown(f"""
        <div class="card">
            <h2 style="color:{color};">{state}</h2>
            <hr style="border: 0.5px solid #374151;">
            <p><b>Precio:</b> {p_txt}</p>
            <p><b>Basis:</b> {b_txt} pts</p>
            <p><b>POC Ayer:</b> {poc_txt}</p>
            <p><b>Rango HTF:</b> {range_txt}</p>
            <p><b>Bias:</b> {bias}</p>
            <hr style="border: 0.5px solid #374151;">
            <p style="font-size:0.8em; color:#8b949e;">{f_ny} {h_ny} NY TIME</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Ingresa los datos arriba y presiona el botón para generar el análisis.")
