import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Cerrillos Connect",
    page_icon="🚌",
    layout="wide",
)

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Cerrillos Connect: Dashboard de Movilidad")
st.write("Visualización en tiempo real de nodos críticos y tiempos de espera en la comuna.")

data_dict = {
    'lat': [
        -33.482917, # Cruce PAC / Departamental
        -33.483538, # Metro Cerrillos
        -33.490639, # Cruce Lo Errazuriz
        -33.508500  # Plaza Cerrillos
    ],
    'lon': [
        -70.696389, 
        -70.694962, 
        -70.722712, 
        -70.716200
    ],
    'nombre': [
        'Cruce PAC / Departamental', 
        'Metro Cerrillos', 
        'Cruce Lo Errázuriz', 
        'Plaza Cerrillos'
    ],
    'espera_actual': [12, 8, 20, 15]
}

data_cerrillos = pd.DataFrame(data_dict)


st.subheader("Tiempos de espera actuales")
cols = st.columns(len(data_cerrillos)) 

for i, row in data_cerrillos.iterrows():
    with cols[i]:
        estado = "normal" if row['espera_actual'] < 15 else "critico"
        st.metric(label=row['nombre'], value=f"{row['espera_actual']} min", delta=estado, delta_color="inverse")

        
st.divider()

st.subheader("Mapa de puntos críticos")

m = folium.Map(location=[-33.5, -70.72], zoom_start=14, titles="cartodbpositron")

for i, row in data_cerrillos.iterrows():
    folium.CircleMarker(
        location = [row['lat'], row['lon']],
        radius = 10,
        popup = f"{row['nombre']}: {row['espera_actual']} min de espera",
        color = 'red' if row['espera_actual'] >= 15 else 'orange',
        fill = True,
        fill_opacity = 0.7
).add_to(m)
    
st_folium(m, width="100%", height=500)

st.info("💡 **Próxima actualización:** Integración de algoritmo de despacho dinámico y conexión con API de transporte público.")
