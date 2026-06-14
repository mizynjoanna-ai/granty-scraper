import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
}

# --- BLOKI SKRAPERÓW DLA POSZCZEGÓLNYCH PORTALI ---

def pobierz_ngo(g_id):
    wyniki = []
    try:
        r = requests.get("https://fundusze.ngo.pl/konkursy", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for art in soup.find_all('div', class_='views-row'):
                t_elem = art.find('h3') or art.find('a', class_='title')
                if t_elem:
                    wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "Portal NGO.pl", "amount": "Do ustalenia", "deadline": "Sprawdź na stronie", "category": "Krajowe NGO"})
                    g_id += 1
    except Exception as e: print(f"⚠️ NGO.pl błąd: {e}")
    return wyniki, g_id

def pobierz_grantowo(g_id):
    wyniki = []
    try:
        r = requests.get("https://grantowo.pl/konkursy", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Dopasowane do standardowej struktury WordPress/pętli wpisów
            for art in soup.find_all(['article', 'div'], class_=['post', 'grant-item', 'entry-card']):
                t_elem = art.find(['h2', 'h3', 'h4'])
                if t_elem:
                    wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "Grantowo.pl", "amount": "Unijne / Krajowe", "deadline": "Bieżący", "category": "Agregator"})
                    g_id += 1
    except Exception as e: print(f"⚠️ Grantowo błąd: {e}")
    return wyniki, g_id

def pobierz_grantona(g_id):
    wyniki = []
    try:
        r = requests.get("https://grantona.pl", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for item in soup.find_all(['div', 'article'], class_=['grant', 'offer', 'card']):
                t_elem = item.find(['h3', 'a'])
                if t_elem:
                    wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "Grantona.pl", "amount": "Zróżnicowana", "deadline": "Wkrótce", "category": "Dla JST i NGO"})
                    g_id += 1
    except Exception as e: print(f"⚠️ Grantona błąd: {e}")
    return wyniki, g_id

def pobierz_grantmatcher(g_id):
    wyniki = []
    try:
        r = requests.get("https://grantmatcher.pl", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for card in soup.find_all('div', class_=['card', 'grant-row']):
                t_elem = card.find('h3')
                if t_elem:
                    wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "GrantMatcher AI", "amount": "Dopasowanie AI", "deadline": "Ciągły", "category": "Fundusze AI"})
                    g_id += 1
    except Exception as e: print(f"⚠️ GrantMatcher błąd: {e}")
    return wyniki, g_id

def pobierz_grancik(g_id):
    wyniki = []
    try:
        r = requests.get("https://grancik.pl", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for item in soup.find_all(['div', 'li']):
                if 'grant' in item.get('class', []) or 'konkurs' in item.get('class', []):
                    t_elem = item.find('h3') or item.find('a')
                    if t_elem and len(t_elem.text.strip()) > 10:
                        wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "Grancik.pl", "amount": "Asystent NGO", "deadline": "Zobacz portal", "category": "Wyszukiwarka"})
                        g_id += 1
    except Exception as e: print(f"⚠️ Grancik błąd: {e}")
    return wyniki, g_id

def pobierz_grantbot(g_id):
    wyniki = []
    try:
        r = requests.get("https://grantbot.pl", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for program in soup.find_all(['div', 'section'], class_=['program', 'item', 'list']):
                t_elem = program.find(['h3', 'h4'])
                if t_elem:
                    wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "Grantbot.pl", "amount": "Dotacje celowe", "deadline": "Harmonogram", "category": "Programy"})
                    g_id += 1
    except Exception as e: print(f"⚠️ Grantbot błąd: {e}")
    return wyniki, g_id

def pobierz_witkac(g_id):
    wyniki = []
    try:
        r = requests.get("https://www.witkac.pl/public/konkursy", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for row in soup.find_all(['div', 'tr'], class_=['contest', 'row', 'item']):
                t_elem = row.find(['a', 'h4', 'span'], class_=['title', 'name'])
                if t_elem:
                    wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "Witkac.pl", "amount": "Samorządowe (JST)", "deadline": "Wg ogłoszenia", "category": "Zlecenia Publiczne"})
                    g_id += 1
    except Exception as e: print(f"⚠️ Witkac błąd: {e}")
    return wyniki, g_id

def pobierz_ekonomia_spoleczna(g_id):
    wyniki = []
    try:
        r = requests.get("https://www.ekonomiaspoleczna.gov.pl", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for news in soup.find_all(['div', 'li'], class_=['news', 'wyszukiwarka-item', 'art']):
                t_elem = news.find(['h3', 'h4', 'a'])
                if t_elem and "grant" in t_elem.text.lower() or "konkurs" in t_elem.text.lower():
                    wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "Ministerstwo (gov.pl)", "amount": "Państwowe", "deadline": "Określony", "category": "Ekonomia Społeczna"})
                    g_id += 1
    except Exception as e: print(f"⚠️ Gov.pl błąd: {e}")
    return wyniki, g_id

def pobierz_mazowia(g_id):
    wyniki = []
    try:
        r = requests.get("https://mazowia.pl.pl/konkursy", headers=HEADERS, timeout=15) # Zabezpieczony link federacji
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for post in soup.find_all(['div', 'article']):
                t_elem = post.find(['h2', 'h3', 'a'])
                if t_elem and ("konkurs" in t_elem.text.lower() or "grant" in t_elem.text.lower()):
                    wyniki.append({"id": g_id, "title": t_elem.text.strip(), "organization": "Federacja Mazowia", "amount": "Regionalne", "deadline": "Sprawdź", "category": "Konkursy"})
                    g_id += 1
    except Exception as e: print(f"⚠️ Mazowia błąd: {e}")
    return wyniki, g_id


# --- GŁÓWNY PROCES ŁĄCZENIA DANYCH ---

print("🚀 Rozpoczynamy wieloportaliwowe skrapowanie bazy grantów...")
aktualne_id = 1
wszystkie_granty = []

# Bezpieczne wywoływanie kolejnych modułów
for funkcja_pobierająca in [
    pobierz_ngo, pobierz_grantowo, pobierz_grantona, 
    pobierz_grantmatcher, pobierz_grancik, pobierz_grantbot, 
    pobierz_witkac, pobierz_ekonomia_spoleczna, pobierz_mazowia
]:
    dane, aktualne_id = funkcja_pobierająca(aktualne_id)
    wszystkie_granty.extend(dane)
    time.sleep(1) # Chwila odpoczynku dla serwerów, by nas nie zablokowały

# Awaryjna baza startowa, gdyby wszystkie portale na raz były niedostępne
if not wszystkie_granty:
    wszystkie_granty = [{
        "id": 1,
        "title": "Brak aktywnych połączeń. Sprawdź panele portali agregujących.",
        "organization": "System Automatyczny",
        "amount": "- PLN",
        "deadline": "31.12.2026",
        "category": "Status"
    }]

# Zapis do końcowego pliku JSON
with open('granty.json', 'w', encoding='utf-8') as f:
    json.dump(wszystkie_granty, f, ensure_ascii=False, indent=4)

print(f"✅ Sukces! Zebrano łącznie {len(wszystkie_granty)} rekordów z działających portali i zaktualizowano plik granty.json!")
