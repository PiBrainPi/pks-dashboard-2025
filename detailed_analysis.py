import openpyxl
import json

folder = "/home/claw_01_rasbpi5_1/bka_pks2025"
results = {"altersgruppen": {}, "geschlecht": {}, "straftat_kategorien": {}, "top_laender": {}}

# Bevölkerungsschätzungen (für Raten pro 100k)
pop = {
    "deutsch": 71300000,
    "tuerkei": 2200000,
    "syrien": 1220000,
    "rumaenien": 980000,
    "ukraine": 1100000,
    "polen": 850000,
    "afghanistan": 330000,
    "bulgarien": 420000,
    "serbien": 310000,
    "irak": 280000,
}

# Mapping Ländernamen zu Keys
laender_map = {
    "Deutschland": "deutsch",
    "Türkei": "tuerkei", 
    "Syrien": "syrien",
    "Rumänien": "rumaenien",
    "Ukraine": "ukraine",
    "Polen": "polen",
    "Afghanistan": "afghanistan",
    "Bulgarien": "bulgarien",
    "Serbien": "serbien",
    "Irak": "irak",
}

# 1. ALTERSGRUPPEN (aus T50 - nichtdeutsche TV nach Alter) 
# und T40 für Deutsche (ähnliche Struktur)
try:
    # Deutsche Altersgruppen
    wb40 = openpyxl.load_workbook(f"{folder}/12-T40-TV-deutsch.xlsx", read_only=True)
    ws40 = wb40['T40']
    
    # Suche die Altersgruppen-Zeilen (ab Zeile 7 ca.)
    alters_de = {}
    for row in ws40.iter_rows(min_row=7, max_col=24, values_only=True):
        if not row[0] or not isinstance(row[0], (int, float)):
            continue
        if row[1] and 'insgesamt' in str(row[1]).lower():
            # Alternativ: Suche nach Altersgruppen-Schlüsseln
            pass
    
    # Vereinfachter Ansatz: Nutze T50 für nichtdeutsche Altersgruppen
    wb50 = openpyxl.load_workbook(f"{folder}/17-T50-TV-nichtdeutsch.xlsx", read_only=True)
    ws50 = wb50['T50']
    
    alters_nd = {}
    # Header in Zeile 5/6 finden
    headers = None
    for idx, row in enumerate(ws50.iter_rows(min_row=1, max_col=24, values_only=True)):
        if idx >= 6:  # ab Zeile 7 (0-index 6)
            break
        if row[1] and 'insgesamt' in str(row[1]).lower():
            # Das ist die Gesamtzeile, nicht Header
            continue
        if any('Kinder' in str(cell) for cell in row if cell):
            headers = [str(cell).strip() for cell in row]
            break
    
    # Wenn kein Header gefunden, nehme Standard-Spalten
    if not headers:
        headers = ["Schlüssel", "Straftat", "Sexus", "TV_insgesamt", 
                   "bis_unter_6", "6_bis_unter_8", "8_bis_unter_10", "10_bis_unter_12",
                   "12_bis_unter_14", "14_bis_unter_16", "16_bis_unter_18", "18_bis_unter_21",
                   "21_bis_unter_25", "25_bis_unter_30", "30_bis_unter_40", "40_bis_unter_50",
                   "50_bis_unter_60", "60_bis_unter_65", "65_bis_unter_70", "70_bis_unter_75",
                   "75_und_aelter"]
    
    # Gruppierung: Kinder (0-17), Erwachsene (18-59), Senioren (60+)
    kinder_idx = list(range(4, 12))  # bis unter 18
    erwachsene_idx = list(range(12, 17))  # 18 bis unter 60
    senioren_idx = list(range(17, 21))  # 60+
    
    for row in ws50.iter_rows(min_row=7, max_col=24, values_only=True):
        if row[1] and 'insgesamt' in str(row[1]).lower():
            kinder = sum(row[i] for i in kinder_idx if i < len(row) and isinstance(row[i], (int, float)))
            erwachsene = sum(row[i] for i in erwachsene_idx if i < len(row) and isinstance(row[i], (int, float)))
            senioren = sum(row[i] for i in senioren_idx if i < len(row) and isinstance(row[i], (int, float)))
            alters_nd = {
                "kinder_0_17": int(kinder),
                "erwachsene_18_59": int(erwachsene),
                "senioren_60plus": int(senioren),
                "gesamt": int(row[3]) if len(row) > 3 else None
            }
            break
    
    wb50.close()
    wb40.close()
    
    results['altersgruppen'] = {
        "nichtdeutsche": alters_nd,
        "deutsche": "Siehe T40-Analyse (analog strukturiert)"
    }
except Exception as e:
    results['altersgruppen'] = {"error": str(e)}

# 2. GESCHLECHT (männlich / weiblich)
try:
    # T50 hat Spalte "Sexus" (M/F) - Zeilen mit M und F getrennt
    wb50 = openpyxl.load_workbook(f"{folder}/17-T50-TV-nichtdeutsch.xlsx", read_only=True)
    ws50 = wb50['T50']
    
    geschlecht_nd = {"männlich": 0, "weiblich": 0}
    for row in ws50.iter_rows(min_row=7, max_col=5, values_only=True):
        if not row[2]:  # Sexus-Spalte
            continue
        sexus = str(row[2]).strip().upper()
        if 'M' in sexus:
            geschlecht_nd['männlich'] += int(row[3]) if isinstance(row[3], (int, float)) else 0
        elif 'W' in sexus or 'F' in sexus:
            geschlecht_nd['weiblich'] += int(row[3]) if isinstance(row[3], (int, float)) else 0
    
    wb50.close()
    
    # Deutsche analog aus T40
    wb40 = openpyxl.load_workbook(f"{folder}/12-T40-TV-deutsch.xlsx", read_only=True)
    ws40 = wb40['T40']
    
    geschlecht_de = {"männlich": 0, "weiblich": 0}
    for row in ws40.iter_rows(min_row=7, max_col=5, values_only=True):
        if not row[2]:
            continue
        sexus = str(row[2]).strip().upper()
        if 'M' in sexus:
            geschlecht_de['männlich'] += int(row[3]) if isinstance(row[3], (int, float)) else 0
        elif 'W' in sexus or 'F' in sexus:
            geschlecht_de['weiblich'] += int(row[3]) if isinstance(row[3], (int, float)) else 0
    
    wb40.close()
    
    # Raten berechnen
    results['geschlecht'] = {
        "deutsche": {
            **geschlecht_de,
            "männlich_pro_100k": round(geschlecht_de['männlich'] / pop['deutsch'] * 100000, 1),
            "weiblich_pro_100k": round(geschlecht_de['weiblich'] / pop['deutsch'] * 100000, 1),
        },
        "nichtdeutsche_gesamt": {
            **geschlecht_nd,
            "männlich_pro_100k": round(geschlecht_nd['männlich'] / 12100000 * 100000, 1),
            "weiblich_pro_100k": round(geschlecht_nd['weiblich'] / 12100000 * 100000, 1),
        }
    }
except Exception as e:
    results['geschlecht'] = {"error": str(e)}

# 3. STRFTAT-KATEGORIEN (Top-Level Gruppen aus T62)
try:
    wb62 = openpyxl.load_workbook(f"{folder}/22-T62-TV-Staatsangehoerigkeiten.xlsx", read_only=True)
    ws62 = wb62['T62 BKA']
    
    # Suche Hauptkategorien (gekennzeichnet durch 6-stellige Schlüssel wie 010000, 020000...)
    kategorien = []
    for row in ws62.iter_rows(min_row=7, max_col=5, values_only=True):
        if not row[0] or not isinstance(row[0], str):
            continue
        key = str(row[0]).strip()
        if len(key) == 6 and key.endswith('0000'):  # Hauptkategorie
            kategorien.append({
                "schluessel": key,
                "bezeichnung": row[1] if len(row) > 1 else "",
                "gesamt_tv": int(row[2]) if len(row) > 2 and isinstance(row[2], (int, float)) else 0,
            })
    
    # Top 10 nach Gesamtzahl
    top_kat = sorted(kategorien, key=lambda x: x['gesamt_tv'], reverse=True)[:10]
    
    # Raten pro 100k (Deutsche vs. Nichtdeutsche)
    # Spalte C = Nichtdeutsche gesamt, Spalte D = Deutschland
    # (brauche Mapping welche Spalte welches Land)
    
    results['straftat_kategorien'] = {
        "top_10_nach_gesamtzahl": top_kat,
        "hinweis": "Detaillierte Raten pro Land erfordern Spalten-Mapping aus T62"
    }
    wb62.close()
except Exception as e:
    results['straftat_kategorien'] = {"error": str(e)}

# 4. TOP-LÄNDER DETAIL (Afghanistan, Syrien, Rumänien exemplarisch)
try:
    wb62 = openpyxl.load_workbook(f"{folder}/22-T62-TV-Staatsangehoerigkeiten.xlsx", read_only=True)
    ws62 = wb62['T62 BKA']
    
    # Header
    headers = None
    for row in ws62.iter_rows(min_row=5, max_row=5, values_only=True):
        headers = list(row)
        break
    
    # Länderspalten finden (ab Spalte E = Index 4)
    laender_spalten = {}
    for idx in range(4, len(headers)):
        land = str(headers[idx]).strip()
        if land and land != "None":
            laender_spalten[land] = idx
    
    # Top-Länder analysieren (Syrien, Afghanistan, Rumänien)
    top_laender_keys = ["Syrien", "Afghanistan", "Rumänien", "Türkei", "Ukraine"]
    top_results = {}
    
    for land in top_laender_keys:
        if land in laender_spalten:
            col_idx = laender_spalten[land]
            # Top 5 Straftat-Kategorien für dieses Land
            kats = []
            for row in ws62.iter_rows(min_row=7, max_col=col_idx+1, values_only=True):
                if not row[0] or not isinstance(row[0], str):
                    continue
                key = str(row[0]).strip()
                if len(key) == 6 and key.endswith('0000'):
                    wert = row[col_idx] if len(row) > col_idx else 0
                    if wert and isinstance(wert, (int, float)) and wert > 0:
                        kats.append({
                            "schluessel": key,
                            "bezeichnung": row[1] if len(row) > 1 else "",
                            "anzahl": int(wert)
                        })
            top5 = sorted(kats, key=lambda x: x['anzahl'], reverse=True)[:5]
            pop_key = laender_map.get(land, "").lower()
            pop_wert = pop.get(pop_key, 100000)  # Fallback 100k
            gesamt_land = sum(k['anzahl'] for k in kats)
            top_results[land] = {
                "gesamt_tv": gesamt_land,
                "rate_pro_100k": round(gesamt_land / pop_wert * 100000, 1),
                "top_5_straftaten": top5
            }
    
    results['top_laender'] = top_results
    wb62.close()
except Exception as e:
    results['top_laender'] = {"error": str(e)}

print(json.dumps(results, indent=2, ensure_ascii=False))
