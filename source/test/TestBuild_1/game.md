# test/TestBuild_1

2 slides. Slide numbers are show order.

## Slide 1 — `slide1.xml`
- **Прямоугольник 4** — "This is a test build for first demo. / For some reason, this version has severe issues. / I’m not responsible for that. / Either, I don’t  / wanna /  fix issues."
- **Дата 1** — "6/16/2023 3:56:35 PM"
- **Нижний колонтитул 2** — "Test version, expect several issues."
- **Номер слайда 3** — "1"
- **Прямоугольник 5** — "I understand." — CLICK: go to slide 2
- **Прямоугольник 6** — "Didn’t understand." — CLICK: END SHOW

## Slide 2 — `slide2.xml`
- **Рисунок 5** — [predemo_background.png]
- **Дата 1** — "6/16/2023 3:56:35 PM"
- **Нижний колонтитул 2** — "Test version, expect several issues."
- **Номер слайда 3** — "2"
- **predemo_world.mp3** — CLICK: play media — MEDIA: LINKED predemo_world.mp3
- Animations:
  - on slide load -> play/stop media: 'predemo_world.mp3'
  - on slide load -> motion path (loops): 'Рисунок 5'
  - on slide load -> disappear: 'Прямоугольник 6'
