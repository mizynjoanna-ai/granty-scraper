import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pl-PL,pl;q=0.9'
}

# --- 1. JEDYNY DYNAMICZNY PORTAL (NGO.PL) ---
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
                        "amount": "Dotacje krajowe", "deadline": "Sprawdź na NGO.pl", "category": "Krajowe NGO",
                        "url": link_url
                    })
                    g_id += 1
    except Exception as e: print(f"NGO.pl błąd: {e}")
    return wyniki, g_id

# --- 2. PORTALE AGREGUJĄCE I REGIONALNE (STABILNE STRONY ZAKŁADEK / STRONY GŁÓWNE) ---
def generuj_baze_wyszukiwania(g_id):
    portale = [
        # Krajowe i agregatory
        {"nazwa": "Grantowo.pl", "kat": "Fundusze UE", "tytul": "Wsparcie cyfryzacji i innowacji w przedsiębiorstwach i NGO", "url": "https://grantowo.pl"},
        {"nazwa": "Grantona.pl", "kat": "Dla JST", "tytul": "Rozwój infrastruktury lokalnej i granty modernizacyjne", "url": "https://grantona.pl"},
        {"nazwa": "GrantMatcher.pl", "kat": "AI Matching", "tytul": "Automatyczne dopasowanie funduszy norweskich - Nabór 2026", "url": "https://grantmatcher.pl"},
        {"nazwa": "Grancik.pl", "kat": "Inicjatywy", "tytul": "Mikrogranty na aktywizację społeczności w małych miastach", "url": "https://grancik.pl"},
        {"nazwa": "Grantbot.pl", "kat": "Edukacja", "tytul": "Program operacyjny Wiedza Edukacja Rozwój - wnioski", "url": "https://grantbot.pl"},
        {"nazwa": "Witkac.pl", "kat": "Samorządy", "tytul": "Konkurs na realizację zadań publicznych w sferze kultury i sportu", "url": "https://www.witkac.pl/public/#/konkursy"},
        {"nazwa": "Ekonomiaspoleczna.gov.pl", "kat": "Gov.pl", "tytul": "Dofinansowanie działalności podmiotów ekonomii solidarnej", "url": "https://www.ekonomiaspoleczna.gov.pl"},
        
        # Lokalne i Regionalne (Przekierowania na oficjalne działy NGO/Nabory)
        {"nazwa": "Dolnośląskie Małe Granty", "kat": "Mikrogranty", "tytul": "Dolnośląskie Małe Granty - Mikrodotacje na projekty lokalne", "url": "https://www.dolnoslaskiemalegranty.pl"},
        {"nazwa": "LGD Partnerstwo Ducha Gór", "kat": "Rozwój Lokalny", "tytul": "Wsparcie rozwoju lokalnego w ramach strategii LGD - Karkonosze", "url": "https://www.duchagor.pl/pl/artykuly/nabory-wnioskow-i-konkursy"},
        {"nazwa": "FE dla Dolnego Śląska", "kat": "Fundusze UE", "tytul": "Fundusze Europejskie dla Dolnego Śląska 2021–2027 - EFS+", "url": "https://www.funduszeuedolnyslask.pl/nabory"},
        {"nazwa": "UMWD Wrocław", "kat": "Wojewódzkie", "tytul": "Otwarty konkurs ofert na realizację zadań publicznych Województwa", "url": "https://umwd.dolnyslask.pl/organizacje-pozarzadowe/otwarte-konkursy-ofert/"},
        {"nazwa": "DFOP", "kat": "Wsparcie NGO", "tytul": "Dolnośląski Festiwal i Granty DFOP - Wzmocnienie potencjału NGO", "url": "https://dfop.org.pl"},
        {"nazwa": "UM Jelenia Góra", "kat": "Lokalne JST", "tytul": "Miejski program współpracy z NGO - Dotacje celowe Jeleniej Góry", "url": "https://bip.jeleniagora.pl/menu/216/wspolpraca-z-ngo"},
        {"nazwa": "Powiat Karkonoski", "kat": "Powiatowe", "tytul": "Konkursy dotacyjne Powiatu Karkonoskiego na zadania publiczne", "url": "https://powiatkarkonoski.pl/organizacje-pozarzadowe"}
    ]
    
    wyniki = []
    for p in portale:
        wyniki.append({
            "id": g_id, 
            "title": p["tytul"], 
            "organization": p["nazwa"],
            "amount": "Zgodnie z ogłoszeniem", 
            "deadline": "Bieżący rok", 
            "category": p["kat"],
            "url": p["url"]
        })
        g_id += 1
    return wyniki, g_id

# --- 3. PROCES SCALANIA ---
print("🚀 Generowanie stabilnej bazy z bezpośrednimi linkami...")
wszystkie_granty = []
aktualne_id = 1

# Pobieramy dynamiczne wpisy z NGO.pl
dane_ngo, aktualne_id = pobierz_ngo(aktualne_id)
wszystkie_granty.extend(dane_ngo)

# Pobieramy stabilne, przejrzyste linki regionalne
dane_reszta, aktualne_id = generuj_baze_wyszukiwania(aktualne_id)
wszystkie_granty.extend(dane_reszta)

with open('granty.json', 'w', encoding='utf-8') as f:
    json.dump(wszystkie_granty, f, ensure_ascii=False, indent=4)

print(f"✅ Gotowe! Zapisano {len(wszystkie_granty)} stabilnych pozycji.")
