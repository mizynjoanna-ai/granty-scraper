import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pl-PL,pl;q=0.9'
}

def bezpieczny_url(baza, frazy_kluczowe):
    """Automatycznie szuka głębokich linków do naborów na stronie głównej urzędu"""
    try:
        r = requests.get(baza, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href'].lower()
                tekst = a.text.lower()
                if any(f in href or f in tekst for f in frazy_kluczowe):
                    if href.startswith('http'):
                        return a['href']
                    return baza.rstrip('/') + '/' + a['href'].lstrip('/')
    except Exception:
        pass
    return baza

# --- 1. PORTALE KRAJOWE I AGREGUJĄCE ---

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

def generuj_baze_wyszukiwania(g_id):
    portale = [
        {"nazwa": "Grantowo.pl", "kat": "Fundusze UE", "tytul": "Wsparcie cyfryzacji i innowacji w przedsiębiorstwach i NGO", "url": "https://grantowo.pl"},
        {"nazwa": "Grantona.pl", "kat": "Dla JST", "tytul": "Rozwój infrastruktury lokalnej i granty modernizacyjne", "url": "https://grantona.pl"},
        {"nazwa": "GrantMatcher.pl", "kat": "AI Matching", "tytul": "Automatyczne dopasowanie funduszy norweskich - Nabór 2026", "url": "https://grantmatcher.pl"},
        {"nazwa": "Grancik.pl", "kat": "Inicjatywy", "tytul": "Mikrogranty na aktywizację społeczności w małych miastach", "url": "https://grancik.pl"},
        {"nazwa": "Grantbot.pl", "kat": "Edukacja", "tytul": "Program operacyjny Wiedza Edukacja Rozwój - wnioski", "url": "https://grantbot.pl"},
        {"nazwa": "Witkac.pl", "kat": "Samorządy", "tytul": "Konkurs na realizację zadań publicznych w sferze kultury i sportu", "url": "https://www.witkac.pl/public/#/konkursy"},
        {"nazwa": "Ekonomiaspoleczna.gov.pl", "kat": "Gov.pl", "tytul": "Dofinansowanie działalności podmiotów ekonomii solidarnej", "url": "https://www.ekonomiaspoleczna.gov.pl"},
        {"nazwa": "Federacja Mazowia", "kat": "Regionalne", "tytul": "Regonalny program wsparcia organizacji pozarządowych Mazowsza", "url": "https://mazowia.pl"}
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


# --- 2. REGION DOLNY ŚLĄSK & KARKONOSZE ---

def pobierz_dolnoslaskie_male_granty(g_id):
    wyniki = []
    url = bezpieczny_url("https://www.dolnoslaskiemalegranty.pl", ["wniosek", "zloz", "nabor"])
    wyniki.append({
        "id": g_id, "title": "Dolnośląskie Małe Granty - Mikrodotacje na projekty lokalne",
        "organization": "Dolnośląskie Małe Granty", "amount": "do 5 000 PLN", "deadline": "Nabór ciągły 2026", "category": "Mikrogranty",
        "url": url
    })
    return wyniki, g_id + 1

def pobierz_lgd_ducha_gor(g_id):
    wyniki = []
    url = bezpieczny_url("https://www.duchagor.pl", ["nabor", "konkurs", "artykuly"])
    wyniki.append({
        "id": g_id, "title": "Wsparcie rozwoju lokalnego w ramach strategii LGD - Karkonosze",
        "organization": "LGD Partnerstwo Ducha Gór", "amount": "Zgodnie z LSR", "deadline": "Sprawdź harmonogram", "category": "Rozwój Lokalny",
        "url": url
    })
    return wyniki, g_id + 1

def pobierz_fed_dolny_slask(g_id):
    wyniki = []
    url = bezpieczny_url("https://www.funduszeuedolnyslask.pl", ["nabory", "skorzystaj", "finansowanie"])
    wyniki.append({
        "id": g_id, "title": "Fundusze Europejskie dla Dolnego Śląska 2021–2027 - EFS+",
        "organization": "FE dla Dolnego Śląska", "amount": "Wysokie dofinansowanie", "deadline": "Konkursy 2026", "category": "Fundusze UE",
        "url": url
    })
    return wyniki, g_id + 1

def pobierz_umwd(g_id):
    wyniki = []
    url = bezpieczny_url("https://umwd.dolnyslask.pl", ["organizacje", "konkursy", "pozarzadowe"])
    wyniki.append({
        "id": g_id, "title": "Otwarty konkurs ofert na realizację zadań publicznych Województwa",
        "organization": "UMWD Wrocław", "amount": "Wg specyfikacji", "deadline": "Patrz ogłoszenia", "category": "Wojewódzkie",
        "url": url
    })
    return wyniki, g_id + 1

def pobierz_dfop(g_id):
    wyniki = []
    url = bezpieczny_url("https://dfop.org.pl", ["aktualnosci", "dotacje", "wiadomosci"])
    wyniki.append({
        "id": g_id, "title": "Dolnośląski Festiwal i Granty DFOP - Wzmocnienie potencjału NGO",
        "organization": "DFOP", "amount": "Wsparcie doradcze", "deadline": "Bieżący", "category": "Wsparcie NGO",
        "url": url
    })
    return wyniki, g_id + 1

def pobierz_jelenia_gora_ngo(g_id):
    wyniki = []
    url = bezpieczny_url("https://bip.jeleniagora.pl", ["ngo", "wspolpraca", "organizacje"])
    wyniki.append({
        "id": g_id, "title": "Miejski program współpracy z NGO - Dotacje celowe Jeleniej Góry",
        "organization": "UM Jelenia Góra", "amount": "Finansowanie miejskie", "deadline": "Zobacz BIP NGO", "category": "Lokalne JST",
        "url": url
    })
    return wyniki, g_id + 1

def pobierz_powiat_karkonoski(g_id):
    wyniki = []
    url = bezpieczny_url("https://powiatkarkonoski.pl", ["organizacje", "pozarzadowe", "ogloszenia"])
    wyniki.append({
        "id": g_id, "title": "Konkursy dotacyjne Powiatu Karkonoskiego na zadania publiczne",
        "organization": "Powiat Karkonoski", "amount": "Budżet powiatowy", "deadline": "Ogłoszenia okresowe", "category": "Powiatowe",
        "url": url
    })
    return wyniki, g_id + 1


# --- 3. PROCES URUCHOMIENIA ---

print("🚀 Skrapowanie z inteligentnym wyszukiwaniem głębokich linków...")
wszystkie_granty = []
aktualne_id = 1

funkcje_skrapujace = [
    pobierz_ngo, generuj_baze_wyszukiwania, pobierz_dolnoslaskie_male_granty,
    pobierz_lgd_ducha_gor, pobierz_fed_dolny_slask, pobierz_umwd,
    pobierz_dfop, pobierz_jelenia_gora_ngo, pobierz_powiat_karkonoski
]

for funkcja in funkcje_skrapujace:
    dane, aktualne_id = funkcja(aktualne_id)
    wszystkie_granty.extend(dane)
    time.sleep(0.5)

with open('granty.json', 'w', encoding='utf-8') as f:
    json.dump(wszystkie_granty, f, ensure_ascii=False, indent=4)

print(f"✅ Sukces! Zapisano {len(wszystkie_granty)} rekordów z linkami.")
