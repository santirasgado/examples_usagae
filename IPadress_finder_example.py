import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

def main():
    st.title("Mapa de Ubicación de IPs")

    # Aquí puedes agregar la funcionalidad para ingresar direcciones IP
    ips = ['189.241.203.74', '3.80.247.134', '187.208.97.53', '189.216.43.254',  '73.179.155.130', '216.163.246.128', '187.188.8.161', '89.163.216.65', '181.13.214.90', '89.163.216.65', '89.163.216.65']

    api_key = 'tu_clave_de_api'
    mapa = folium.Map(location=[20, 0], zoom_start=2)

    for ip in ips:
        response = requests.get(f'https://ipinfo.io/{ip}/json?token={api_key}')
        if response.status_code == 200:
            data = response.json()
            location = data['loc'].split(',')
            folium.Marker([float(location[0]), float(location[1])], popup=ip).add_to(mapa)
        else:
            st.error(f'Error al obtener la ubicación para {ip}: {response.status_code}')

    st_data = st_folium(mapa, width=700, height=500)

if __name__ == "__main__":
    main()
