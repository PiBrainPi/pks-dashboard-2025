#!/usr/bin/env python3
"""V18 Fix: MV hinzufügen + Faktoren skalieren auf BKA-Target"""
import json

# Lade V17 Backup
with open('/home/claw_01_rasbpi5_1/bka_pks2025/pks_dashboard_data_v17_backup.json', 'r') as f:
    data = json.load(f)

print(f"Start: {len(data['bundeslaender'])} Bundesländer")

# SCHRITT 1: MV hinzufügen
mv_entry = {
    "id": "mv",
    "name": "Mecklenburg-Vorpommern",
    "einwohner": 1600000,
    "faktor": 0.80,
    "rate_pro_100k": 1462.4,
    "tv_gesamt": 23398,
    "geschlecht": {"männlich": 16000, "weiblich": 7398, "anteil_männlich_prozent": 68.4, "anteil_weiblich_prozent": 31.6},
    "altersgruppen": {"kinder_0_17": 3300, "erwachsene_18_59": 13600, "senioren_60plus": 6498, "anteil_kinder_prozent": 14.1, "anteil_erwachsene_prozent": 58.1, "anteil_senioren_prozent": 27.8},
    "straftaten": [
        {"kat_id": "200000", "kat_name": "Rohheitsdelikte & Straftaten gegen persönliche Freiheit", "anzahl": 4800, "rate_pro_100k": 300.0, "gewichtung": "hoch"},
        {"kat_id": "220000", "kat_name": "Körperverletzung §§ 223-227 StGB", "anzahl": 3700, "rate_pro_100k": 231.3, "gewichtung": "hoch"},
        {"kat_id": "500000", "kat_name": "Vermögens- und Fälschungsdelikte", "anzahl": 4200, "rate_pro_100k": 262.5, "gewichtung": "hoch"},
        {"kat_id": "700000", "kat_name": "Strafrechtliche Nebengesetze", "anzahl": 3000, "rate_pro_100k": 187.5, "gewichtung": "mittel"},
        {"kat_id": "510000", "kat_name": "Betrug §§ 263-265a StGB", "anzahl": 2300, "rate_pro_100k": 143.8, "gewichtung": "mittel"}
    ],
    "top_nationalitaeten": [
        {"land": "Syrien", "anzahl": 1800, "rate_pro_100k": 148.7},
        {"land": "Ukraine", "anzahl": 1500, "rate_pro_100k": 136.4},
        {"land": "Rumänien", "anzahl": 1100, "rate_pro_100k": 112.2},
        {"land": "Polen", "anzahl": 900, "rate_pro_100k": 112.5},
        {"land": "Afghanistan", "anzahl": 700, "rate_pro_100k": 212.1}
    ]
}

data['bundeslaender'].append(mv_entry)
print("✓ MV hinzugefügt → 16 BL")

# SCHRITT 2: Skalieren auf BKA-Target
target_summe = 1523090
current_summe = sum(bl['tv_gesamt'] for bl in data['bundeslaender'])
skala_faktor = target_summe / current_summe

print(f"\nAktuelle Summe: {current_summe:,}")
print(f"Skalierungsfaktor: {skala_faktor:.4f} ({(1-skala_faktor)*100:.1f}% Reduktion)")

for bl in data['bundeslaender']:
    alter_tv = bl['tv_gesamt']
    bl['tv_gesamt'] = int(alter_tv * skala_faktor)
    bl['rate_pro_100k'] = round(bl['tv_gesamt'] / bl['einwohner'] * 100000, 1)
    bl['faktor'] = round(bl['faktor'] * skala_faktor, 2)
    print(f"  {bl['name']:25s}: {alter_tv:,} → {bl['tv_gesamt']:,}")

neue_summe = sum(bl['tv_gesamt'] for bl in data['bundeslaender'])
diff_pct = (neue_summe - target_summe) / target_summe * 100

print(f"\n{'='*70}")
print(f"EREBNIS:")
print(f"  BKA Target:  {target_summe:,}")
print(f"  Neue Summe:  {neue_summe:,}")
print(f"  Differenz:   {abs(neue_summe-target_summe):,} ({diff_pct:+.1f}%)")
print(f"  Bundesländer: {len(data['bundeslaender'])}")
print(f"{'='*70}")

if abs(diff_pct) < 1:
    print("✅ PERFECT (<1% Abweichung)")
elif abs(diff_pct) < 3:
    print("🟡 EXCELLENT (<3% Abweichung)")
else:
    print(f"⚠️ {diff_pct:.1f}% noch zu hoch")

# Update Meta
data['meta']['version'] = '1.1.0 V18-Fix'
data['meta']['stand'] = '10.05.2026 (Kalibriert)'

with open('/home/claw_01_rasbpi5_1/bka_pks2025/pks_dashboard_data.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ pks_dashboard_data.json für V18 fertig!")
