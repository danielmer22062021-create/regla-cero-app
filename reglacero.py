import streamlit as st
from datetime import datetime
import pytz

# 1. ZONA HORARIA NY
tz_ny = pytz.timezone('America/New_York')
ahora_ny = datetime.now(tz_ny)
h_display = ahora_ny.strftime("%H:%M")
f_display = ahora_ny.strftime("%Y-%m-%d")

# 2. CONFIGURACIÓN PÁGINA
st.set_page_config(page_title="REGLA CERO V9.3", layout="wide")

# 3. ESTILOS LIMPIOS (Protección de líneas 15-20)
css_code = """
<style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; text-align: center; }
    .card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; text-align: center; }
    .session-header { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
    .level-box { padding: 8px; border-radius: 5px; margin: 4px 0; text-align: center; font-size: 0.9em; border: 1px solid #30363d; font-weight: bold; }
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

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
        bias = st.sidebar.selectbox("Bias Diario", ["Alcista", "Bajista", "Consolidación"])

    # --- DESVIACIONES AUTOMÁTICAS ---
    def get_sd(v): return ah + (r_size * v) if v > 0 else al + (r_size * v)
    
    # --- LÓGICA JUDAS ---
    state = "ESPERA"
    color = "#f59e0b"
    if now < al:
        state = "JUDAS SWEEP (LONG)" if now >= get_sd(-1.5) else "CONTINUACIÓN BAJISTA"
        color = "#00ff41" if "LONG" in state else "#ef4444"
    elif now > ah:
        state = "JUDAS SWEEP (SHORT)" if now <= get_sd(1.5) else "CONTINUACIÓN ALCISTA"
        color = "#ef4444" if "SHORT" in state else "#00ff41"

    # --- INTERFAZ LONDRES ---
    st.markdown(f'<div class="session-header"><h1>🇬🇧 LONDON TERMINAL | NY: {h_display}</h1></div>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("ESTADO", state)
    m2.metric("BASIS (PTS)", f"{basis:.1f}")
    m3.metric("BIAS", bias)

    st.divider()

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.subheader("🕵️ Radar de Valor")
        d_poc = (now - poc) * 10000
        st.write(f"**Vs POC Ayer:** {abs(d_poc):.1f} pips ({'Sobre' if d_poc > 0 else 'Bajo'})")
        
        if abs(basis) < 40: st.success(f"✅ Arbitraje Estable ({basis:.1f})")
        else: st.error(f"🚨 Presión de Basis ({basis:.1f})")

        st.write("---")
        st.write("### 📏 Desviaciones Automáticas")
        cl1, cl2 = st.columns(2)
        with cl1:
            st.markdown(f'<div class="level-box" style="color:#ef4444;">1.5 SD: {get_sd(1.5):.4f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="level-box" style="color:#ef4444;">2.5 SD: {get_sd(2.5):.4f}</div>', unsafe_allow_html=True)
        with cl2:
            st.markdown(f'<div class="level-box" style="color:#00ff41;">-1.5 SD: {get_sd(-1.5):.4f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="level-box" style="color:#00ff41;">-2.5 SD: {get_sd(-2.5):.4f}</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("📸 Snapshot")
        # Snapshot Texto Directo
        snap_html = f"""
        <div class="card">
            <h2 style="color:{color};">{state}</h2>
            <hr style="border: 0.5px solid #374151;">
            <p><b>Precio:</b> {now:.4f}</p>
            <p><b>Basis:</b> {basis:.1f} pts</p>
            <p><b>POC Ayer:</b> {poc:.4f}</p>
            <p><b>Rango:</b> {pdl:.4f} - {pdh:.
