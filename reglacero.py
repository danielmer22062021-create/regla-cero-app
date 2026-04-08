import streamlit as st
from datetime import datetime
import pytz

# 1. Configuración de Tiempo (NY)
ny_tz = pytz.timezone('America/New_York')
ny_now = datetime.now(ny_tz)
hora_print = ny_now.strftime("%H:%M")
fecha_print = ny_now.strftime("%Y-%m-%d")

# 2. Configuración de Página
st.set_page_config(page_title="REGLA CERO V9.2", layout="wide")

# 3. Diseño Profesional
st.markdown("""
<style>
.main { background-color: #05070a; color: #e0e0e0; }
[data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
.stMetric { background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; text-align: center; }
.card { background-color: #11
