# Phase 3: Mod Hintergrundfarbe (`background_color`)

Ziel: Das Clear-FillRect (Befehl 0x02, 320x240, erstes Paket jedes Frames) wird pro Raum in der gewünschten Farbe gefüllt. Default Schwarz.

## 3a Technik klären (zuerst)

Befund aus `alundra-clear-layer-ansatz.md`: RAM-Schreiben auf das Paket bleibt ohne Wirkung (das Spiel schreibt es neu). Die Adresse wechselt mit dem Puffer (0x801F4028 / 0x801F3728 / 0x801F3428, Stride 0x300). Der Schreiber 0x80086AAC ist nur der DMA-Walker.

Zu prüfen, in dieser Reihenfolge:
1. **Wer schreibt das Paket?** `wtrace_add` auf die Paketadresse (alte Boot-Watches vorher löschen). Die Clear-Routine im statischen Code suchen (`build-debugtools/cache/tmp/*/out/overlay_8002A000.psx_full.c`).
2. **Variante A:** Instruction-Hook direkt nach dem Schreiben (neuer Site, braucht `generate`, einige Minuten), Farbwort neu schreiben.
   **Variante B:** Hook vor dem DMA-Start, Paket im OT-Ende-Block suchen und umfärben.
   **Variante C (Fallback):** Mod-API im Framework, die FillRect 0x02 im GPU-Decoder umfärbt (`psxrecomp/runtime/src/gpu.c`, wie die Debug-Hilfe `PSX_DEBUG_FILL_RGB`). Das ist eine Framework-Änderung für alle Projekte, nur nach Rücksprache.
3. **Nur das Clear umfärben**, nicht andere FillRects (VRAM-Füllungen, Menü-Rechtecke): Vollbild 320x240 am Frameanfang als Merkmal.

## 3b Mod-Aufbau

- `alundra_bgcolor.c`, Plugin `alundra.bgcolor`.
- `alundra_room_color(sig)` als `switch` über `alundra_room_sig()` (FNV-1a über 24960 B ab 0x800DD86C), `default` = Schwarz (0,0,0). Farbformat 0x00BBGGRR.
- Hash nicht jeden Frame über 25 KB rechnen (bei Raumwechsel oder alle N Frames), Übergang beim Laden sauber behandeln (kein Aufblitzen falscher Farbe).
- Feature aus: Spiel-Clear bleibt unberührt.

## 3c Raumtabelle füllen

Aus der Messtabelle von Phase 0:
- Räume, deren Spiel-Clear schon passt: kein Eintrag (Default).
- Mine-Räume (8,8,0), Skelett-Räume (0,8,0) usw.: Eintrag nur, wenn der Rand dadurch besser aussieht als Schwarz.
- Was der Rand zeigen soll, entscheidet der Nutzer nach Sicht. Räume mit gleicher Randfarbe (Grabstätte, Mine, Schuppen, Haus) ggf. gruppieren.
- Räume, bei denen eine Farbe nicht reicht (vertikale Unterschiede, z. B. Maskenband): Phase 5.

## Zur Entscheidung "Default Schwarz"

Das Spiel hat im Skelett-Raum (0,8,0), also nicht reines Schwarz. Beim früheren Clear-auf-Schwarz-Versuch sah der Außenbereich "zu schwarz" gegenüber den dunkelgrünen Randkacheln aus. Dafür sind die Tabelleneinträge da: eigene Farbe pro Raum, nie global.

## Test

- Alle Räume der Testmatrix mit Default (Schwarz) und mit Tabelle.
- Kein Flackern beim Scrollen, Raumwechsel, Laden, Menü, Dialog, FMV, Game Over.
- Schalter `background_color = false` in `state.toml`: Spiel-Clear original.
- `PSX_DEBUG_FILL_ONLY=1` + `PSX_DEBUG_FILL_RGB=BBGGRR` zeigt, was die Clear-Schicht allein macht.

## Abnahme

Nutzer bestätigt pro Raum der Matrix. Danach darf der Alt-Rand-Code ersatzlos weg (Phase 6).
