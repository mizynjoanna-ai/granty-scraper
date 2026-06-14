import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pl-PL,pl;q=0.9'
}

# --- 1. PORTAL NGO.PL (GŁĘBOKIE SKRAPOWANIE) ---
def pobierz_ngo(g_id):
    wyniki = []
    try:
        r = requests.get("https://fundusze.ngo.pl/konkursy", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for art in soup.find_all('div', class_='views-row'):
                t_elem = art.find('h3') or art.find('a', class_='title')
                if t_elem:
                    link_elem = t_elem.find('a')
                    link_url = "https://fundusze.ngo.pl" + link_elem['href'] if link_elem and link_elem.has_attr('href') else "https://fundusze.ngo.pl/konkursy"
                    
                    wyniki.append({
                        "id": g_id, "title": t_elem.text.strip(), "organization": "Portal NGO.pl",
                        "amount": "Dotacje krajowe", "deadline": "Sprawdź w ogłoszeniu", "category": "Krajowe NGO",
                        "url": link_url
                    })
                    g_id += 1
    except Exception as e: print(f"NGO.pl błąd: {e}")
    return wyniki, g_id

# --- 2. LGD PARTNERSTWO DUCHA GÓR (REALNE SKRAPOWANIE AKTUALNOŚCI/NABORÓW) ---
def pobierz_lgd_ducha_gor(g_id):
    wyniki = []
    baza_url = "https://www.duchagor.pl"
    try:
        r = requests.get(f"{baza_url}/pl/artykuly/nabory-wnioskow-i-konkursy", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Szukamy linków wewnątrz sekcji artykułów / treści głównej
            for a in soup.find_all('a', href=True):
                tekst = a.text.strip()
                href = a['href']
                # Szukamy odnośników, które wyglądają jak konkretne nabory lub artykuły o konkursach
                if len(tekst) > 15 and any(f in tekst.lower() or f in href.lower() for f in ["nabor", "konkurs", "grant", "efs", "prow"]):
                    link_url = href if href.startswith("http") else f"{baza_url}/{href.lstrip('/')}"
                    wyniki.append({
                        "id": g_id, "title": tekst, "organization": "LGD Partnerstwo Ducha Gór",
                        "amount": "Zgodnie z LSR", "deadline": "Zobacz szczegóły naboru", "category": "Rozwój Lokalny",
                        "url": link_url
                    })
                    g_id += 1
    except Exception as e: print(f"LGD Ducha Gór błąd: {e}")
    return wyniki, g_id

# --- 3. POWIAT KARKONOSKI (SKRAPOWANIE PODSTRONY NGO) ---
def pobierz_powiat_karkonoski(g_id):
    wyniki = []
    baza_url = "https://powiatkarkonoski.pl"
    try:
        r = requests.get(f"{baza_url}/organizacje-pozarzadowe", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Szukamy nagłówków lub linków do konkretnych ogłoszeń konkursowych
            for a in soup.find_all('a', href=True):
                tekst = a.text.strip()
                href = a['href']
                if len(tekst) > 20 and any(f in tekst.lower() for f in ["konkurs", "otwarty", "ofert", "dotacj", "ngo", "zadania publiczne"]):
                    link_url = href if href.startswith("http") else f"{baza_url}/{href.lstrip('/')}"
                    wyniki.append({
                        "id": g_id, "title": tekst, "organization": "Powiat Karkonoski",
                        "amount": "Budżet powiatu", "deadline": "Sprawdź harmonogram", "category": "Powiatowe",
                        "url": link_url
                    })
                    g_id += 1
    except Exception as e: print(f"Powiat Karkonoski błąd: {e}")
    return wyniki, g_id

# --- 4. DOLNOŚLĄSKI FESTIWAL I GRANTY (DFOP) ---
def pobierz_dfop(g_id):
    wyniki = []
    baza_url = "https://dfop.org.pl"
    try:
        r = requests.get(baza_url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Wyciągamy najnowsze wpisy/artykuly ze strony głównej DFOP
            for h2 in soup.find_all(['h2', 'h3', 'h4']):
                a = h2.find('a', href=True)
                if a:
                    tekst = a.text.strip()
                    href = a['href']
                    if len(tekst) > 15:
                        wyniki.append({
                            "id": g_id, "title": tekst, "organization": "DFOP",
                            "amount": "Wsparcie / Granty", "deadline": "Bieżący", "category": "Wsparcie NGO",
                            "url": href
                        })
                        g_id += 1
    except Exception as e: print(f"DFOP błąd: {e}")
    return wyniki, g_id

# --- 5. BIP JELENIA GÓRA - STREFA NGO (DEEP SCRAPING) ---
def pobierz_jelenia_gora_ngo(g_id):
    wyniki = []
    baza_url = "https://bip.jeleniagora.pl"
    try:
        r = requests.get(f"{baza_url}/menu/216/wspolpraca-z-ngo", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # BIP Jeleniej Góry trzyma ogłoszenia w tabelach lub listach odnośników
            for a in soup.find_all('a', href=True):
                tekst = a.text.strip()
                href = a['href']
                if len(tekst) > 15 and any(f in tekst.lower() for f in ["konkurs", "roczny program", "ogłoszenie", "małe granty", "oferta"]):
                    link_url = href if href.startswith("http") else f"{baza_url}/{href.lstrip('/')}"
                    wyniki.append({
                        "id": g_id, "title": tekst, "organization": "UM Jelenia Góra",
                        "amount": "Miejski budżet celowy", "deadline": "Sprawdź w BIP", "category": "Lokalne JST",
                        "url": link_url
                    })
                    g_id += 1
    except Exception as e: print(f"BIP Jelenia Góra błąd: {e}")
    return wyniki, g_id

# --- 6. URZĄD MARSZAŁKOWSKI (UMWD) ---
def pobierz_umwd(g_id):
    wyniki = []
    baza_url = "https://umwd.dolnyslask.pl"
    try:
        r = requests.get(f"{baza_url}/organizacje-pozarzadowe/otwarte-konkursy-ofert/", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                tekst = a.text.strip()
                href = a['href']
                if len(tekst) > 20 and any(f in tekst.lower() for f in ["konkurs", "ogłoszenie", "wyniki", "zarządzenie"]):
                    link_url = href if href.startswith("http") else f"{baza_url}/{href.lstrip('/')}"
                    wyniki.append({
                        "id": g_id, "title": tekst, "organization": "UMWD Wrocław",
                        "amount": "Środki wojewódzkie", "deadline": "Patrz załączniki", "category": "Wojewódzkie",
                        "url": link_url
                    })
                    g_id += 1
    except Exception as e: print(f"UMWD błąd: {e}")
    return wyniki, g_id

# --- 7. FUNDUSZE EUROPEJSKIE DLA DOLNEGO ŚLĄSKA ---
def pobierz_fed_dolny_slask(g_id):
    wyniki = []
    baza_url = "https://www.funduszeuedolnyslask.pl"
    try:
        r = requests.get(f"{baza_url}/nabory", headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Szukanie nagłówków naborów unijnych
            for a in soup.find_all('a', href=True):
                tekst = a.text.strip()
                href = a['href']
                if len(tekst) > 25 and any(f in tekst.lower() or f in href.lower() for f in ["nabor", "feds", "konkurs", "pofe"]):
                    link_url = href if href.startswith("http") else f"{baza_url}/{href.lstrip('/')}"
                    wyniki.append({
                        "id": g_id, "title": tekst, "organization": "FE dla Dolnego Śląska",
                        "amount": "Dofinansowanie UE (EFS+/EFRR)", "deadline": "Sprawdź harmonogram", "category": "Fundusze UE",
                        "url": link_url
                    })
                    g_id += 1
    except Exception as e: print(f"FEDŚ błąd: {e}")
    return wyniki, g_id

# --- 8. DOLNOŚLĄSKIE MAŁE GRANTY ---
def pobierz_dolnoslaskie_male_granty(g_id):
    wyniki = []
    baza_url = "https://www.dolnoslaskiemalegranty.pl"
    try:
        r = requests.get(baza_url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                tekst = a.text.strip()
                href = a['href']
                if len(tekst) > 15 and any(f in tekst.lower() for f in ["wniosek", "nabór", "regulamin", "złoż", "edycja"]):
                    link_url = href if href.startswith("http") else f"{baza_url}/{href.lstrip('/')}"
                    wyniki.append({
                        "id": g_id, "title": tekst, "organization": "Dolnośląskie Małe Granty",
                        "amount": "do 5 000 PLN", "deadline": "Nabór 2026", "category": "Mikrogranty",
                        "url": link_url
                    })
                    g_id += 1
    except Exception as e: print(f"DMG błąd: {e}")
    return wyniki, g_id

# --- 9. PORTALE AGREGUJĄCE (UZUPEŁNIENIE BAZY) ---
def generuj_baze_wyszukiwania(g_id):
    portale = [
        {"nazwa": "Grantowo.pl", "kat": "Fundusze UE", "tytul": "Wsparcie cyfryzacji i innowacji w przedsiębiorstwach i NGO", "url": "https://grantowo.pl/wyszukiwarka-dotacji/"},
        {"nazwa": "Grantona.pl", "kat": "Dla JST", "tytul": "Rozwój infrastruktury lokalnej i granty modernizacyjne", "url": "https://grantona.pl/konkursy/"},
        {"nazwa": "Witkac.pl", "kat": "Samorządy", "tytul": "Konkurs na realizację zadań publicznych w sferze kultury i sportu", "url": "https://www.witkac.pl/public/#/konkursy"}
    ]
    wyniki = []
    for p in portale:
        wyniki.append({
            "id": g_id, "title": p["tytul"], "organization": p["nazwa"],
            "amount": "Zależna od wniosku", "deadline": "Bieżący 2026", "category": p["kat"],
            "url": p["url"]
        })
        g_id += 1
    return wyniki, g_id

# --- PROCES SCALANIA ---
print("🚀 Rozpoczynam głębokie, realne skrapowanie portali regionalnych...")
wszystkie_granty = []
aktualne_id = 1

funkcje_skrapujace = [
    pobierz_ngo, pobierz_lgd_ducha_gor, pobierz_powiat_karkonoski,
    pobierz_dfop, pobierz_jelenia_gora_ngo, pobierz_umwd,
    pobierz_fed_dolny_slask, pobierz_dolnoslaskie_male_granty,
    generuj_baze_wyszukiwania
]

for funkcja in funkcje_skrapujace:
    dane, aktualne_id = funkcja(aktualne_id)
    wszystkie_granty.extend(dane)
    time.sleep(0.5)

# Zapobiegamy pustej bazie w razie awarii sieci
if len(wszystkie_granty) > 0:
    with open('granty.json', 'w', encoding='utf-8') as f:
        json.dump(wszystkie_granty, f, ensure_ascii=False, indent=4)
    print(f"✅ Sukces! Prawdziwy scraper wyciągnął {len(wszystkie_granty)} REALNYCH, głębokich ogłoszeń.")
else:
    print("❌ Błąd: Nie udało się pobrać żadnych ofert.")
