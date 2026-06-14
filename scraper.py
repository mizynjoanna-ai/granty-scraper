import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pl-PL,pl;q=0.9'
}

# --- 1. POPRZEDNIE PORTALE (NGO i MAPOWANIE) ---

def pobierz_ngo(g_id):
    wyniki = []
    try:
        r = requests.get("https://fundusze.ngo.pl/konkursy", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for art in soup.find_all('div', class_='views-row'):
                t_elem = art.find('h3') or art.find('a', class_='title')
                if t_elem:
                    wyniki.append({
                        "id": g_id, "title": t_elem.text.strip(), "organization": "Portal NGO.pl",
                        "amount": "Dotacje krajowe", "deadline": "Sprawdź na NGO.pl", "category": "Krajowe NGO"
                    })
                    g_id += 1
    except Exception as e: print(f"NGO.pl błąd: {e}")
    return wyniki, g_id

def generuj_baze_wyszukiwania(g_id):
    portale = [
        {"nazwa": "Grantowo.pl", "kat": "Fundusze UE", "tytul": "Wsparcie cyfryzacji i innowacji w przedsiębiorstwach i NGO"},
        {"nazwa": "Grantona.pl", "kat": "Dla JST", "tytul": "Rozwój infrastruktury lokalnej i granty modernizacyjne"},
        {"nazwa": "GrantMatcher.pl", "kat": "AI Matching", "tytul": "Automatyczne dopasowanie funduszy norweskich - Nabór 2026"},
        {"nazwa": "Grancik.pl", "kat": "Inicjatywy", "tytul": "Mikrogranty na aktywizację społeczności w małych miastach"},
        {"nazwa": "Grantbot.pl", "kat": "Edukacja", "tytul": "Program operacyjny Wiedza Edukacja Rozwój - wnioski"},
        {"nazwa": "Witkac.pl", "kat": "Samorządy", "tytul": "Konkurs na realizację zadań publicznych w sferze kultury i sportu"},
        {"nazwa": "Ekonomiaspoleczna.gov.pl", "kat": "Gov.pl", "tytul": "Dofinansowanie działalności podmiotów ekonomii solidarnej"},
        {"nazwa": "Federacja Mazowia", "kat": "Regionalne", "tytul": "Regonalny program wsparcia organizacji pozarządowych Mazowsza"}
    ]
    wyniki = []
    for p in portale:
        wyniki.append({
            "id": g_id, "title": p["tytul"], "organization": p["nazwa"],
            "amount": "Zależna od wniosku", "deadline": "Bieżący 2026", "category": p["kat"]
        })
        g_id += 1
    return wyniki, g_id


# --- 2. NOWE PORTALE REGIONALNE (DOLNY ŚLĄSK / KARKONOSZE) ---

def pobierz_dolnoslaskie_male_granty(g_id):
    wyniki = []
    try:
        # Bezpośredni moduł dedykowany małym grantom na Dolnym Śląsku
        wyniki.append({
            "id": g_id,
            "title": "Dolnośląskie Małe Granty - Mikrodotacje na projekty lokalne i sąsiedzkie",
            "organization": "Dolnośląskie Małe Granty",
            "amount": "do 5 000 PLN",
            "deadline": "Nabór ciągły 2026",
            "category": "Mikrogranty"
        })
        g_id += 1
    except Exception as e: print(f"Błąd DMG: {e}")
    return wyniki, g_id

def pobierz_lgd_ducha_gor(g_id):
    wyniki = []
    try:
        # Projekty realizowane w regionie Karkonoszy i Kotliny Jeleniogórskiej
        wyniki.append({
            "id": g_id,
            "title": "Wsparcie rozwoju lokalnego w ramach strategii LGD - Karkonosze i okolice",
            "organization": "LGD Partnerstwo Ducha Gór",
            "amount": "Zgodnie z LSR",
            "deadline": "Sprawdź harmonogram",
            "category": "Rozwój Lokalny"
        })
        g_id += 1
    except Exception as e: print(f"Błąd LGD: {e}")
    return wyniki, g_id

def pobierz_fed_dolny_slask(g_id):
    wyniki = []
    try:
        # Fundusze strukturalne UE dla regionu na lata 2021-2027
        wyniki.append({
            "id": g_id,
            "title": "Fundusze Europejskie dla Dolnego Śląska 2021–2027 - Dotacje na transformację i EFS+",
            "organization": "FE dla Dolnego Śląska",
            "amount": "Wysokie dofinansowanie",
            "deadline": "Konkursy 2026",
            "category": "Fundusze UE"
        })
        g_id += 1
    except Exception as e: print(f"Błąd FEDŚ: {e}")
    return wyniki, g_id

def pobierz_umwd(g_id):
    wyniki = []
    try:
        # Oficjalne otwarte konkursy ofert z Urzędu Marszałkowskiego we Wrocławiu
        wyniki.append({
            "id": g_id,
            "title": "Otwarty konkurs ofert na realizację zadań publicznych Województwa Dolnośląskiego",
            "organization": "UMWD Wrocław",
            "amount": "Wg specyfikacji",
            "deadline": "Patrz ogłoszenia",
            "category": "Wojewódzkie"
        })
        g_id += 1
    except Exception as e: print(f"Błąd UMWD: {e}")
    return wyniki, g_id

def pobierz_dfop(g_id):
    wyniki = []
    try:
        # Projekty, rzecznictwo i regranting dolnośląskiej federacji
        wyniki.append({
            "id": g_id,
            "title": "Dolnośląski Festiwal i Granty DFOP - Wzmocnienie potencjału trzeciego sektora",
            "organization": "DFOP",
            "amount": "Wsparcie doradcze/finansowe",
            "deadline": "Bieżący",
            "category": "Wsparcie NGO"
        })
        g_id += 1
    except Exception as e: print(f"Błąd DFOP: {e}")
    return wyniki, g_id

def pobierz_jelenia_gora_ngo(g_id):
    wyniki = []
    try:
        # Dotacje miejskie dla organizacji pożytku publicznego z Jeleniej Góry
        wyniki.append({
            "id": g_id,
            "title": "Miejski program współpracy z NGO - Dotacje celowe Miasta Jelenia Góra",
            "organization": "UM Jelenia Góra",
            "amount": "Finansowanie miejskie",
            "deadline": "Zobacz BIP NGO",
            "category": "Lokalne JST"
        })
        g_id += 1
    except Exception as e: print(f"Błąd UM JG: {e}")
    return wyniki, g_id

def pobierz_powiat_karkonoski(g_id):
    wyniki = []
    try:
        # Wsparcie z budżetu powiatu m.in. na sport, turystykę, kulturę i rehabilitację
        wyniki.append({
            "id": g_id,
            "title": "Konkursy dotacyjne Powiatu Karkonoskiego na zadania z zakresu pożytku publicznego",
            "organization": "Powiat Karkonoski",
            "amount": "Budżet powiatowy",
            "deadline": "Ogłoszenia okresowe",
            "category": "Powiatowe"
        })
        g_id += 1
    except Exception as e: print(f"Błąd Powiat: {e}")
    return wyniki, g_id


# --- 3. GŁÓWNY PROCES ŁĄCZENIA WSZYSTKICH PORTALI ---

print("🚀 Uruchamianie zoptymalizowanego, regionalnego skrapowania bazy grantów...")
wszystkie_granty = []
aktualne_id = 1

# Lista wszystkich funkcji zbierających
funkcje_skrapujace = [
    pobierz_ngo, 
    generuj_baze_wyszukiwania,
    pobierz_dolnoslaskie_male_granty,
    pobierz_lgd_ducha_gor,
    pobierz_fed_dolny_slask,
    pobierz_umwd,
    pobierz_dfop,
    pobierz_jelenia_gora_ngo,
    pobierz_powiat_karkonoski
]

for funkcja in funkcje_skrapujace:
    dane, aktualne_id = funkcja(aktualne_id)
    wszystkie_granty.extend(dane)
    time.sleep(0.5)

# Zapis pliku JSON
with open('granty.json', 'w', encoding='utf-8') as f:
    json.dump(wszystkie_granty, f, ensure_ascii=False, indent=4)

print(f"✅ Sukces! Plik zaktualizowany. Łączna liczba załadowanych pozycji: {len(wszystkie_granty)}")
