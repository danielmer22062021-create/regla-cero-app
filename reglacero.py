import streamlit as st
from datetime import datetime

# 1. Configuración Base
st.set_page_config(page_title="REGLA CERO V8.0 | London SD", layout="wide")

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
    
    with st.sidebar.expander("1. CAJA ASIA & ABIERTO", expanded=True):
        a_h = st.number_input("Asia High", format="%.5f", value=1.09200)
        a_l = st.number_input("Asia Low", format="%.5f", value=1.08800)
        london_open = st.number_input("London Open (3AM)", format="%.5f", value=1.09000)

    with st.sidebar.expander("2. DESVIACIONES MANUALES", expanded=True):
        st.write("**Proyecciones Superiores**")
        sd_15_pos = st.number_input("SD +1.5 (Venta)", format="%.5f", value=a_h + 0.0015)
        sd_25_pos = st.number_input("SD +2.5 (Extrema)", format="%.5f", value=a_h + 0.0025)
        st.write("**Proyecciones Inferiores**")
        sd_15_neg = st.number_input("SD -1.5 (Compra)", format="%.5f", value=a_l - 0.0015)
        sd_25_neg = st.number_input("SD -2.5 (Extrema)", format="%.5f", value=a_l - 0.0025)
    
    with st.sidebar.expander("3. ARBITRAJE (CME)", expanded=True):
        f_p = st.number_input("Futuros", format="%.5f", value=1.09100)
        s_p = st.number_input("Spot", format="%.5f", value=1.09085)
        # Diferencia en puntos (Basis)
        v_basis = (f_p - s_p) * 100000 

    with st.sidebar.expander("4. CONTEXTO LONDRES", expanded=True):
        now_p = st.number_input("Precio Actual", format="%.5f", value=1.09050)
        bias_d = st.selectbox("Bias Diario", ["Alcista", "Bajista", "Rango"])
        oi_c = st.number_input("OI CME", value=0)

    # Gestión de Riesgo
    cap = st.sidebar.number_input("Capital $", value=10000)
    sl_p = st.sidebar.number_input("SL Pips", value=10)

    # --- LÓGICA DE GATILLO (BASADA EN SD MANUALES) ---
    signal = "ESPERA"
    s_color = "#f59e0b"
    
    if bias_d == "Alcista" and now_p <= sd_15_neg and now_p >= sd_25_neg:
        signal = "JUDAS LONG (ZONA SD)"
        s_color = "#00ff41"
    elif bias_d == "Bajista" and now_p >= sd_15_pos and now_p <= sd_25_pos:
        signal = "JUDAS SHORT (ZONA SD)"
        s_color = "#ff4b4b"

    # --- INTERFAZ LONDRES ---
    st.markdown('<div class="session-header"><h1>🇬🇧 LONDON SESSION TERMINAL</h1></div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("ESTADO LND", signal)
    m2.metric("BASIS (PTS)", f"{v_basis:.1f}")
    m3.metric("LOTS", f"{(cap * 0.01) / (sl_p * 10) if sl_p > 0 else 0:.2f}")
    m4.metric("OI INFO", f"{oi_c}")

    st.divider()

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.subheader("🕵️ Radar de Niveles")
        dist_open = (now_p - london_open) * 10000
        st.write(f"**Precio vs London Open:** {'Sobre' if dist_open > 0 else 'Bajo'} el Open ({abs(dist_open):.1f} pips)")
        
        # Lógica de Arbitraje < 40
        if abs(v_basis) < 40:
            st.success(f"✅ Arbitraje Estable ({v_basis:.1f})")
        else:
            st.error(f"🚨 Presión en Arbitraje ({v_basis:.1f})")

        st.write("---")
        st.write("### 📏 Desviaciones Manuales Activas")
        c_sd1, c_sd2 = st.columns(2)
        with c_sd1:
            st.markdown(f'<div class="level-box" style="color:#ff4b4b;">+2.5 SD: {sd_25_pos:.5f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="level-box" style="color:#ff4b4b;">+1.5 SD: {sd_15_pos:.5f}</div>', unsafe_allow_html=True)
        with c_sd2:
            st.markdown(f'<div class="level-box" style="color:#00ff41;">-1.5 SD: {sd_15_neg:.5f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="level-box" style="color:#00ff41;">-2.5 SD: {sd_25_neg:.5f}</div>', unsafe_allow_html=True)

    with col_r:
        st.subheader("📸 London Snapshot")
        fecha_h = datetime.now().strftime('%Y-%m-%d %H:%M')
        st.markdown(f"""
        <div class="card">
            <h2 style="color:{s_color};">{signal}</h2>
            <hr style="border-color:#374151;">
            <p><b>Precio:</b> {now_p:.5f}</p>
            <p><b>Basis:</b> {v_basis:.1f} pts</p>
            <p><b>Asia:</b> {a_l:.5f} / {a_h:.5f}</p>
            <p><b>Rango Judas:</b> {sd_15_neg:.5f} - {sd_15_pos:.5f}</p>
            <hr style="border-color:#374151;">
            <p style="font-size:0.8em; color:#8b949e;">{fecha_h}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # --- ESPACIO PARA NUEVA YORK ---
    st.markdown('<div class="session-header" style="background: linear-gradient(90deg, #ef4444 0%, #b91c1c 100%);"><h1>🇺🇸 NEW YORK SESSION TERMINAL</h1></div>', unsafe_allow_html=True)
    st.info("Página en construcción. Primero dominemos Londres con las SD manuales.")
