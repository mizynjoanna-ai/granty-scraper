import requests
from bs4 import BeautifulSoup
import json
import time

# Wspólne nagłówki, aby serwery nie odrzucały nas jako bota
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3'
}

def skrapuj_ngo(grant_id_start):
    print("Pobieranie danych z NGO.pl...")
    wyniki = []
    url = "https://fundusze.ngo.pl/konkursy"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Szukamy boksów ogłoszeń na NGO.pl
            artykuly = soup.find_all('div', class_='views-row')
            
            for art in artykuly:
                tytul_elem = art.find('h3') or art.find('a', class_='title')
                if not tytul_elem: continue
                
                tytul = tytul_elem.text.strip()
                # Próba wyciągnięcia organizatora i terminu
                org = "Sektor NGO / Fundacje"
                org_elem = art.find('div', class_='field-nam-organizator')
                if org_elem: org = org_elem.text.strip()
                
                termin = "Sprawdź na stronie"
                date_elem = art.find('time') or art.find('span', class_='date')
                if date_elem: termin = date_elem.text.strip()
                
                wyniki.append({
                    "id": grant_id_start,
                    "title": tytul,
                    "organization": org,
                    "amount": "Do ustalenia",
                    "deadline": termin,
                    "category": "Wsparcie NGO"
                })
                grant_id_start += 1
    except Exception as e:
        print(f"Błąd podczas skrapowania NGO.pl: {e}")
        
    return wyniki

def skrapuj_grantowo(grant_id_start):
    print("Pobieranie danych z Grantowo.pl...")
    wyniki = []
    url = "https://grantowo.pl/" # Główna strona agregatora
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Przykładowe kontenery dla struktury Grantowo
            bloki = soup.find_all('article') or soup.find_all('div', class_='post-item')
            
            for blok in bloki:
                tytul_elem = blok.find('h2') or blok.find('h3')
                if not tytul_elem: continue
                
                tytul = tytul_elem.text.strip()
                
                wyniki.append({
                    "id": grant_id_start,
                    "title": tytul,
                    "organization": "Agregator Grantowo.pl",
                    "amount": "Różne kwoty",
                    "deadline": "Bieżący rok",
                    "category": "Fundusze Krajowe/UE"
                })
                grant_id_start += 1
    except Exception as e:
        print(f"Błąd podczas skrapowania Grantowo.pl: {e}")
        
    return wyniki

def skrapuj_witkac(grant_id_start):
    print("Pobieranie danych z Witkac.pl...")
    wyniki = []
    url = "https://www.witkac.pl/public/konkursy"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            wiersze_konkursow = soup.find_all('tr', class_='contest-row') or soup.find_all('div', class_='contest-card')
            
            for wiersz in wiersze_konkursow:
                tytul = wiersz.find('td', class_='title').text.strip() if wiersz.find('td', class_='title') else "Konkurs Grantowy Witkac"
                organizator = wiersz.find('td', class_='institution').text.strip() if wiersz.find('td', class_='institution') else "Jednostka Samorządu"
                
                wyniki.append({
                    "id": grant_id_start,
                    "title": tytul,
                    "organization": organizator,
                    "amount": "Wg wniosku",
                    "deadline": "Zgodnie z naborem",
                    "category": "Samorządy / JST"
                })
                grant_id_start += 1
    except Exception as e:
        print(f"Błąd podczas skrapowania Witkac.pl: {e}")
        
    return wyniki

def skrapuj_ekonomia_spoleczna(grant_id_start):
    print("Pobieranie danych z EkonomiaSpoleczna.gov.pl...")
    wyniki = []
    url = "https://www.ekonomiaspoleczna.gov.pl/aktywne-nabory"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            lista_naborow = soup.find_all('div', class_='news-item') or soup.find_all('li', class_='row')
            
            for item in lista_naborow:
                link = item.find('a')
                if not link: continue
                tytul = link.text.strip()
                
                wyniki.append({
                    "id": grant_id_start,
                    "title": tytul,
                    "organization": "Ministerstwo Rodziny i Polityki Społecznej",
                    "amount": "Dofinansowanie rządowe",
                    "deadline": "Patrz ogłoszenie",
                    "category": "Ekonomia Społeczna"
                })
                grant_id_start += 1
    except Exception as e:
        print(f"Błąd podczas skrapowania EkonomiaSpoleczna.gov.pl: {e}")
        
    return wyniki

def glowny_menedzer():
    wszystkie_granty = []
    aktualny_id = 1
    
    # Uruchamiamy pobieranie z poszczególnych modułów
    wszystkie_granty.extend(skrapuj_ngo(aktualny_id))
    aktualny_id = len(wszystkie_granty) + 1
    time.sleep(1) # Krótka przerwa, by nie przeciążać serwerów
    
    wszystkie_granty.extend(skrapuj_grantowo(aktualny_id))
    aktualny_id = len(wszystkie_granty) + 1
    time.sleep(1)
    
    wszystkie_granty.extend(skrapuj_witkac(aktualny_id))
    aktualny_id = len(wszystkie_granty) + 1
    time.sleep(1)
    
    wszystkie_granty.extend(skrapuj_ekonomia_spoleczna(aktualny_id))
    
    # Dodajemy zabezpieczenie na wypadek, gdyby wszystkie portale akurat miały przerwę techniczną
    if not wszystkie_granty:
        print("Brak danych z sieci. Generowanie bazy zapasowej...")
        wszystkie_granty = [
            {
                "id": 1,
                "title": "Brak aktywnych naborów online - Serwery zajęte",
                "organization": "System",
                "amount": "0 PLN",
                "deadline": "---",
                "category": "Status"
            }
        ]
        
    # Zapisujemy skonsolidowany plik JSON
    nazwa_pliku = 'granty_z_sieci.json'
    with open(nazwa_pliku, 'w', encoding='utf-8') as f:
        json.dump(wszystkie_granty, f, ensure_ascii=False, indent=4)
        
    print(f"\nSukces! Zebrano łącznie {len(wszystkie_granty)} rekordów.")
    print(f"Dane zostały pomyślnie zapisane do pliku: {nazwa_pliku}")

if _name_ == "_main_":
    glowny_menedzer()
