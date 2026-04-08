import streamlit as st
from datetime import datetime

# 1. Configuración Base
st.set_page_config(page_title="REGLA CERO V8.7 | Technical Focus", layout="wide")

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
        pdh = st.sidebar.number_input("PDH (Máximo Ayer)", format="%.4f", value=1.0950)
        pdl = st.sidebar.number_input("PDL (Mínimo Ayer)", format="%.4f", value=1.0850)
        p_poc = st.sidebar.number_input("POC (Valor Ayer)", format="%.4f", value=1.0900)

    with st.sidebar.expander("2. CAJA ASIA", expanded=True):
        a_h = st.sidebar.number_input("Asia High", format="%.4f", value=1.0920)
        a_l = st.sidebar.number_input("Asia Low", format="%.4f", value=1.0880)

    with st.sidebar.expander("3. DESVIACIONES MANUALES", expanded=True):
        sd_15_pos = st.sidebar.number_input("SD +1.5 (Venta)", format="%.4f", value=a_h + 0.0015)
        sd_15_neg = st.sidebar.number_input("SD -1.5 (Compra)", format="%.4f", value=a_l - 0.0015)
    
    with st.sidebar.expander("4. ARBITRAJE & CONTEXTO", expanded=True):
        f_p = st.sidebar.number_input("Futuros CME", format="%.4f", value=1.0910)
        s_p = st.sidebar.number_input("Spot Broker", format="%.4f", value=1.0908)
        v_basis = (f_p - s_p) * 100000 
        now_p = st.sidebar.number_input("Precio Actual", format="%.4f", value=1.0905)
        bias_d = st.sidebar.selectbox("Bias Diario", ["Alcista", "Bajista", "Rango"])

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
    st.markdown('<div class="session-header"><h1>🇬🇧 LONDON SESSION TERMINAL</h1></div>', unsafe_allow_html=True)
    
    # Dashboard con 3 métricas técnicas
    m1, m2, m3 = st.columns(3)
    m1.metric("ESTADO LND", signal)
    m2.metric("BASIS (PTS)", f"{v_basis:.1f}")
    m3.metric("SESGO MACRO", bias_d)

    st.divider()

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.subheader("🕵️ Radar de Niveles")
        
        # --- PRECIO VS VALOR DÍA ANTERIOR ---
        dist_poc = (now_p - p_poc) * 10000
        st.write(f"**Distancia al POC:** {'Sobre' if dist_poc > 0 else 'Bajo'} el POC ({abs(dist_poc):.1f} pips)")
        
        # --- ESTADO DENTRO DEL RANGO PDH/PDL ---
        if pdl <= now_p <= pdh:
            st.info(f"📍 Precio dentro del Rango HTF ({pdl:.4f} - {pdh:.4f})")
        else:
            st.warning(f"🚀 Fuera de Rango: PDL {pdl:.4f} | PDH {pdh:.4f}")

        # Lógica de Arbitraje < 40
        if abs(v_basis) < 40:
            st.success(f"✅ Arbitraje Estable ({v_basis:.1f})")
        else:
            st.error(f"🚨 Presión en Arbitraje ({v_basis:.1f})")

        st.write("---")
        st.write("### 📏 Niveles Manuales")
        st.markdown(f'<div class="level-box" style="color:#ff4b4b;">Venta SD +1.5: {sd_15_pos:.4f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="level-box" style="color:#00ff41;">Compra SD -1.5: {sd_15_neg:.4f}</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("📸 London Snapshot")
        fecha_h = datetime.now().strftime('%Y-%m-%d %H:%M')
        st.markdown(f"""
        <div class="card">
            <h2 style="color:{s_color};">{signal}</h2>
            <hr style="border-color:#374151;">
            <p><b>Precio:</b> {now_p:.4f}</p>
            <p><b>POC Ayer:</b> {p_poc:.4f}</p>
            <p><b>Basis:</b> {v_basis:.1f} pts</p>
            <p><b>Rango HTF:</b> {pdl:.4f}-{pdh:.4f}</p>
            <hr style="border-color:#374151;">
            <p style="font-size:0.8em; color:#8b949e;">{fecha_h}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown('<div class="session-header" style="background: linear-gradient(90deg, #ef4444 0%, #b91c1c 100%);"><h1>🇺🇸 NEW YORK SESSION</h1></div>', unsafe_allow_html=True)
    st.info("Configuración de NY pendiente.")
