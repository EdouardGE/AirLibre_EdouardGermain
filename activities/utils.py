# activities/utils.py
import urllib.request
import json

# ================================
# Récupère la qualité de l'air (AQI) pour une ville donnée
# API publique de World Air Quality Index (WAQI).
# Retourne un message formaté avec l'indice AQI si disponible
# ================================
#get_air_quality
def get_air_quality(city):
    token = "14664cff7e0e8109b0620e1e89fdfcaef1b3e44c"
    url = f"https://api.waqi.info/feed/{city}/?token={token}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            if data.get("status") == "ok":
                aqi = data["data"]["aqi"]
                return f"Indice AQI pour {city} : {aqi}"
            else:
                return "Qualité de l'air non disponible"
    except Exception:
        return "Qualité de l'air non disponible"