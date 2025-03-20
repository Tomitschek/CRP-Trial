# Praktischer Leitfaden zur Analyse klinischer Zeitreihendaten

## Einführung

Die Analyse klinischer Zeitreihendaten stellt uns in der medizinischen Forschung vor besondere Herausforderungen, bietet aber auch einzigartige Möglichkeiten. Dieser Leitfaden führt durch den Prozess der Analyse longitudinaler klinischer Daten und verwendet dabei eine postoperative CRP-Studie als durchgehendes Beispiel. Wir behandeln den gesamten Prozess von der ersten Datenexploration bis zur ausgefeilten statistischen Analyse.

## Teil 1: Verständnis der Daten

### Biologischer und klinischer Kontext

Bevor wir uns in die Statistik vertiefen, ist es wichtig, den biologischen und klinischen Kontext der Messungen zu verstehen:

1. Natürlicher Verlauf des Parameters
   - Was ist der Normalbereich?
   - Wie schnell kann sich der Wert ändern?
   - Welche Faktoren beeinflussen die Werte?

2. Klinische Relevanz
   - Welche Änderungen sind klinisch bedeutsam?
   - Wie groß ist der Messfehler?
   - Gibt es etablierte klinische Schwellenwerte?

**Beispiel**: In unserer CRP-Studie wissen wir:
- Normales CRP liegt bei < 5 mg/L
- Nach einer Operation erreicht CRP typischerweise nach 48-72 Stunden seinen Höchstwert
- Änderungen > 50 mg/L sind klinisch signifikant
- Der Labormessfehler beträgt etwa 5%
- Werte > 100 mg/L deuten auf eine signifikante Entzündung hin

### Beurteilung der Datenstruktur

Untersuchen Sie Ihre Datenstruktur sorgfältig:

1. Zeitliche Eigenschaften
   - Werden die Messungen in festen Intervallen durchgeführt?
   - Gibt es fehlende Zeitpunkte?
   - Wie lang ist der Nachbeobachtungszeitraum?

2. Gruppeneigenschaften
   - Wie viele Gruppen gibt es?
   - Stichprobengröße pro Gruppe?
   - Vergleichbarkeit der Ausgangswerte?

**Beispiel**: Unsere CRP-Studie hat:
- Tägliche Messungen über 7 Tage postoperativ
- Eine Ausgangsmessung (Tag 0)
- Zwei Gruppen: Antibiotika vs. Kontrolle
- 20 Patienten pro Gruppe
- Randomisierte Zuteilung zur Sicherstellung der Baseline-Vergleichbarkeit

## Teil 2: Erste Datenexploration

### Visuelle Exploration

Beginnen Sie immer mit Visualisierungen:

1. Individuelle Verlaufsgrafiken
   - Plotten Sie die Daten jedes Patienten separat
   - Suchen Sie nach Ausreißern und ungewöhnlichen Mustern
   - Beurteilen Sie die Variabilität zwischen Patienten

2. Visualisierungen auf Gruppenebene
   - Plotten Sie mittlere Verläufe mit Konfidenzintervallen
   - Erstellen Sie Boxplots für jeden Zeitpunkt
   - Erwägen Sie Heatmaps für dichte Zeitreihen

3. Muster fehlender Daten
   - Erstellen Sie Visualisierungen fehlender Daten
   - Suchen Sie nach systematischen Mustern bei fehlenden Werten

### Deskriptive Statistik

Berechnen Sie für jeden Zeitpunkt:

1. Zentrale Tendenz
   - Mittelwert und Median
   - Interquartilsabstand
   - Standardabweichung

2. Datenqualitätsmetriken
   - Prozentsatz fehlender Werte
   - Anzahl der Ausreißer
   - Messbereiche

## Teil 3: Statistische Analyse

### Wahl des richtigen Ansatzes

Berücksichtigen Sie diese Faktoren bei der Auswahl statistischer Methoden:

1. Primäre Forschungsfrage
   - Gesamtunterschied zwischen Gruppen?
   - Unterschied zu bestimmten Zeitpunkten?
   - Veränderungsrate?

2. Dateneigenschaften
   - Normalverteilung
   - Muster fehlender Daten
   - Zeitliche Korrelationsstruktur

3. Stichprobengrößenüberlegungen
   - Power für verschiedene Analysen
   - Mehrfachtestungsproblematik
   - Effektgrößenschätzung

### Empfohlene statistische Ansätze

1. Primäre Analyse: Lineare gemischte Modelle
   ```R
   # R-Beispiel
   model <- lmer(wert ~ gruppe * zeit + (1|patient), data=daten)
   ```

   Vorteile:
   - Guter Umgang mit fehlenden Daten
   - Berücksichtigt Innersubjekt-Korrelation
   - Kann komplexe Zeitmuster modellieren
   - Erhält statistische Power

2. Sekundäre Analysen:
   - Fläche unter der Kurve (AUC) Analyse
   - Zeit-bis-Ereignis-Analyse für das Erreichen von Schwellenwerten
   - Vergleich der Maximalwerte
   - Analyse der Veränderungsrate

## Teil 4: Beispielanalyse: Postoperative CRP-Studie

### Studienüberblick
- Ziel: Vergleich der CRP-Verläufe zwischen Antibiotika- und Kontrollgruppe
- Hypothese: Antibiotika-Gruppe zeigt schnellere CRP-Normalisierung
- Primärer Endpunkt: CRP-Verlauf über 7 Tage
- Sekundärer Endpunkt: Zeit bis CRP < 100 mg/L

### Analyseplan

1. Primäre Analyse:
   ```python
   # Spezifikation des gemischten Modells
   model = MixedLM.from_formula(
       "crp ~ gruppe + zeit + gruppe:zeit",
       groups="patient_id",
       data=df
   )
   ```

2. Sekundäre Analysen:
   - Vergleich der CRP-Maximalwerte
   - Berechnung der Zeit bis zur 50%-Reduktion
   - Vergleich der Werte an Tag 5 (wenn die meisten Patienten normalisiert haben sollten)

### Interpretationsrichtlinien

1. Klinische Signifikanz
   - Berücksichtigen Sie absolute Unterschiede zwischen Gruppen
   - Betrachten Sie individuelle Patientenverläufe
   - Beurteilen Sie praktische Implikationen

2. Statistische Signifikanz
   - Berücksichtigen Sie multiples Testen
   - Betrachten Sie Effektgröße neben p-Werten
   - Berichten Sie Konfidenzintervalle

## Teil 5: Ergebnisdarstellung

### Wesentliche Elemente

1. Studiencharakteristika
   - Stichprobengrößen und Demographie
   - Muster fehlender Daten
   - Protokollabweichungen

2. Ergebnispräsentation
   - Grafische Zusammenfassungen
   - Wichtige numerische Befunde
   - Sowohl Gruppen- als auch individuelle Erkenntnisse

3. Diskussion der Limitationen
   - Auswirkungen fehlender Daten
   - Generalisierbarkeit
   - Potenzielle Störfaktoren

### Beispiel eines Ergebnisabschnitts

"Die Antibiotika-Gruppe zeigte signifikant niedrigere CRP-Maximalwerte (150 ± 20 mg/L vs. 180 ± 25 mg/L, p < 0,01) und eine schnellere Normalisierung (mediane Zeit bis CRP < 100 mg/L: 4 Tage vs. 6 Tage, p < 0,01). Die Analyse mit linearem gemischtem Modell ergab eine signifikante Gruppe-Zeit-Interaktion (β = -15,2, 95% KI: -20,1 bis -10,3, p < 0,001), was auf unterschiedliche Verläufe zwischen den Gruppen hinweist."

## Fazit

Die Analyse klinischer Zeitreihen erfordert sorgfältige Berücksichtigung sowohl statistischer als auch klinischer Aspekte. Der Erfolg hängt ab von:
- Verständnis des biologischen Kontexts
- Gründlicher explorativer Analyse
- Angemessener statistischer Modellierung
- Klarer Kommunikation der Ergebnisse

Denken Sie daran, dass das Ziel nicht nur statistische Signifikanz ist, sondern bedeutsame klinische Erkenntnisse, die die Patientenversorgung verbessern können.

## Bedienungsanleitung

### Installation und Einrichtung

1. **Virtuelle Umgebung aktivieren:**
   ```
   # Windows:
   c:\Users\muelltho\git-rpositories\CRP-Trial\venv\Scripts\activate.bat
   
   # PowerShell:
   c:\Users\muelltho\git-rpositories\CRP-Trial\venv\Scripts\Activate.ps1
   
   # Linux/macOS:
   source c:/Users/muelltho/git-rpositories/CRP-Trial/venv/bin/activate
   ```

2. **Abhängigkeiten installieren:**
   ```
   pip install -r requirements.txt
   ```

### Anwendung

Das Tool besteht aus drei Hauptkomponenten im `src` Verzeichnis:
- `generate.py` - Erzeugt synthetische CRP-Daten
- `analyse.py` - Analysiert die Daten und erstellt Visualisierungen
- `main.py` - Benutzerfreundliche Schnittstelle für den gesamten Workflow

#### Ausführung

Verwenden Sie das `run.py` Skript im Hauptverzeichnis:

```
python run.py [Optionen]
```

#### Detaillierte Beschreibung der Parameter

* `--generate`
  - Beschreibung: Erzeugt einen neuen Datensatz mit synthetischen CRP-Daten
  - Typ: Flag (ohne Wertangabe)
  - Standard: Nicht gesetzt (es werden keine neuen Daten erzeugt)
  - Beispiel: `python run.py --generate`

* `--day-effects`
  - Beschreibung: Definiert die Größe der Behandlungseffekte für bestimmte Tage als Python-Dictionary
  - Typ: String (Python-Dictionary-Format)
  - Standard: `"{5: 50}"` (starker Effekt an Tag 5)
  - Format: `"{Tag1: Effektgröße1, Tag2: Effektgröße2, ...}"`
  - Hinweis: Positive Werte bedeuten niedrigere CRP-Werte in der Behandlungsgruppe
  - Beispiele:
    - `--day-effects "{5: 50}"` - Starker Effekt (50 Einheiten) nur an Tag 5
    - `--day-effects "{}"` - Kein Behandlungseffekt
    - `--day-effects "{3: 10, 4: 20, 5: 30, 6: 40, 7: 50}"` - Ansteigender Behandlungseffekt

* `--input-file`
  - Beschreibung: Pfad zur Eingabedatei mit CRP-Daten im CSV-Format
  - Typ: String (Dateipfad)
  - Standard: `output/crp_raw_data.csv`
  - Beispiel: `--input-file meine_daten.csv`

* `--output-md`
  - Beschreibung: Pfad zur Ausgabedatei für die Analyseergebnisse im Markdown-Format
  - Typ: String (Dateipfad)
  - Standard: `output/crp_analysis_results.md`
  - Beispiel: `--output-md output/meine_ergebnisse.md`

* `--output-excel`
  - Beschreibung: Pfad zur Excel-Ausgabedatei mit den Daten im breiten Format (eine Zeile pro Patient)
  - Typ: String (Dateipfad)
  - Standard: `output/crp_data_wide.xlsx`
  - Beispiel: `--output-excel output/meine_daten.xlsx`

#### Beispiele für typische Anwendungsfälle

1. **Neue Daten erzeugen mit Standardeinstellungen:**

```
python run.py --generate
```
Erzeugt einen neuen Datensatz mit einem starken Behandlungseffekt an Tag 5 und speichert ihn als `output/crp_raw_data.csv`.

2. **Neue Daten mit spezifischem Behandlungseffektmuster erzeugen:**

```
python run.py --generate --day-effects "{3: 10, 4: 20, 5: 30, 6: 20, 7: 10}"
```

Erzeugt Daten mit einem ansteigenden und dann abnehmenden Behandlungseffekt.

3. **Neue Daten ohne Behandlungseffekt erzeugen (für Nullhypothese):**

```
python run.py --generate --day-effects "{}"
```

Erzeugt Daten ohne Unterschied zwischen den Gruppen.

4. **Vorhandene Daten aus einer bestimmten Datei analysieren:**

```
python run.py --input-file meine_crp_daten.csv
```

Analysiert die Daten aus der angegebenen Datei ohne neue Daten zu generieren.

5. **Vollständiger Workflow mit benutzerdefinierten Dateipfaden:**

```
python run.py --generate --day-effects "{4: 30, 5: 40}" --output-md ergebnisse/analyse.md --output-excel daten/final_data.xlsx
```

Erzeugt Daten mit Effekten an Tag 4 und 5, und speichert die Ergebnisse in benutzerdefinierten Verzeichnissen.

#### Interpretieren der Ergebnisse

Nach dem Ausführen des Skripts werden mehrere Ausgaben erstellt:

1. **CSV-Datei mit Rohdaten**: Enthält die CRP-Werte für jeden Patienten an jedem Tag im langen Format.

2. **Excel-Datei mit Daten im breiten Format**: Ein Patient pro Zeile, mit Spalten für jeden Tag.

3. **Markdown-Bericht**: Enthält:
- Zusammenfassende Statistiken
- Deskriptive Statistiken nach Gruppe und Tag
- Ergebnisse des linearen gemischten Modells
- T-Test-Ergebnisse für maximale CRP-Werte
- Analyse der Zeit bis zur CRP-Normalisierung
- Fazit und Einschränkungen
- Grafiken

4. **Visualisierungen**:
- `crp_over_time.png`: Verlauf der CRP-Werte nach Gruppe
- `individual_patient_plots.png`: Individuelle Verläufe für jeden Patienten
- `crp_boxplot.png`: Boxplot-Darstellung der CRP-Werte nach Tag und Gruppe
- `crp_over_time_by_group.png`: Detaillierte Darstellung mit Standardfehler und p-Werten

## Beispiel output
einen kompletten Beispieloutput findet sich unter ./example

## Projektstruktur

Dieses Projekt ist als Python-Paket organisiert, um die Wartbarkeit, Erweiterbarkeit und Wiederverwendbarkeit zu verbessern.
```
CRP-Trial/
├── README.md                   # Diese Dokumentation
├── requirements.txt            # Python-Abhängigkeiten
├── setup.py                    # Paket-Setup für pip-Installation
├── .gitignore                  # Ignorierte Dateien für Git
├── run.py                      # Haupteinstiegspunkt zum Ausführen der Analyse
│
├── crptrial/                   # Hauptpaketverzeichnis
│   ├── __init__.py             # Paketinitialisierung
│   │
│   ├── generate/               # Code für die Datengenerierung
│   │   ├── __init__.py
│   │   └── generator.py        # Funktionen zur Erzeugung synthetischer Daten
│   │
│   ├── analysis/               # Analysemodule
│   │   ├── __init__.py
│   │   ├── stats.py            # Statistische Analysefunktionen
│   │   ├── plotting.py         # Funktionen für die Datenvisualisierung
│   │   └── reporting.py        # Funktionen für die Berichterstellung
│   │
│   ├── utils/                  # Hilfsfunktionen
│   │   ├── __init__.py
│   │   └── io.py               # Datei-I/O-Operationen
│   │
│   └── cli.py                  # Befehlszeilenschnittstelle
├── example                     # Beispiel output
│
└── output/                     # Ausgabeverzeichnis (gitignoriert)
    ├── crp_raw_data.csv        # Rohdaten im CSV-Format
    ├── crp_data_wide.xlsx      # Daten im breiten Format (Excel)
    ├── crp_analysis_results.md # Ergebnisbericht im Markdown-Format
    └── *.png                   # Generierte Abbildungen
```