"""Client minimo per il server locale di LM Studio.

Scheletro da completare con Claude Code (slide 19-22):
configurazione, messaggi, payload e chiamata HTTP.
Import e gestione degli errori sono gia' presenti: conservarli.
"""

import os

import requests
from dotenv import load_dotenv

# --- Configurazione -------------------------------------------------------
load_dotenv()
base_url = os.environ["LM_BASE_URL"]
model = os.environ["LM_MODEL"]

# --- Messaggi -------------------------------------------------------------
SYSTEM = "Sei un assistente per studenti. Rispondi in italiano, in modo chiaro e conciso."

# --- Ciclo di domande -----------------------------------------------------
while True:
    try:
        domanda = input("Tu> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        break
    if domanda.lower() == "esci":
        break
    if not domanda:
        continue

    # --- Payload ----------------------------------------------------------
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": domanda},
        ],
        "temperature": 0.2,
        "max_tokens": 300,
        "reasoning_effort": "none",
        "stream": False,
    }

    # --- Chiamata ---------------------------------------------------------
    try:
        response = requests.post(f"{base_url}/chat/completions", json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            print("Errore dal server:", data["error"])
        else:
            print(data["choices"][0]["message"]["content"])
    except requests.exceptions.Timeout:
        print("Attesa scaduta: controllare server, carico e tempi.")
    except requests.exceptions.ConnectionError:
        print("Connessione fallita: controllare server, URL e porta.")
    except requests.exceptions.HTTPError:
        print("Errore HTTP:", response.status_code, response.text)
