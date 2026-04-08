import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Regla Cero - Motor de Escenarios", layout="wide")

# Estilo personalizado (Dark Mode vibe)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INPUT DE DATOS (AUDITORÍA MANUAL) ---
st.sidebar.header("📊 Auditoría de Sesión")
st.sidebar.subheader("Paso 1: Macro (CME/COT)")

cot_bias = st.sidebar.selectbox("Sesgo COT", ["Net Long", "Net Short", "Neutral"])
oi_delta = st.sidebar.number_input("Variación OI (Contratos)", value=0, step=500)
dxy_trend = st.sidebar.selectbox("Tendencia DXY", ["Bajista (Soporte Roto)", "Alcista (Resistencia Rota)", "Rango / Indeciso"])

st.sidebar.divider()
st.sidebar.subheader("Paso 2: Mapa Maestro (TV)")
pdh = st.sidebar.number_input("Price Daily High (PDH)", format="%.5f", value=1.09500)
pdl = st.sidebar.number_input("Price Daily Low (PDL)", format="%.5f", value=1.08500)
asia_low = st.sidebar.number_input("Asia Low", format="%.5f", value=1.08800)

st.sidebar.divider()
st.sidebar.subheader("Paso 3: Radar (ATAS)")
cvd_state = st.sidebar.selectbox("CVD / Delta", ["Agresión a favor de sesgo", "Divergencia detectada", "Neutral"])
dom_walls = st.sidebar.checkbox("¿Muros >300 detectados?")

# --- LÓGICA DEL MOTOR DE ESCENARIOS ---
bias_result = "FUERA DE MERCADO"
probability = "Baja"
color = "gray"

# Lógica Simplificada de la Matriz
if cot_bias == "Net Long" and oi_delta > 0 and dxy_trend == "Bajista (Soporte Roto)":
    bias_result = "EXPANSIÓN ALCISTA (A+)"
    probability = "Alta"
    color = "green"
elif cot_bias == "Net Short" and oi_delta > 0 and dxy_trend == "Alcista (Resistencia Rota)":
    bias_result = "EXPANSIÓN BAJISTA (A+)"
    probability = "Alta"
    color = "red"
elif oi_delta < 0:
    bias_result = "POSIBLE TRAMPA / LIQUIDACIÓN"
    probability = "Media-Baja"
    color = "orange"

# --- DASHBOARD PRINCIPAL ---
st.title("🛡️ Motor de Escenarios: Regla Cero")
st.caption("Foco Técnico | Sin Suposiciones | Rigor Matemático")

col1, col2, col3 = st.columns(3)
col1.metric("SESGO DIRECCIONAL", bias_result)
col2.metric("PROBABILIDAD", probability)
col3.metric("CONFLUENCIA DXY", dxy_trend)

st.divider()

# --- GENERACIÓN DE NARRATIVA ---
st.header("📖 Narrativa Técnica del Día")

if bias_result == "EXPANSIÓN ALCISTA (A+)":
    st.success(f"**Escenario de Alta Probabilidad:** El mercado tiene gasolina real (OI UP). "
               f"Busca el **Judas Swing** por debajo de Asia Low ({asia_low}) para cargar largos.")
    st.info(f"**Target Principal:** PDH en {pdh}. Si el CVD confirma agresión en el descuento, ejecuta con confianza.")

elif bias_result == "EXPANSIÓN BAJISTA (A+)":
    st.error(f"**Escenario de Alta Probabilidad:** Sesgo institucional vendedor confirmado. "
             f"Busca manipulación por encima de Asia High o retroceso a FVG en Premium.")
    st.info(f"**Target Principal:** PDL en {pdl}. Vigila muros de 300+ en el Smart DOM para proteger el SL.")

else:
    st.warning("⚠️ **ALERTA:** No hay confluencia clara entre COT, OI y DXY. El algoritmo recomienda esperar o buscar solo scalps rápidos en zonas de liquidez extrema.")

st.divider()

# --- CHECKLIST DE DISCIPLINA ---
st.subheader("✅ Checklist de Ejecución (Regla Cero)")
c1, c2, c3 = st.columns(3)
with c1:
    st.checkbox("¿El precio está en zona de descuento/premium?")
    st.checkbox("¿Hubo toma de liquidez previa?")
with c2:
    st.checkbox("¿El DXY confirma el movimiento?")
    st.checkbox("¿CVD muestra divergencia o absorción?")
with c3:
    st.checkbox("¿El SL está protegido por un muro en el DOM?")
    st.checkbox("¿Riesgo/Beneficio es mínimo 1:3?")

if st.button("Guardar en Bitácora"):
    st.write("Datos guardados. Mantén la disciplina.")
