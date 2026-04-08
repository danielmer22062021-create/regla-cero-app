import streamlit as st

# Configuración de la página Pro
st.set_page_config(page_title="Regla Cero V2.0 - Order Flow Engine", layout="wide")

# Estilo Dark Pro
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    div.stButton > button:first-child { background-color: #00ff41; color: black; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: DATOS MAESTROS ---
st.sidebar.header("🛡️ Auditoría Regla Cero")

# 1. MACRO (CME)
with st.sidebar.expander("1. Energía (CME/COT)", expanded=True):
    cot_bias = st.selectbox("Sesgo Semanal COT", ["Comprador (Long)", "Vendedor (Short)", "Neutral"])
    oi_delta = st.number_input("Variación OI (Contratos)", value=0, step=1000)
    dxy_state = st.selectbox("Estado DXY", ["Distribución (Baja)", "Acumulación (Sube)", "Rango"])

# 2. ESTRUCTURA (TradingView)
with st.sidebar.expander("2. Mapa Maestro (TV)", expanded=True):
    market_phase = st.selectbox("Fase de Mercado", ["Expansión", "Retroceso", "Consolidación"])
    price_zone = st.select_slider("Zona de Precio (PDH/PDL)", options=["Discount", "Equilibrium", "Premium"], value="Equilibrium")
    fvg_status = st.checkbox("¿Precio dentro de un FVG / Order Block?")
    liquidity_target = st.selectbox("Objetivo de Liquidez (ERL)", ["PDH", "PDL", "Asia H/L", "Equal Highs/Lows"])

# 3. RADAR (ATAS)
with st.sidebar.expander("3. Confirmación (ATAS)", expanded=True):
    cvd_behavior = st.selectbox("Comportamiento CVD", ["Divergencia Bullish", "Divergencia Bearish", "Absorción en Muro", "Agresión a Favor"])
    dom_wall_level = st.number_input("Precio del Muro 300+", format="%.5f", value=0.00000)
    dom_type = st.radio("Función del Muro", ["Soporte/Resistencia (Rebote)", "Imán (El precio va hacia allá)"])

# --- MOTOR DE LÓGICA REFINADA ---
st.title("🏹 Estratega de Escenarios V2.0")
st.caption("Combinando Estructura Institucional (TV) con Agresión Real (ATAS)")

# Inicialización de variables de decisión
decision = "ESPERAR"
confidence = "Baja"
scenario_text = "No se cumplen las condiciones de la Regla Cero."

# LÓGICA ESCENARIO A+ (COMPRA)
if cot_bias == "Comprador (Long)" and oi_delta > 5000 and dxy_state == "Distribución (Baja)":
    if price_zone == "Discount" and cvd_behavior in ["Divergencia Bullish", "Absorción en Muro"]:
        decision = "COMPRA (LONG A+)"
        confidence = "Alta"
        scenario_text = f"**Escenario de Expansión:** El COT y el OI confirman gasolina. El precio está en zona de DESCUENTO. ATAS muestra que los vendedores están siendo absorbidos. El imán es {liquidity_target}."
    elif price_zone == "Premium":
        decision = "EVITAR COMPRAS"
        confidence = "Nula"
        scenario_text = "⚠️ **PELIGRO:** El sesgo es alcista pero el precio está CARO (Premium). Espera retroceso a zona Discount para no entrar en el pico."

# LÓGICA ESCENARIO A+ (VENTA)
elif cot_bias == "Vendedor (Short)" and oi_delta > 5000 and dxy_state == "Acumulación (Sube)":
    if price_zone == "Premium" and cvd_behavior in ["Divergencia Bearish", "Absorción en Muro"]:
        decision = "VENTA (SHORT A+)"
        confidence = "Alta"
        scenario_text = f"**Escenario de Distribución:** DXY fuerte y COT vendedor. Precio en zona PREMIUM. ATAS confirma agotamiento comprador. Buscamos {liquidity_target}."
    elif price_zone == "Discount":
        decision = "EVITAR VENTAS"
        confidence = "Nula"
        scenario_text = "⚠️ **PELIGRO:** El sesgo es bajista pero el precio está BARATO (Discount). Espera manipulación a Premium."

# --- DASHBOARD DE RESULTADOS ---
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("GATILLO", decision)
with c2:
    st.metric("CONFIANZA", confidence)
with c3:
    st.metric("VALOR OI", f"{oi_delta} CTR")

st.divider()

# NARRATIVA DETALLADA
st.subheader("📝 Plan de Batalla")
st.info(scenario_text)

# TABLA DE CONFLUENCIAS
st.subheader("📊 Confluencias Técnicas")
col_a, col_b = st.columns(2)

with col_a:
    st.write("**TradingView (Ubicación)**")
    st.write(f"📍 Fase: {market_phase}")
    st.write(f"📍 Zona: {price_zone}")
    st.write(f"📍 Target: {liquidity_target}")

with col_b:
    st.write("**ATAS (Ejecución)**")
    st.write(f"⚡ CVD: {cvd_behavior}")
    if dom_wall_level > 0:
        st.write(f"🧱 Muro Detectado en: {dom_wall_level} ({dom_type})")
    else:
        st.write("🧱 No se reportan muros significativos.")

st.divider()
st.button("Registrar Sesión en Bitácora")
