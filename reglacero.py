
import streamlit as st
from datetime import datetime
import pytz

# 1. Configuración de Zona Horaria (NY)
ny_tz = pytz.timezone('America/New_York')
ny_now = datetime.now(ny_tz)

# 2. Configuración Base
st.set_page_config(page_title="REGLA CERO V9.0 | NY Time", layout="wide")

# 3. Estética Terminal
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; }
    .card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; text-align: center; }
    .session-header { background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%); padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
    .level-box { padding: 8px; border-radius: 5px; margin: 4px 0; text-align: center; font-size: 0.9em; border: 1px solid #30363d; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: CENTRO DE MANDO ---
st.sidebar.title("CENTRO DE MANDO")
sesion_activa = st.sidebar.radio("Elegir Sesión:", ["🇬🇧 LONDRES", "🇺🇸 NUEVA YORK"])

st.sidebar.divider()

if sesion_activa == "🇬🇧 LONDRES":
    st.sidebar.subheader("Configuración Londres")
    
    with st.sidebar.expander("1. RANGO DÍA ANTERIOR (4D)", expanded=True):
        pdh = st.number_input("PDH (Ayer)", format="%.4f", value=1.0950)
        pdl = st.number_input("PDL (Ayer)", format="%.4f", value=1.0850)
        p_poc = st.number_input("POC (Valor)", format="%.4f", value=1.0900)

    with st.sidebar.expander("2. CAJA ASIA (4D)", expanded=True):
        a_h = st.number_input("Asia High", format="%.4f", value=1.0920)
        a_l = st.number_input("Asia Low", format="%.4f", value=1.0880)

    with st.sidebar.expander("3. DESVIACIONES MANUALES", expanded=True):
        sd_15_pos = st.number_input("SD +1.5 (Venta)", format="%.4f", value=a_h + 0.0015)
        sd_15_neg = st.number_input("SD -1.5 (Compra)", format="%.4f", value=a_l - 0.0015)
    
    with st.sidebar.expander("4. ARBITRAJE & CONTEXTO", expanded=True):
        f_p = st.number_input("Futuros CME", format="%.4f", value=1.0910)
        s_p = st.number_input("Spot Broker", format="%.4f", value=1.0908)
        # Basis en puntos
        v_basis = (f_p - s_p) * 10000 
        now_p = st.number_input("Precio Actual", format="%.4f", value=1.0905)
        bias_d = st.selectbox("Bias Diario", ["Alcista", "Bajista", "Rango"])

    # Gestión de Riesgo
    cap = st.sidebar.number_input("Capital $", value=10000)
    sl_p = st.sidebar.number_input("SL Pips", value=10)

    # --- LÓGICA DE GATILLO ---
    signal = "ESPERA"
    s_color = "#f59e0b"
    
    if bias_d == "Alcista" and now_p <= sd_15_neg:
        signal = "JUDAS LONG"
        s_color = "#00ff41"
    elif bias_d == "Bajista" and now_p >= sd_15_pos:
        signal = "JUDAS SHORT"
        s_color = "#ff4b4b"

    # --- INTERFAZ LONDRES ---
    st.markdown(f'<div class="session-header"><h1>🇬🇧 LONDON TERMINAL | NY TIME: {ny_now.strftime("%H:%M")}</h1></div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ESTADO LND", signal)
    m2.metric("BASIS (PTS)", f"{v_basis:.1f}")
    m3.metric("LOTS", f"{(cap * 0.01) / (sl_p * 10) if sl_p > 0 else 0:.2f}")
    m4.metric("SESGO", bias_d)

    st.divider()

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.subheader("🕵️ Radar de Valor")
        
        dist_poc = (now_p - p_poc) * 10000
        st.write(f"**Distancia al POC:** {abs(dist_poc):.1f} pips ({'Sobre' if dist_poc > 0 else 'Bajo'})")
        
        if pdl <= now_p <= pdh:
            st.info(f"📍 Precio dentro del Rango HTF ({pdl:.4f} - {pdh:.4f})")
        else:
            st.warning(f"🚀 Fuera de Rango: PDL {pdl:.4f} | PDH {pdh:.4f}")

        if abs(v_basis) < 40:
            st.success(f"✅ Arbitraje Estable ({v_basis:.1f})")
        else:
            st.error(f"🚨 Presión en Arbitraje ({v_basis:.1f})")

        st.write("---")
        st.write("### 📏 Niveles Manuales")
        st.markdown(f'<div class="level-box" style="color:#ff4b4b;">Venta SD +1.5: {sd_15_pos:.4f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="level-box" style="color:#00ff41;">Compra SD -1.5: {sd_15_neg:.4f}</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("📸 Snapshot")
        st.markdown(f"""
        <div class="card">
            <h2 style="color:{s_color};">{signal}</h2>
            <hr style="border-color:#374151;">
            <p><b>Precio:</b> {now_p:.4f}</p>
            <p><b>POC Ayer:</b> {p_poc:.4f}</p>
            <p><b>Basis:</b> {v_basis:.1f} pts</p>
            <hr style="border-color:#374151;">
            <p style="font-size:0.8em; color:#8b949e;">NY TIME: {ny_now.strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown(f'<div class="session-header" style="background: linear-gradient(90deg, #ef4444 0%, #b91c1c 100%);"><h1>🇺🇸 NY SESSION | NY TIME: {ny_now.strftime("%H:%M")}</h1></div>', unsafe_allow_html=True)
    st.info("Configuración de NY pendiente.")
