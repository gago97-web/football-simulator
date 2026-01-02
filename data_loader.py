
import requests
import certifi
import pandas as pd


API_KEY = "ab621f97f61d67da3a2f0264f1cdfc37"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": API_KEY
}
LEAGUE_ID = 135  # Serie A
SEASON = 2025  # Cambiato da 2025 a 2024

def carica_classifica():
    """Carica la classifica attuale dalla API"""
    url = f"{BASE_URL}/standings"
    params = {
        "league": LEAGUE_ID,
        "season": SEASON
    }
    
    try:
        print(f"📡 Chiamata API: {url}")
        print(f"   Parametri: {params}")
        
        r = requests.get(
            url, 
            headers=HEADERS, 
            params=params,
            verify=certifi.where(),
            timeout=10
        )
        
        print(f"✅ Status Code: {r.status_code}")
        data = r.json()
        
        # Stampa la risposta completa per debug
        print(f"📦 Risposta API: {data}")
        
        # Verifica se ci sono errori nell'API
        if "errors" in data and data["errors"]:
            error_msg = data['errors']
            print(f"❌ Errore API: {error_msg}")
            raise Exception(f"API Error: {error_msg}")
        
        # Verifica se la risposta contiene dati
        if not data.get("response") or len(data["response"]) == 0:
            print(f"⚠️ Risposta API vuota o nessun dato disponibile")
            print(f"   Response completa: {data}")
            raise Exception("Nessun dato disponibile dall'API. Possibili cause: API key non valida, limite chiamate raggiunto, o stagione non disponibile.")
        
        standings = data["response"][0]["league"]["standings"][0]
        
        table = []
        for t in standings:
            table.append({
                "nome": t["team"]["name"],
                "punti": t["points"],
                "partite": t["all"]["played"],
                "golFatti": t["all"]["goals"]["for"],
                "golSubiti": t["all"]["goals"]["against"]
            })
        
        print(f"✅ Caricate {len(table)} squadre dalla classifica")
        return table
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di connessione: {e}")
        raise Exception(f"Errore di connessione all'API: {e}")
    except KeyError as e:
        print(f"❌ Errore nella struttura dei dati: {e}")
        print(f"   Dati ricevuti: {data if 'data' in locals() else 'Nessun dato'}")
        raise Exception(f"Formato dati API non valido: {e}")
    except Exception as e:
        print(f"❌ Errore generico: {e}")
        raise


def carica_calendario_rimanente():
    """Carica le partite rimanenti dalla API"""
    url = f"{BASE_URL}/fixtures"
    params = {
        "league": LEAGUE_ID,
        "season": SEASON,
        "status": "NS"  # Not Started
    }
    
    try:
        r = requests.get(
            url, 
            headers=HEADERS, 
            params=params,
            verify=certifi.where(),
            timeout=10
        )
        
        data = r.json()
        
        # Verifica errori
        if "errors" in data and data["errors"]:
            print(f"Errore API calendario: {data['errors']}")
            raise Exception(f"API Error: {data['errors']}")
        
        if not data.get("response"):
            print("Nessuna partita futura trovata")
            return {}
        
        calendario = {}
        for f in data["response"]:
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            
            # Aggiungi l'avversario per la squadra di casa
            if home not in calendario:
                calendario[home] = []
            calendario[home].append(away)
            
            # Aggiungi l'avversario per la squadra ospite
            if away not in calendario:
                calendario[away] = []
            calendario[away].append(home)
        
        return calendario
        
    except requests.exceptions.RequestException as e:
        print(f"Errore di connessione calendario: {e}")
        raise Exception(f"Errore di connessione all'API: {e}")
    except Exception as e:
        print(f"Errore generico calendario: {e}")
        raise


# Dati di fallback statici (usati se l'API fallisce)
CLASSIFICA_FALLBACK = [
    {"nome": "Inter", "punti": 36, "partite": 16, "vinte":12 , "pareggi":0 , "golFatti": 35, "golSubiti": 14},
    {"nome": "Milan", "punti": 35, "partite": 16,"vinte":10 , "pareggi":5 , "golFatti": 27, "golSubiti": 13},
    {"nome": "Napoli", "punti": 34, "partite": 16,"vinte":11 , "pareggi":1 , "golFatti": 24, "golSubiti": 13},
    {"nome": "Roma", "punti": 33, "partite": 17,"vinte":11 , "pareggi":0 , "golFatti": 20, "golSubiti": 11},
    {"nome": "Juventus", "punti": 32, "partite": 17,"vinte":9 , "pareggi":5 , "golFatti": 23, "golSubiti": 15},
    {"nome": "Como", "punti": 27, "partite": 16,"vinte":7 , "pareggi":6 , "golFatti": 22, "golSubiti": 12},
    {"nome": "Bologna", "punti": 26, "partite": 16,"vinte":7 , "pareggi":5 , "golFatti": 24, "golSubiti": 14},
    {"nome": "Lazio", "punti": 24, "partite": 17,"vinte":6 , "pareggi":6 , "golFatti": 18, "golSubiti": 12},
    {"nome": "Sassuolo", "punti": 22, "partite": 17,"vinte":6 , "pareggi":4 , "golFatti": 22, "golSubiti": 21},
    {"nome": "Atalanta", "punti": 22, "partite": 17,"vinte":5 , "pareggi":7 , "golFatti": 20, "golSubiti": 19},
    {"nome": "Udinese", "punti": 22, "partite": 17,"vinte":6 , "pareggi":4 , "golFatti": 18, "golSubiti": 28},
    {"nome": "Cremonese", "punti": 21, "partite": 17,"vinte":5 , "pareggi":6 , "golFatti": 17, "golSubiti": 20},
    {"nome": "Torino", "punti": 20, "partite": 17,"vinte":5 , "pareggi":5 , "golFatti": 17, "golSubiti": 28},
    {"nome": "Cagliari", "punti": 18, "partite": 17,"vinte":4 , "pareggi":6 , "golFatti": 19, "golSubiti": 24},
    {"nome": "Parma", "punti": 17, "partite": 16,"vinte":4 , "pareggi":5 , "golFatti": 11, "golSubiti": 18},
    {"nome": "Lecce", "punti": 16, "partite": 16,"vinte":4 , "pareggi":4 , "golFatti": 11, "golSubiti": 22},
    {"nome": "Genoa", "punti": 14, "partite": 16,"vinte":3 , "pareggi":5 , "golFatti": 16, "golSubiti": 24},
    {"nome": "Verona", "punti": 12, "partite": 16,"vinte":2 , "pareggi":6 , "golFatti": 13, "golSubiti": 25},
    {"nome": "Pisa", "punti": 11, "partite": 17,"vinte":1 , "pareggi":8 , "golFatti": 12, "golSubiti": 24},
    {"nome": "Fiorentina", "punti": 9, "partite": 17,"vinte":1 , "pareggi":6 , "golFatti": 17, "golSubiti": 28}
]



from collections import defaultdict

# Carica il CSV
calendario = pd.read_csv("C:/Users/ggrassi004/Downloads/seriea_simulator/calendario.csv", sep=";")
calendario=calendario.loc[166:]

# Dizionario: squadra -> lista di match ordinati
# Ogni match è un dict: {"vs": avversario, "home": True/False}
CALENDARIO_FALLBACK = defaultdict(list)

for _, row in calendario.iterrows():
    casa = row["Squadra_casa"].strip()
    ospite = row["Squadra_ospite"].strip()
    
    # Aggiunge la partita al calendario della squadra di casa
    CALENDARIO_FALLBACK[casa].append({"vs": ospite, "home": True})
    
    # Aggiunge la partita al calendario della squadra ospite
    CALENDARIO_FALLBACK[ospite].append({"vs": casa, "home": False})

# Converti in dict normale
CALENDARIO_FALLBACK = dict(CALENDARIO_FALLBACK)



