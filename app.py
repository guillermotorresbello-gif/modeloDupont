# modelo_dupont_app.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Modelo Dupont", layout="wide")
st.title("Modelo Dupont - Análisis de Rentabilidad Financiera")

# Carga de archivo
uploaded_file = st.file_uploader("Sube tu archivo Excel (.xlsx) con los datos financieros", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name=0)
    df.columns.values[0] = "Indicador"
    df.set_index("Indicador", inplace=True)

    st.subheader("Vista previa de datos cargados")
    st.dataframe(df)

    # Validación de columnas necesarias
    requeridos = ["Utilidad Neta", "Ventas Netas", "Activos Totales", "Capital Contable"]
    faltantes = [col for col in requeridos if col not in df.index]

    if faltantes:
        st.error(f"Faltan los siguientes indicadores requeridos en tu archivo: {', '.join(faltantes)}")
    else:
        st.subheader("Cálculo de Indicadores Dupont")

        # Cálculos
        ventas = df.loc["Ventas Netas"]
        utilidad_neta = df.loc["Utilidad Neta"]
        activos = df.loc["Activos Totales"]
        capital = df.loc["Capital Contable"]

        margen = utilidad_neta / ventas * 100
        rotacion = ventas / activos
        apalancamiento = activos / capital

        roe = margen * rotacion
        roa = rotacion * apalancamiento
        payback_capital = 1 / (roe / 100)
        payback_activos = 1 / (roa / 100)

        # Redondeo según formato solicitado
        resumen = pd.DataFrame({
            "Margen Neto (%)": margen.round(1),
            "Rotación (veces)": rotacion.round(1),
            "Apalancamiento (veces)": apalancamiento.round(1),
            "ROE (%)": roe.round(1),
            "ROA (%)": roa.round(1),
            "Pay Back Capital (veces)": payback_capital.round(1),
            "Pay Back Activos (veces)": payback_activos.round(1)
        }).T

        # Mostrar resultados
        st.dataframe(resumen)

        st.markdown("---")
        st.subheader("Indicaciones")
        st.markdown("""
        - Asegúrate que tu archivo contenga los siguientes indicadores como filas:
            - `Utilidad Neta`, `Ventas Netas`, `Activos Totales`, `Capital Contable`
        - Las columnas deben ser los años o periodos.
        - Los resultados se muestran con:
            - **% con un decimal**: Margen, ROE, ROA
            - **Veces con un decimal**: Rotación, Apalancamiento, Pay Back
        """)
else:
    st.info("Por favor, sube un archivo .xlsx para comenzar el análisis.")
