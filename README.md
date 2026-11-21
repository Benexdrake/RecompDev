# RecompDev

Meta-Repo für meine PSX-Static-Recompilation-Projekte (Framework: [psxrecomp](https://github.com/RetroPortingToolKit/psxrecomp)).

| Projekt | Repo | Stand |
|---|---|---|
| Alundra (EU/DE) | [Alundra-Recomp](https://github.com/Benexdrake/Alundra-Recomp) | 16:9, HUD-Ecken, weicher Kartenrand |
| Breath of Fire III (EU) | [BreathOfFire3-Recomp](https://github.com/Benexdrake/BreathOfFire3-Recomp) | 16:9 |
| Breath of Fire IV (EU) | [BreathOfFire4-Recomp](https://github.com/Benexdrake/BreathOfFire4-Recomp) | gebaut, ungetestet |
| Legend of Dragoon (DE) | [LegendOfDragoon-Recomp](https://github.com/Benexdrake/LegendOfDragoon-Recomp) | 16:9 im Kampf |

Klonen: `git clone --recurse-submodules https://github.com/Benexdrake/RecompDev.git`

Jedes Projekt bindet das Framework als Submodul aus einem Fork ein ([Benexdrake/psxrecomp](https://github.com/Benexdrake/psxrecomp), je ein Branch pro Spiel mit lokalen Änderungen).

**Enthalten sind keine Spieldaten.** Disc-Images, Spiel-EXEs und der daraus generierte Code (`generated/`) bleiben lokal; jeder erzeugt sie aus seiner eigenen Disc.

- `CLAUDE.md`: Projektstand, Workflow und Debug-Hinweise
- `docs/`: Handoff-Dokumente und Erkenntnisse (`docs/memory/`)
