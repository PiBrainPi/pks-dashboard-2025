# 📊 PKS Dashboard 2025

**Polizeiliche Kriminalstatistik 2025** - Interaktives Dashboard mit Nationalitäten-Vergleich & Bundesländer-Analyse

## 🎯 Zielsetzung

Dieses Dashboard visualisiert die polizeiliche Kriminalstatistik (PKS) 2025 des Bundeskriminalamts (BKA) mit Fokus auf:

- **Tatverdächtigenzahlen** nach Nationalität (deutsche vs. nicht-deutsche TV)
- **Kriminalitätsraten** pro 100.000 Einwohner
- **Bundesländer-Vergleiche** mit interaktiven, sortierbaren Tabellen
- **Demografische Aufschlüsselung** nach Geschlecht und Altersgruppen

## 📁 Projektstruktur

```
bka_pks2025/
├── pks_dashboard_v18.html      # Finale Dashboard-Version (v1.0.2)
├── pks_dashboard_data.json     # Strukturierte Daten (16 Bundesländer)
├── bl_estimation.py            # Korrekturfaktor-Logik
├── fix_json_v18.py             # Datenbereinigung & Validierung
├── .gitignore                  # Git-Exclusions
└── README.md                   # Diese Datei
```

## 📊 Datenquelle

- **Primärquelle:** [BKA PKS 2025](https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/PKS2025/pksTabellen_Interpretationshilfen/ThematischeGliederung/tabellenthema_node.html)
- **Bevölkerungsdaten:** Destatis-Schätzungen (2025)
- **Validierung:** Gesamtsomme 1.523.084 TV (Abweichung: -0.00% zum BKA-Bund-Wert)

## ⚠️ Wichtiger Hinweis

> **ALLE BUNDESLÄNDER-WERTE SIND SCHÄTZUNGEN** basierend auf BKA-Bund-Daten mit regionalen Korrekturfaktoren. Diese Zahlen dienen ausschließlich zu Demonstrations- und Analyse-Zwecken und stellen keine offiziellen BKA-Angaben dar.

## 🚀 Nutzung

1. **Lokal öffnen:** `pks_dashboard_v18.html` in einem Browser öffnen
2. **Interaktivität:** Tabellen sind sortierbar (Klick auf Spalten-Header)
3. **Responsiv:** Funktioniert auf Desktop & Mobile

## 📈 Versionen

| Version | Datum | Änderungen |
|---------|-------|------------|
| v16 | 2026-05-09 | Initialer Nationalitäten-Vergleich |
| v17 | 2026-05-10 | Footer-Anpassung, DISCLAIMER |
| v18 | 2026-05-10 | **Final:** 16 BL, 0.0% Abweichung, Version 1.0.2 |

## 🔧 Technische Details

- **Frontend:** Pure HTML/CSS/JavaScript (kein Framework)
- **Datenformat:** JSON (leicht erweiterbar)
- **Validierung:** Python-Skripte mit `openpyxl` für Excel-Import
- **Design:** Dark/Light Theme, sortierbare Tabellen, visuelle Trennungen

## 📄 Lizenz

Dieses Projekt wurde erstellt mittels agentischer AI (~2h Entwicklung).

**Keine Gewähr auf Richtigkeit der Angaben!**

## 📞 Kontakt

- **Autor:** PiBrainPi
- **Repository:** [github.com/PiBrainPi/pks-dashboard-2025](https://github.com/PiBrainPi/pks-dashboard-2025)
- **Quelle:** [BKA PKS 2025](https://www.bka.de/DE/AktuelleInformationen/StatistikenLagebilder/PolizeilicheKriminalstatistik/PKS2025/Node.html)

---

*Letzte Aktualisierung: 10. Mai 2026*
