# Alundra: Sprechboxen ersetzen – Plan

Stand: 2026-11-20. Alles unten ist Hypothese, im Code noch nichts geprüft.

## Ziel
Die Original-Sprechbox (Pergamentrahmen, Namensschild, Porträt, Pixeltext) ausblenden und durch eigene Grafik plus eigenen, scharf gerenderten Text (TTF) ersetzen. Der Text kommt aus dem Spiel selbst.

## Phase 0 – Einstieg (ca. 30 Min)
- [ ] Projekt `C:\RecompDev\alundra-recomp` öffnen, Handoff-Datei in `C:\RecompDev` lesen.
- [ ] Prüfen, wie der 16:9-Stand (`full_2d` + Tile-Hooks) aufgebaut ist; dort wird der Overlay-Ansatz andocken.
- [ ] Testsave bereitstellen, der direkt vor einem Dialog steht (z. B. NPC "Jess").

## Phase 1 – Dialog-Routine finden
- [ ] Text im RAM suchen: Beim Dialog den String im Speicher lokalisieren (Emulator-Memory-Dump oder Log im Recomp-Build).
- [ ] Per Write-/Read-Watch herausfinden, welche Funktion den Text liest und die Glyphen zeichnet.
- [ ] Von dort aufwärts: Funktion für Box-Aufbau (Rahmen, Namensfeld, Porträt), Aufklapp-Animation, Warten auf Taste, Schließen.
- [ ] Ergebnis dokumentieren: Funktionsadressen, Parameter, Textpuffer-Format.

## Phase 2 – Text abgreifen (Log-Prototyp)
- [ ] Hook in die Textausgabe, der den dekodierten String und den Sprecher loggt.
- [ ] Steuercodes katalogisieren: Zeilenumbruch, Seitenwechsel, Pause, Farbe, Variablen (Spielername), Auswahlmenüs.
- [ ] Kodierung der Schrift klären (Zeichentabelle, Umlaute).

## Phase 3 – Original unterdrücken
- [ ] Zeichenaufrufe für Rahmen und Glyphen überspringen, Spiellogik (Warten auf Taste, Dialogende) unverändert lassen.
- [ ] Prüfen: Spiel läuft weiter, nichts hängt, Porträt/Name verhalten sich wie erwartet.

## Phase 4 – Eigene Box als Overlay
- [ ] Overlay-Pfad im Renderer: Quad mit PNG-Textur, 16:9-tauglich positioniert.
- [ ] TTF-Textrendering (z. B. stb_truetype oder vorhandene Lib) mit Zeilenumbruch.
- [ ] Zeitverhalten: Ein-/Ausblenden, Textlauf (Buchstabe für Buchstabe), Weiter-Symbol.
- [ ] Name und Porträt: erst Original behalten, später optional ersetzen.

## Phase 5 – Feinschliff
- [ ] Auswahlmenüs (Ja/Nein usw.), Itemtexte, Kampf-/Shop-Dialoge.
- [ ] Konfiguration in `game.toml` (an/aus, Schrift, Rahmengrafik).
- [ ] Optional: eigene Textquelle/Übersetzung statt Originaltext.

## Risiken
- Mehrere Dialogarten mit eigenen Routinen (Story, Schilder, Menüs) → mehrere Hooks nötig.
- Steuercodes falsch interpretiert → fehlender oder falsch umbrochener Text.
- Overlay-Timing weicht von der Spielanimation ab.

## Erstes Ziel für morgen
Phase 0–2: Dialog-Funktion finden und den Text von "Jess" im Log sehen.
