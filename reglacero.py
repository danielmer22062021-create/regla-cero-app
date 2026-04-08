import streamlit as st
from datetime import datetime

# 1. Configuración Base
st.set_page_config(page_title="REGLA CERO V8.5 | Value Radar", layout="wide")

# 2. Estética Terminal
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
st.sidebar.title("🎮 CENTRO DE MANDO")
sesion_activa = st.sidebar.radio("Elegir Sesión:", ["🇬🇧 LONDRES", "🇺🇸 NUEVA YORK"])

st.sidebar.divider()

if sesion_activa == "🇬🇧 LONDRES":
    st.sidebar.subheader("Configuración Londres")
    
    with st.sidebar.expander("1. RANGO DÍA ANTERIOR (HTF)", expanded=True):
        pdh = st.number_input("PDH (Máximo Ayer)", format="%.5f", value=1.09500)
        pdl = st.number_input("PDL (Mínimo Ayer)", format="%.5f", value=1.08500)
        p_poc = st.number_input("POC (Valor Ayer)", format="%.5f", value=1.09000)

    with st.sidebar.expander("2. CAJA ASIA", expanded=True):
        a_h = st.number_input("Asia High", format="%.5f", value=1.09200)
        a_l = st.number_input("Asia Low", format="%.5f", value=1.08800)

    with st.sidebar.expander("3. DESVIACIONES MANUALES", expanded=True):
        sd_15_pos = st.number_input("SD +1.5 (Venta)", format="%.5f", value=a_h + 0.0015)
        sd_25_pos = st.number_input("SD +2.5 (Extrema)", format="%.5f", value=a_h + 0.0025)
        sd_15_neg = st.number_input("SD -1.5 (Compra)", format="%.5f", value=a_l - 0.0015)
        sd_25_neg = st.number_input("SD -2.5 (Extrema)", format="%.5f", value=a_l - 0.0025)
    
    with st.sidebar.expander("4. ARBITRAJE & CONTEXTO", expanded=True):
        f_p = st.number_input("Futuros CME", format="%.5f", value=1.09100)
        s_p = st.number_input("Spot Broker", format="%.5f", value=1.09085)
        v_basis = (f_p - s_p) * 100000 
        now_p = st.number_input("Precio Actual", format="%.5f", value=1.09050)
        bias_d = st.selectbox("Bias Diario", ["Alcista", "Bajista", "Rango"])

    # Gestión de Riesgo
    cap = st.sidebar.number_input("Capital $", value=10000)
    sl_p = st.sidebar.number_input("SL Pips", value=10)

    # --- LÓGICA DE GATILLO ---
    signal = "ESPERA"
    s_color = "#f59e0b"
    
    if bias_d == "Alcista" and now_p <= sd_15_neg and now_p >= pdl:
        signal = "JUDAS LONG (VALUE BUY)"
        s_color = "#00ff41"
    elif bias_d == "Bajista" and now_p >= sd_15_pos and now_p <= pdh:
        signal = "JUDAS SHORT (VALUE SELL)"
        s_color = "#ff4b4b"

    # --- INTERFAZ LONDRES ---
    st.markdown('<div class="session-header"><h1>🇬🇧 LONDON SESSION TERMINAL</h1></div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ESTADO LND", signal)
    m2.metric("BASIS (PTS)", f"{v_basis:.1f}")
    m3.metric("LOTS", f"{(cap * 0.01) / (sl_p * 10) if sl_p > 0 else 0:.2f}")
    m4.metric("SESGO", bias_d)

    st.divider()

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.subheader("🕵️ Radar de Niveles")
        
        # --- PRECIO VS VALOR DÍA ANTERIOR ---
        dist_poc = (now_p - p_poc) * 10000
        st.write(f"**Precio vs Valor Día Anterior (POC):** {'Sobre' if dist_poc > 0 else 'Bajo'} el POC ({abs(dist_poc):.1f} pips)")
        
        # --- ESTADO DENTRO DEL RANGO PDH/PDL ---
        if pdl <= now_p <= pdh:
            st.info(f"📍 El precio está dentro del rango del día anterior (Rango: {pdl:.5f} - {pdh:.5f})")
        elif now_p > pdh:
            st.warning("🚀 El precio ha roto el PDH (Máximo de ayer). Buscando Liquidez Externa.")
        else:
            st.warning("📉 El precio ha roto el PDL (Mínimo de ayer). Buscando Liquidez Externa.")

        # Lógica de Arbitraje < 40
        if abs(v_basis) < 40:
            st.success(f"✅ Arbitraje Estable ({v_basis:.1f})")
        else:
            st.error(f"🚨 Presión en Arbitraje ({v_basis:.1f})")

        st.write("---")
        st.write("### 📏 Niveles de Desviación Proyectados")
        c_sd1, c_sd2 = st.columns(2)
        with c_sd1:
            st.markdown(f'<div class="level-box" style="color:#ff4b4b;">Venta SD +1.5: {sd_15_pos:.5f}</div>', unsafe_allow_html=True)
        with c_sd2:
            st.markdown(f'<div class="level-box" style="color:#00ff41;">Compra SD -1.5: {sd_15_neg:.5f}</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("📸 London Snapshot")
        fecha_h = datetime.now().strftime('%Y-%m-%d %H:%M')
        st.markdown(f"""
        <div class="card">
            <h2 style="color:{s_color};">{signal}</h2>
            <hr style="border-color:#374151;">
            <p><b>Precio:</b> {now_p:.5f}</p>
            <p><b>POC Ayer:</b> {p_poc:.5f}</p>
            <p><b>Rango Ayer:</b> {pdl:.5f} - {pdh:.5f}</p>
            <p><b>Basis:</b> {v_basis:.1f} pts</p>
            <hr style="border-color:#374151;">
            <p style="font-size:0.8em; color:#8b949e;">{fecha_h}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown('<div class="session-header" style="background: linear-gradient(90deg, #ef4444 0%, #b91c1c 100%);"><h1>🇺🇸 NEW YORK SESSION</h1></div>', unsafe_allow_html=True)
    st.info("Configuración de NY pendiente.")
