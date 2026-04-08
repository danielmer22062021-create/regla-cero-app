import streamlit as st
from datetime import datetime

# 1. Configuración Base
st.set_page_config(page_title="REGLA CERO V9.0 | Technical Terminal", layout="wide")

# 2. Estética Terminal Minimalista
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; }
    [data-testid="stSidebar"] { background-color: #0a0d12; border-right: 1px solid #1f2937; }
    .stMetric { background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; text-align: center; }
    .card { background-color: #111827; padding: 20px; border: 1px solid #374151; border-radius: 15px; text-align: center
