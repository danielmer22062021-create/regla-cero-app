import streamlit as st
from datetime import datetime
import pytz

# 1. Configuración de Tiempo (NY)
ny_tz = pytz.timezone('America/New_York')
ny_now = datetime.now(ny_tz)

# 2. Configuración de Página
st.set_page_config(page_title="REGLA CERO V9.1", layout="wide")

# 3. Diseño Profesional (Líneas 8-13 protegidas)
st.markdown("""
<style>
.main { background-color: #05070a; color: #e0e0e0; }
[data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
.stMetric { background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; text-align: center; }
.card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; text-align: center; }
.session-header { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
.level-box { padding: 8px; border-radius: 5px; margin: 4px 0; text-align: center; font-size: 0.9em; border: 1px solid #30363d; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CENTRO DE MANDO ---
st.sidebar.title("🎮 CENTRO DE MANDO")
sesion = st.sidebar.radio("Elegir Sesión:", ["🇬🇧 LONDRES", "🇺🇸 NUEVA YORK"])
st.sidebar.divider()

if sesion == "🇬🇧 LONDRES":
    with st.sidebar.expander("1. CAJA ASIA", expanded=True):
        a_h = st.sidebar.number_input("Asia High", format="%.4f", value=1.0920)
        a_l = st.sidebar.number_input("Asia Low", format="%.4f", value=1.0880)
        range_size = a_h - a_l

    with st.sidebar.expander("2. VALOR AYER (HTF)", expanded=True):
        pdh = st.sidebar.number_input("PDH", format="%.4f", value=1.0950)
        pdl = st.sidebar.number_input("PDL", format="%.4f", value=1.0850)
        p_poc = st.sidebar.number_input("POC", format="%.4f", value=1.0900)
    
    with st.sidebar.expander("3. ARBITRAJE & PRECIO", expanded=True):
        f_p = st.sidebar.number_input("Futuros", format="%.4f", value=1.0910)
        s_p = st.sidebar.number_input("Spot", format="%.4f", value=1.0908)
        v_basis = (f_p - s_p) * 100000 
        now_p = st.sidebar.number_input("Precio Actual", format="%.4f", value=1.0905)
        bias_d = st.sidebar.selectbox("Bias Diario", ["Alcista", "Bajista", "Consolidación"])

    # --- CÁLCULO AUTO DE DESVIACIONES ---
    def sd(v): return a_h + (range_size * v) if v > 0 else a_l + (range_size * v)
    
    # --- LÓGICA DE ESTADO (JUDAS / CONTINUACIÓN) ---
    state = "ESPERA"
    s_color = "#f59e0b"
    
    if now_p < a_l: # Manipulación Inferior
        if now_p >= sd(-1.5): state = "JUDAS SWEEP (REVERSIÓN LONG)"
        elif now_p < sd(-2.0): state = "EXPANSIÓN / CONTINUACIÓN BAJISTA"
        s_color = "#00ff41" if "LONG" in state else "#ef4444"
    elif now_p > a_h: # Manipulación Superior
        if now_p <= sd(1.5): state = "JUDAS SWEEP (REVERSIÓN SHORT)"
        elif now_p > sd(2.0): state = "EXPANSIÓN / CONTINUACIÓN ALCISTA"
        s_color = "#ef4444" if "SHORT" in state else "#00ff41"

    # --- INTERFAZ LONDRES ---
    st.markdown(f'<div class="session-header"><h1>🇬🇧 LONDON TERMINAL | NY: {ny_now.strftime("%H:%M")}</h1></div>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("ESTADO", state)
    m2.metric("BASIS (PTS)", f"{v_basis:.1f}")
    m3.metric("BIAS", bias_d)

    st.divider()

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.subheader("🕵️ Radar de Valor")
        dist_poc = (now_p - p_poc) * 10000
        st.write(f"**Vs POC Ayer:** {abs(dist_poc):.1f} pips ({'Sobre' if dist_poc > 0 else 'Bajo'})")
        
        if abs(v_basis) < 40: st.success(f"✅ Arbitraje Estable ({v_basis:.1f})")
        else: st.error(f"🚨 Arbitraje Bajo Presión ({v_basis:.1f})")

        st.write("---")
        st.write("### 📏 Desviaciones Automáticas (Caja Asia)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="level-box" style="color:#ef4444;">2.5 SD: {sd(2.5):.4f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="level-box" style="color:#ef4444;">1.5 SD: {sd(1.5):.4f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="level-box">0.5 SD: {sd(0.5):.4f}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="level-box"> -0.5 SD: {sd(-0.5):.4f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="level-box" style="color:#00ff41;">-1.5 SD: {sd(-1.5):.4f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="level-box" style="color:#00ff41;">-2.5 SD: {sd(-2.5):.4f}</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("📸 Snapshot")
        st.markdown(f"""
        <div class="card">
            <h2 style
