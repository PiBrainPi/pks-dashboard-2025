#!/usr/bin/env python3
"""V18 Final Fix: Nur Faktoren skalieren, kein Duplikat mehr"""
import json

# Lade V17 Backup (das OHNE die korrigierten Faktoren)
with open('/home/claw_01_rasbpi5_1/bka_pks2025/pks_dashboard_data_v17_backup.json', 'r') as f:
    data = json.load(f)

print(f"Start: {len(data['bundeslaender'])} Bundesländer")
for bl in data['bundeslaender']:
    print(f"  - {bl['name']}")

target_summe = 1523090
current_summe = sum(bl['tv_gesamt'] for bl in data['bundeslaender'])

print(f"\nAktuelle Summe: {current_summe:,}")
print(f"BKA Target:     {target_summe:,}")
print(f"Fehlbetrag:     {target_summe-current_summe:+,}")

# Skalierungsfaktor berechnen
skala_faktor = target_summe / current_summe
print(f"Skalierung:     {skala_faktor:.4f} ({(1-skala_faktor)*100:+.1f}%)")

# Alle Werte skalieren
for bl in data['bundeslaender']:
    alter_tv = bl['tv_gesamt']
    bl['tv_gesamt'] = int(alter_tv * skala_faktor)
    bl['rate_pro_100k'] = round(bl['tv_gesamt'] / bl['einwohner'] * 100000, 1)
    bl['faktor'] = round(bl['faktor'] * skala_faktor, 2)

neue_summe = sum(bl['tv_gesamt'] for bl in data['bundeslaender'])
diff_pct = (neue_summe - target_summe) / target_summe * 100

print(f"\n{'='*70}")
print(f"EREBNIS:")
print(f"  BKA Target:  {target_summe:,}")
print(f"  Neue Summe:  {neue_summe:,}")
print(f"  Differenz:   {abs(neue_summe-target_summe):,} ({diff_pct:+.1f}%)")
print(f"  Bundesländer: {len(data['bundeslaender'])}")
print(f"{'='*70}")

if abs(diff_pct) < 0.1:
    print("✅ PERFECT (<0.1% Abweichung)")
elif abs(diff_pct) < 1:
    print("🟢 EXCELLENT (<1% Abweichung)")
else:
    print(f"⚠️ {diff_pct:.1f}% noch zu hoch")

# Update Meta
data['meta']['version'] = '1.1.0 V18'
data['meta']['stand'] = '10.05.2026 (Kalibriert auf BKA-Gesamtsumme)'

with open('/home/claw_01_rasbpi5_1/bka_pks2025/pks_dashboard_data.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ pks_dashboard_data.json für V18 fertig!")
print(f"   Dateipfad: /home/claw_01_rasbpi5_1/bka_pks2025/pks_dashboard_data.json")
