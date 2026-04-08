
import streamlit as st
from datetime import datetime
import pytz
import time

# 1. TIEMPO NY
tz_ny = pytz.timezone('America/New_York')
now_ny = datetime.now(tz_ny)
h_ny = now_ny.strftime("%H:%M:%S") # Añadí segundos para ver el refresh
f_ny = now_ny.strftime("%Y-%m-%d")

# 2. CONFIGURACIÓN
st.set_page_config(page_title="REGLA CERO V10 | Live Terminal", layout="wide")

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

# CONFIGURACIÓN DE AUTO-REFRESCO
st.sidebar.subheader("📡 MODO LIVE")
auto_refresh = st.sidebar.toggle("Activar Auto-Refresco", value=False)
refresh_interval = st.sidebar.slider("Segundos de intervalo", 5, 60, 10)

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

    # --- CÁLCULO DE NIVELES ---
    sd_15_p, sd_25_p = ah + (r_size * 1.5), ah + (r_size * 2.5)
    sd_15_n, sd_25_n = al - (r_size * 1.5), al - (r_size * 2.5)
    
    # --- LÓGICA DE ESTADO ---
    state, color = "ESPERA", "#f59e0b"
    if now < al:
        state = "JUDAS SWEEP (LONG)" if now >= sd_15_n else "CONTINUACIÓN BAJA"
        color = "#00ff41" if "LONG" in state else "#ef4444"
    elif now > ah:
        state = "JUDAS SWEEP (SHORT)" if now <= sd_15_p else "CONTINUACIÓN ALZA"
        color = "#ef4444" if "SHORT" in state else "#00ff41"

    # --- INTERFAZ ---
    st.markdown(f'<div class="session-header"><h1>🇬🇧 LONDON TERMINAL | NY: {h_ny}</h1></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("ESTADO", state)
    c2.metric("BASIS (PTS)", f"{basis:.1f}")
    c3.metric("BIAS", bias)

    st.divider()

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.subheader("🕵️ Radar de Valor")
        d_poc = (now - poc) * 10000
        st.write(f"**Vs POC Ayer:** {abs(d_poc):.1f} pips ({'Sobre' if d_poc > 0 else 'Bajo'})")
        
        # Alerta de Arbitraje < 40
        if abs(basis) < 40: st.success(f"✅ Arbitraje Estable ({basis:.1f})")
        else: st.error(f"🚨 Presión de Basis ({basis:.1f})")

        st.write("---")
        st.write("### 📏 Desviaciones Proyectadas")
        la, lb = st.columns(2)
        with la:
            st.markdown(f'<div class="level-box" style="color:#ef4444;">1.5 SD: {sd_15_p:.4f}</div>', unsafe_allow_html=True)
        with lb:
            st.markdown(f'<div class="level-box" style="color:#00ff41;">-1.5 SD: {sd_15_n:.4f}</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("📸 Snapshot")
        p_v, b_v, poc_v, r_v = f"{now:.4f}", f"{basis:.1f}", f"{poc:.4f}", f"{pdl:.4f}-{pdh:.4f}"
        st.markdown(f"""
        <div class="card">
            <h2 style="color:{color};">{state}</h2>
            <hr style="border: 0.5px solid #374151;">
            <p><b>Precio:</b> {p_v}</p>
            <p><b>Basis:</b> {b_v} pts</p>
            <p><b>POC Ayer:</b> {poc_v}</p>
            <p><b>Rango:</b> {r_v}</p>
            <hr style="border: 0.5px solid #374151;">
            <p style="font-size:0.8em; color:#8b949e;">{f_ny} {h_ny} NY TIME</p>
        </div>
        """, unsafe_allow_html=True)

# --- LÓGICA DE AUTO-REFRESCO ---
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
