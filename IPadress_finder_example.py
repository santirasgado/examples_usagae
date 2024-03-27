import streamlit as st
import folium
import requests
import os

def fetch_location(ip, api_key):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json?token={api_key}')
        if response.status_code == 200:
            data = response.json()
            location = data.get('loc', None)
            if location:
                lat, lon = [float(coord) for coord in location.split(',')]
                return lat, lon, data.get('city', 'Unknown city'), data.get('country', 'Unknown country')
    except Exception as e:
        st.error(f'Error al procesar la IP {ip}: {e}')
    return None, None, None, None

def main():
    st.title("Mapa de Ubicación de IPs")

    # Solicita al usuario que ingrese direcciones IP
    ip_addresses = st.text_area("Ingresa las direcciones IP, separadas por comas")
    ips = [ip.strip() for ip in ip_addresses.split(',') if ip.strip()]

    api_key = os.getenv('51d0481f274cac')  # Asegúrate de tener esta variable de entorno configurada

    # Crea un mapa base
    mapa = folium.Map(location=[20, 0], zoom_start=2)

    for ip in ips:
        lat, lon, city, country = fetch_location(ip, api_key)
        if lat and lon:
            folium.Marker([lat, lon], popup=f'{ip} - {city}, {country}').add_to(mapa)

    # Renderizar el mapa en la aplicación Streamlit
    st_data = st_folium(mapa)

def st_folium(m, width=700, height=500):
    """Función para mostrar el mapa en Streamlit"""
    m.save('map.html')
    return st.components.v1.html(open('map.html', 'r').read(), width=width, height=height)

if __name__ == "__main__":
    main()
