# Phase 5: Dunkle Räume (Mine)

> **Hinweis:** Zurückgestellte Punkte (Messungen am Spiel, Referenzbilder, Clear-Farben) stehen in [offen.md](offen.md).

Ziel: Prüfen, ob die Sonderlogik für dunkle Räume durch die Clear-Farbe ersetzt werden kann, und den Rest sauber platzieren.

## Ausgangslage

- Die Dunkelheit in der Mine ist die Wolken-/Schattenschicht (0x7F-Sprites, nur 4:3 breit). Links/rechts davon fehlt die Abdunklung.
- Alt-Lösung: Füllquads (`ALU_DARK_FILL_COLOR` 0x66, ~40 %, Slot 959, subtraktiv), erkannt über Randspalten-Zählung in `alundra_cloud_loop`, plus Raumfarben-Switch für die Außenfarbe (z. B. (8,8,0)), plus Mine-Raum 3 mit eigenem Spaltenbereich 8..22 und Quad-Reihenfolge.
- Im Maskenband oben/unten: außen (24,24,24), innen (32,32,24); die Maske addiert beidseitig gleich.

## Idee

Setzt man die Clear-Farbe pro Raum auf den **abgedunkelten** Außenton, entfällt der Füllquad: außerhalb der Wolkenschicht sieht man nur Clear. Der Rand wird statisch und flackerfrei.

## Aufgaben

1. Pro Mine-Raum (`0x877DDF27`, `0xD78EE04C`, `0x56AA69AF`) die Soll-Farbe außen messen (Screenshot per PIL, Median links/rechts der Naht, HUD-Zeilen auslassen).
2. Farbe als Clear-Eintrag in Phase 3 setzen, prüfen, ob die Naht zwischen Wolkenschicht und Außen verschwindet.
3. Falls vertikale Farbunterschiede (Maskenband) stören: Quad-Variante als Zusatz im Wolken-Teil des Widescreen-Mods, nicht im Farbmod. Entscheiden nach Sicht.
4. Mine-Raum 3 (Spalten 8..22, leere schwarze Spalten links/rechts): Prüfen, ob Clear (8,8,0) die Naht an der ersten gezeichneten Kachelspalte löst oder ob (8,8,0)-Kacheln gegen (0,0,0)-Leerspalten sichtbar bleiben.
5. `ALU_DARK_FILL_COLOR` und Dunkelfüll-Code löschen, sobald alle Mine-Räume per Clear stimmen.

## Test

Alle drei Mine-Räume, Ring/Licht an/aus, Kamera links/rechts am Rand. Vergleich mit den bestätigten Alt-Ergebnissen.

## Abnahme

Nutzer bestätigt die Mine-Räume. Reicht Clear allein nicht, bleibt der Dunkelfüllquad als kleine, getrennte Funktion im Wolken-Teil des Widescreen-Mods, nicht im Rand-Mod.
