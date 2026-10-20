# Puzzle Game (PowerPoint)

"An simple puzzle game..?" is a mouse-dexterity puzzle game built entirely in
Microsoft PowerPoint by Ivan (IvanStudios). There is no compiled code and no
VBA: every rule of the game is expressed with PowerPoint features — slide
hyperlinks, mouse-over actions, timed auto-advance and animation triggers.

The credits slide lists the original toolchain as an unmodified PowerPoint
2007 on Windows 7.

## Contents

- [Playing the game](#playing-the-game)
- [Repository layout](#repository-layout)
- [How the game works](#how-the-game-works)
- [Version history](#version-history)
- [Extracted source](#extracted-source)
- [Assets](#assets)
- [Known issues](#known-issues)
- [Editing the game](#editing-the-game)

## Playing the game

1. Open a deck in PowerPoint on Windows (2007 or later). The most complete
   build is `versions/beta/experimentalbeta_1.1.pptx`; the newest work is
   `versions/demos/v1.0/pre-release/predemo_v1.0.3.pptx`.
2. Start the slide show from the first slide (**F5**).
3. Use only the mouse. Do not press keys or click empty space to advance —
   that skips levels and breaks the intended flow.

Before playing, read [Known issues](#known-issues): the demo builds' **Exit**
button force-closes every running PowerPoint window, and some music will be
silent on any machine other than the author's.

## Repository layout

```
puzzlegame/
├── data/                         Raw art, music and sound effects
├── versions/
│   ├── test/TestBuild_1.pptx     First test build (2 slides)
│   ├── beta/
│   │   ├── experimentalbeta_1.0.pptx   33 slides
│   │   ├── experimentalbeta_1.1.pptx   59 slides
│   │   └── experimentalbeta_1.2.pptx   43 slides
│   ├── demos/v1.0/pre-release/
│   │   ├── predemo_v1.0.pptx     2 slides
│   │   ├── predemo_v1.0.1.pptx   3 slides
│   │   ├── predemo_v1.0.2.pptx   5 slides
│   │   └── predemo_v1.0.3.pptx   5 slides
│   ├── trailers/teasertrailer_demo1.pptx   4-slide teaser
│   └── announcements/
│       ├── discontinued.pptx     Project-discontinued notice
│       └── continued.pptx        Project-resumed notice
└── source/                       Extracted, readable source (generated)
    ├── extract_decks.py          Extraction script
    └── <deck path>/
        ├── game.md               Readable game logic per slide
        └── xml/                  Pretty-printed deck XML
```

## How the game works

PowerPoint provides four building blocks, and the game is built from them:

| Mechanic | PowerPoint feature | Example |
| --- | --- | --- |
| Buttons and menus | Click hyperlink to a slide (`ppaction://hlinksldjump`) | **Play** goes to the start slide |
| Maze walls | Mouse-over action (`hlinkHover`) | Touching a wall jumps to the "Defeated." slide |
| Level timer | Transition auto-advance (`advTm`) | A level advances to failure after 3–10 s |
| Scripted events | Animation triggers (`evt="onClick"` on a shape) | Clicking **Exit** slides in a **YES / CONFIRM?** prompt |

### Main menu

The title slide ("An simple puzzle game..?") has four buttons:

- **Play** — starts the first level.
- **Credits'N'Info** — credits slide.
- **Quit** — ends the slide show.
- **Bypass.** — a cheat shortcut into the later levels. Using it leads to the
  "Dangerland" trap and the "somebody's using developer mode" sequence.

### Levels

- **Mouse mazes.** Each level is one slide with a **Start** and a **Finish**
  shape. The walls carry mouse-over actions, so the cursor only has to touch a
  wall to lose. Losing shows the "Defeated." slide, which offers **Start**
  (retry) or a return to the menu. Larger levels have up to 25 hover walls.
- **Timed levels.** Some maze slides auto-advance after a few seconds. Not
  reaching **Finish** in time moves the player on to a fail or "STOP" slide.
- **Story beats.** Short auto-advancing slides ("It's not the end, yet.",
  "You have to go further... And further…") link the levels.
- **Keypad lock.** Two keypad slides each have ten digit buttons. Nine
  buttons go to "Incorrect!"; one advances. The hint slide shows **79**, and
  the code is 7 then 9.
- **Ending.** A "Thank you." slide with music, then back to the menu.

### Demo v1.0 (rewrite)

The pre-release demos restart the game with new art (city, train and rails
backgrounds), a new animated menu and a debug area:

1. Menu with **Play**, **Dev-only** and **Exit**. **Exit** animates in a
   **YES / CONFIRM?** prompt; **YES** runs `taskkill` on PowerPoint.
2. **Dev-only** opens the "DEBUG ROOM".
3. "DEBUG MAP" title card (auto-advances after 4 s).
4. A test maze in which 25 walls send the player back one slide on
   mouse-over.

**Play** has no action yet in the demo builds.

## Version history

The dates come from the date fields on the slides.

| Version | Date | Notes |
| --- | --- | --- |
| Experimental Beta 1.0 | 2023-04-16 | First playable game: menu, mazes, keypad lock, credits |
| Experimental Beta 1.1 | 2023-05-16 | Adds the developer-mode trap and "GET TROLLED" slides |
| Experimental Beta 1.2 | 2023-06-10 | Removes the troll slides; adds a "COMING SOON!" slide. Slides still read "1.1" |
| Test Build 1 | 2023-06-16 | Test build for the first demo; marked as having severe issues |
| Pre-demo v1.0 – v1.0.3 | 2023-06-18 | Rewrite with new menu, debug room and debug map |
| Teaser trailer | — | Unfinished; the last slide is a "Footage here" placeholder |
| Announcements | — | A "discontinued" notice, followed by a "continued" notice |

## Extracted source

Because the game lives inside `.pptx` files, `source/` holds a readable copy
of each deck generated by `source/extract_decks.py`.

- **`game.md`** lists every slide in show order: shapes and their text,
  CLICK and HOVER actions with the target slide number, auto-advance timers,
  linked or embedded audio, and which event starts each animation.
- **`xml/`** holds the deck's XML parts, pretty-printed. Images and audio are
  left out because the originals are in `data/` and inside each `.pptx`.

Shape names are in Russian because PowerPoint named them in the author's
locale (for example `Прямоугольник` = rectangle, `Лента лицом вверх` =
ribbon shape, `Управляющая кнопка: далее` = action button "next").

To regenerate after editing a deck:

```bash
pip install defusedxml
```

```bash
python3 source/extract_decks.py
```

The script only reads the decks. It overwrites any earlier output in
`source/`.

## Assets

All raw assets are in `data/`.

- **Backgrounds:** `predemo_background.png`, `predemo_city_bg.png`,
  `predemo_train_bg.png`, `predemo_rails_bg.png`, `predemo_devonlybg.png`,
  `predemo_playselectbg.png`, `menu_pre-release.png`
- **Branding:** `logo1.png`, `IvanStudios_Logo_BlackBG.png`,
  `IvanStudios_Logo_WhiteBG.png`
- **Characters and UI:** `sadface_*.png`, `radio_*.png`, `cursor.PNG`,
  `caughtexploiting.PNG`
- **Music:** `predemo_world.mp3`, `devonly_music.mp3`,
  `predemo_debugmap_intro.mp3`, `predemo_debugmap_music.mp3`,
  `predemo_tutorial.mp3`, `predemo_playstart.mp3`, `trailermusic.mp3`,
  `trailermusic2.mp3`
- **Sound effects:** `Victory.wav`, `Death.wav`

Some files are not referenced by name in any deck, so they are most likely
prepared for future builds: `predemo_tutorial.mp3`, `predemo_playstart.mp3`,
`trailermusic2.mp3`, `predemo_devonlybg.png`, `predemo_playselectbg.png`,
`menu_pre-release.png`, `cursor.PNG`, `caughtexploiting.PNG`,
`IvanStudios_Logo_WhiteBG.png`, `sadface_devmode.png`, `sadface_happy.png`
and the inactive/dev-mode `radio_*.png` images. (PowerPoint does not always
record an image's file name, so an image may be embedded without being listed.)

## Known issues

1. **Exit force-closes PowerPoint.** In every demo build, **Exit → YES** runs
   `C:\Windows\System32\taskkill.exe /f /im POWERPOINT.exe /t`. This closes
   *all* PowerPoint windows, including unrelated presentations, without
   saving. PowerPoint shows a security warning before it runs the command.
2. **Music is linked, not embedded.** The demos link audio from
   `C:\Users\Гость\Desktop\Weird Engines\PowerPoint games\data\puzzlegame\`,
   and the betas link music from a local Steam install of the Half-Life 2
   beta. On any other machine those tracks are silent. Embedded `.wav` sound
   effects still play.
3. **Third-party music.** The betas use Half-Life 2 beta soundtrack files,
   which are copyrighted and cannot be redistributed with the game.
4. **Hard-coded slide numbers.** Every jump targets a fixed slide. Inserting,
   deleting or reordering slides silently changes where buttons and walls
   lead, so re-check each link after any structural edit.
5. **Leftovers from copy and paste.** Beta 1.2 is labelled "Experimental Beta
   (1.1)" (one slide says "1.0"), the title menu is duplicated on several
   slides, and some slides are unused.
6. **Keyboard advance.** Several slides still allow click/key advance, so
   pressing a key can skip a level.
7. **Offensive content.** The last slide of
   `versions/announcements/continued.pptx` contains a racial slur. Remove it
   before sharing that deck (it also appears in that deck's `game.md`).

## Editing the game

- Edit the `.pptx` files in PowerPoint; `source/` is a generated, read-only
  view.
- Embed audio rather than linking it (**Insert → Audio → Audio on My PC**,
  with linking off) so the deck works on other machines.
- Replace the `taskkill` action with **Hyperlink to: End Show**.
- After any add, delete or move of slides, run
  `python3 source/extract_decks.py` and check each `game.md` for jumps that
  now point at the wrong slide.
