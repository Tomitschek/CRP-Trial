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


# get started: 
- c:\Users\muelltho\git-rpositories\CRP-Trial\venv\Scripts\activate.bat
-