import requests
import os
import time

bl_names = [
    ("Baden-Wuerttemberg", "baden-wuerttemberg"),
    ("Bayern", "bayern"),
    ("Berlin", "berlin"),
    ("Brandenburg", "brandenburg"),
    ("Bremen", "bremen"),
    ("Hamburg", "hamburg"),
    ("Hessen", "hessen"),
    ("Niedersachsen", "niedersachsen"),
    ("Nordrhein-Westfalen", "nordrhein-westfalen"),
    ("Rheinland-Pfalz", "rheinland-pfalz"),
    ("Saarland", "saarland"),
    ("Sachsen", "sachsen"),
    ("Sachsen-Anhalt", "sachsen-anhalt"),
    ("Schleswig-Holstein", "schleswig-holstein"),
    ("Thueringen", "thueringen")
]

base_url = "https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/PolizeilicheKriminalstatistik/2025/Bundeslaender"
url_patterns = [
    f"{base_url}/{{short}}/BL-TV-01-T40-TV-deutsch_xls.xlsx?__blob=publicationFile&v=1",
    f"{base_url}/{{short}}/BL-TV-02-T50-TV-nichtdeutsch_xls.xlsx?__blob=publicationFile&v=1",
    f"{base_url}/{{short}}/BL-TV-03-T62-TV-Staatsangehoerigkeiten_xls.xlsx?__blob=publicationFile&v=1",
]

found = []
for bl_full, bl_short in bl_names:
    for pattern in url_patterns:
        url = pattern.format(short=bl_short)
        try:
            r = requests.head(url, timeout=10, allow_redirects=True)
            if r.status_code == 200:
                found.append((bl_full, url))
                print(f"✓ {bl_full}: {url}")
                break  # Ersten Erfolg behalten
            else:
                print(f"✗ {bl_full} ({r.status_code}): {url}")
        except Exception as e:
            print(f"✗ {bl_full}: {url} -> {e}")
        time.sleep(0.5)

print("\n\nGefundene URLs:")
for bl, url in found:
    print(f"{bl}: {url}")
