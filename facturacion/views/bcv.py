import requests
from bs4 import BeautifulSoup

def obtener_dolar_bcv():
    url = "https://www.bcv.org.ve/"
    print(f"Obteniendo la tasa oficial del dólar desde {url}...")
    # Encabezado para simular una petición desde un navegador web
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        # Desactivamos la verificación SSL (verify=False) solo si el sitio del BCV presenta problemas de certificados
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()

        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.content, "html.parser")

        # Localizar la etiqueta HTML contenedora del precio del dólar
        div_dolar = soup.find("div", id="dolar")
        
        if div_dolar:
            tasa = div_dolar.find("strong").text.strip()
            # Limpiar y convertir el valor formateado (ejemplo: "36,45" -> 36.45)
            tasa_float = float(tasa.replace(',', '.'))
            return tasa_float
        else:
            print("No se encontró el elemento contenedor del dólar.")
            return None

    except Exception as e:
        print(f"Error al obtener la tasa: {e}")
        return None