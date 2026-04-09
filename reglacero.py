import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="REGLA CERO | Macro Terminal", layout="wide")

# 2. ESTÉTICA TERMINAL (DARK MODE)
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    .stMetric { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; }
    .conclusion-box { background-color: #111827; padding: 20px; border-left: 5px solid #3b82f6; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS LOCAL (CSV)
DB_FILE = "bitacora_macro.csv"

def save_data(data_dict):
    df = pd.DataFrame([data_dict])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- SIDEBAR: ENTRADA DE DATOS ---
st.sidebar.title("📊 DATA ENTRY")
fecha = st.sidebar.date_input("Fecha", datetime.now())

with st.sidebar.expander("1. INDICADORES (Data Dump)", expanded=True):
    pce = st.number_input("Core PCE (%)", format="%.1f")
    gdp = st.number_input("GDP Final (%)", format="%.1f")
    claims = st.number_input("Jobless Claims (K)", value=210)
    income = st.number_input("Personal Income (%)", format="%.1f")

with st.sidebar.expander("2. REGLA CERO (CME)", expanded=True):
    oi_change = st.number_input("OI Change", value=0)
    clearport = st.number_input("ClearPort Contracts", value=0)
    dxy_close = st.number_input("DXY Close", format="%.2f")

# --- SECCIÓN CENTRAL: ANÁLISIS ---
st.title("🛡️ REGLA CERO: BITÁCORA FUNDAMENTAL")
st.write(f"Auditoría para el día: **{fecha}**")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📰 Resumen de Artículos (TradingEconomics)")
    articulos_input = st.text_area("Pega aquí los puntos clave de los artículos...", height=200)
    
    # Lógica de conclusión automática basada en los datos
    if st.button("GENERAR CONCLUSIÓN DIARIA"):
        # Lógica de IA Simplificada (Frialdad Matemática)
        bias_macro = "NEUTRAL"
        if pce >= 0.4 and gdp <= 0.5:
            bias_macro = "ESTANFLACIÓN (Bajista Euro / Alcista Dólar)"
        elif pce < 0.3 and gdp > 1.0:
            bias_macro = "GOLDILOCKS (Alcista Euro)"
        
        concl_diaria = f"BIAS: {bias_macro}. El mercado muestra liquidación de {oi_change} contratos con un PCE en {pce}%. La narrativa de los artículos confirma debilidad en ingresos ({income}%)."
        
        st.markdown(f'<div class="conclusion-box"><h4>🔍 VERDICTO INSTITUCIONAL:</h4><p>{concl_diaria}</p></div>', unsafe_allow_html=True)
        
        # Guardar en DB
        data = {
            "fecha": fecha, "pce": pce, "gdp": gdp, "claims": claims, 
            "income": income, "oi": oi_change, "clearport": clearport,
            "dxy": dxy_close, "articulos": articulos_input, "conclusion": concl_diaria
        }
        save_data(data)
        st.success("Día guardado en la bitácora.")

with col2:
    st.subheader("📋 Checkpoint de Sesión")
    st.checkbox("¿El DXY rompió el nivel psicológico?")
    st.checkbox("¿Hubo divergencia precio/OI?")
    st.checkbox("¿La noticia causó un Judas Swing?")

# --- HISTÓRICO Y CIERRE SEMANAL ---
st.divider()
st.subheader("📈 TENDENCIA SEMANAL")

if os.path.isfile(DB_FILE):
    history_df = pd.read_csv(DB_FILE)
    st.dataframe(history_df.tail(5), use_container_width=True)
    
    # Gráfico de OI vs Precio (Simulado)
    st.line_chart(history_df.set_index('fecha')[['oi']])
else:
    st.info("Aún no hay datos guardados para mostrar tendencias.")

