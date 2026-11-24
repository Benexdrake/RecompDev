# Alundra – Map-Checkliste (Hintergrundfarbe pro Raum)

Quelle: https://www.vgmaps.com/Atlas/PSX/index.htm (Abschnitt "Alundra Maps", 49 Einträge, Dateien unter `https://www.vgmaps.com/Atlas/PSX/Alundra-<Name>.png`).
Code: `alundra-recomp/mods/alundra_bgcolor.c` (`alundra_room_color`, Switch auf Raum-Hash).

Farben (R,G,B), im Code als Konstanten:
- `ALU_BG_GREEN`  (0,8,0) = 0x00000800
- `ALU_BG_RED`    (8,0,0) = 0x00000008 (Default)
- `ALU_BG_YELLOW` (8,8,0) = 0x00000808
- `ALU_BG_GRAY`   (8,8,8) = 0x00080808
- `ALU_BG_BLACK`  (0,0,0) = 0x00000000

Pro Raum eintragen: Hash (Debug-Build, `read` des Kartenpuffers bzw. Log), gemessene Farbe, Status.
Status: `[ ]` offen, `[x]` geprüft (Farbe stimmt), `[d]` Default reicht.

Bekannte Zuordnung aus dem Code (ohne Map-Namen, Zuordnung zu den Maps unten noch offen):
- GREEN: 0x793D39CF, 0x1B8E3013 (Skelett), 0x489CF39A, 0xC114DD8E, 0x90C7456E (Höhlen), 0x5944BC3C, 0xA5781E10 (Gruft), 0x8A1528CF (Treppe), 0x32F8209E (Steinraum mit Buch), Rand-Hash 0x28BF794D (Höhle)
- BLACK: 0xD78EE04C, 0x56AA69AF (Mine)
- YELLOW: 0x877DDF27 (Mine), 0xB2956EA2, 0x7C900F86
- GRAY: 0x0C30BD01
- Himmelblau (96,120,136): 0x09B8D459 (Außenraum, Wolken rechts)
- Dorf: 0xB440C2D (Sonderfall, siehe `alundra-raumfarbe-switch.md`)

| # | Map | Räume/Hashes | Farbe | Status |
|---|-----|--------------|-------|--------|
| 1 | World | | | [ ] |
| 2 | World (In-Game Map) | | | [ ] |
| 3 | Inoa Village | 0xB440C2D (Dorf) + Häuser | Schwarz außen / Häuser Rot | [ ] |
| 4 | Inside Coal Mine | 0x877DDF27, 0xD78EE04C, 0x56AA69AF | s.o. | [ ] |
| 5 | Wendell's Dream | | | [ ] |
| 6 | Klark Ship | | | [ ] |
| 7 | Bonaire's Dream | | | [ ] |
| 8 | Giles's Dream | | | [ ] |
| 9 | Kline's Nightmare | | | [ ] |
| 10 | Ancient Shrine | | | [ ] |
| 11 | Coastal Cave | | | [ ] |
| 12 | Lars' Crypt | 0x5944BC3C, 0xA5781E10, 0x8A1528CF (vermutlich) | GREEN | [ ] |
| 13 | Reptile Lair | | | [ ] |
| 14 | Tarn's Manor | | | [ ] |
| 15 | Megalith Portal Chamber | | | [ ] |
| 16 | Magyscar | | | [ ] |
| 17 | Meia's Dream | | | [ ] |
| 18 | Watermill | | | [ ] |
| 19 | Fairy Pond | | | [ ] |
| 20 | Inspiration Point | | | [ ] |
| 21 | Magyscar Area | | | [ ] |
| 22 | Nirude's Lair | | | [ ] |
| 23 | Sanctuary Area | | | [ ] |
| 24 | Sanctuary | | | [ ] |
| 25 | Shack | | | [ ] |
| 26 | Underground Waterway | | | [ ] |
| 27 | Cliffs Of Madness | | | [ ] |
| 28 | Coal Mine Area | | | [ ] |
| 29 | Dark Swamp | | | [ ] |
| 30 | Despair Desert N | | | [ ] |
| 31 | Despair Desert S | | | [ ] |
| 32 | Fire Manor | | | [ ] |
| 33 | Mt. Torla & Ice Manor | | | [ ] |
| 34 | Outlook Point | | | [ ] |
| 35 | Pub & Pool | | | [ ] |
| 36 | Tarn's Manor Area | | | [ ] |
| 37 | Elene's Dream | | | [ ] |
| 38 | Murgg Woods | | | [ ] |
| 39 | Torla Mountain | | | [ ] |
| 40 | Tower Of The Great Tree | | | [ ] |
| 41 | Great Tree | | | [ ] |
| 42 | Nestus' Dream | | | [ ] |
| 43 | Nava's Keep | | | [ ] |
| 44 | Beach & Nava's Cabin | | | [ ] |
| 45 | Lake | | | [ ] |
| 46 | Lake Shrine | | | [ ] |
| 47 | Lake Shrine Interior | | | [ ] |
| 48 | Debug (000) | | | [ ] |
| 49 | Debug (011) | | | [ ] |
