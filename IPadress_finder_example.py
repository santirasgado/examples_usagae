pip install streamlit folium requests

import streamlit as st
import folium
import requests
import os

def main():
    st.title("Mapa de Ubicación de IPs")

    # Ejemplo de direcciones IP para mostrar cómo ingresarlas
    example_ips = '189.241.203.74, 3.80.247.134'
    ip_addresses = st.text_area("Ingresa las direcciones IP, separadas por comas", example_ips)
    ips = [ip.strip() for ip in ip_addresses.split(',') if ip.strip()]

    # Usa una variable de entorno para la clave API
    api_key = os.getenv('IPINFO_API_KEY')

    # Crea un mapa base
    mapa = folium.Map(location=[0, 0], zoom_start=2)

    for ip in ips:
        try:
            response = requests.get(f'https://ipinfo.io/{ip}/json?token={api_key}')
            if response.status_code == 200:
                data = response.json()
                if 'loc' in data:
                    lat, lon = map(float, data['loc'].split(','))
                    folium.Marker([lat, lon], popup=f'{ip} - {data.get("city", "N/A")}, {data.get("country", "N/A")}').add_to(mapa)
                else:
                    st.error(f'No se pudo obtener la ubicación para {ip}')
        except Exception as e:
            st.error(f'Error al procesar la IP {ip}: {e}')

    # Renderizar el mapa en la aplicación Streamlit
    st_folium(mapa, width=725, height=500)

# Función para mostrar el mapa en Streamlit
def st_folium(m, width=700, height=500):
    m.save('map.html')
    return st.components.v1.html(open('map.html', 'r').read(), width=width, height=height)

if __name__ == "__main__":
    main()
