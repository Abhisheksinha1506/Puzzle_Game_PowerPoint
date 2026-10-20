# demos/v1.0/pre-release/predemo_v1.0

2 slides. Slide numbers are show order.

## Slide 1 — `slide1.xml`
- Click-to-advance disabled
- **Рисунок 5** — [predemo_background.png]
- **Дата 1** — "6/18/2023 2:13:16 PM"
- **predemo_world.mp3** — CLICK: play media — MEDIA: LINKED predemo_world.mp3
- **Рисунок 7** — [IvanStudios_Logo_BlackBG.png]
- **Рисунок 8** — [logo1.png]
- **Лента лицом вверх 9** — "Play"
- **Лента лицом вверх 10** — "Dev-only" — CLICK: go to slide 2
- **Лента лицом вверх 11** — "Exit"
- **Прямоугольник 13** — "YES" — CLICK: RUN PROGRAM: "C:/Windows/System32/taskkill.exe" /f /im POWERPOINT.exe /t
- **TextBox 14** — "CONFIRM?"
- Animations:
  - on slide load -> play/stop media: 'predemo_world.mp3'
  - on slide load -> motion path (loops): 'Рисунок 5'
  - on slide load -> disappear: 'Прямоугольник 6'
  - on slide load -> emphasis (loops): 'Рисунок 5'
  - on slide load -> disappear: 'Рисунок 7'
  - on slide load -> appear: 'Рисунок 8'
  - on slide load -> motion path: 'Рисунок 8'
  - on slide load -> appear: 'Лента лицом вверх 9'
  - on slide load -> appear: 'Лента лицом вверх 10'
  - on slide load -> appear: 'Лента лицом вверх 11'
  - when 'Лента лицом вверх 11' is clicked -> motion path: 'Прямоугольник 12'
  - when 'Лента лицом вверх 11' is clicked -> motion path: 'Прямоугольник 13'
  - when 'Лента лицом вверх 11' is clicked -> motion path: 'TextBox 14'

## Slide 2 — `slide2.xml`
- **Дата 1** — "6/18/2023 2:13:18 PM"
- **devonly_music.mp3** — CLICK: play media — MEDIA: LINKED devonly_music.mp3
- Animations:
  - on slide load -> disappear: 'Прямоугольник 3'
  - on slide load -> play/stop media: 'devonly_music.mp3'
