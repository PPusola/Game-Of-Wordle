# Wordle 175

A fully playable Wordle clone — available as both a **3D interactive web game** and a **Python CLI version**.

Word list is sourced from [tabatkins/wordle-list](https://github.com/tabatkins/wordle-list) (~14k valid 5-letter words). The browser fetches it on load; the CLI downloads and caches it locally, refreshing automatically once a week.

---

## Play in the browser

Open `index.html` in any modern browser.

- 3D tile-flip animations on reveal
- Staggered colour feedback — green / yellow / grey
- On-screen keyboard with live colour state
- Shake on invalid guess, bounce animation on win
- "How to play" guide built in
- Fully responsive — works on desktop and mobile

## Play in the terminal

Requires Python 3. No extra packages needed.

```bash
python wordle.py
```

The word list is downloaded on first run and cached to `words_cache.txt`. It refreshes automatically if the cache is older than 7 days.

---

## File overview

| File | Purpose |
|---|---|
| `index.html` | 3D browser game (self-contained HTML/CSS/JS) |
| `wordle.py` | CLI game — input validation, colour feedback, win/lose logic |
| `dictionary.py` | `ScrabbleDict` class — loads and validates words from a text file |

---

## How the colour logic works

Duplicate letters are handled correctly via a two-pass algorithm:

1. **Pass 1** — mark exact matches (green) and consume those letters from the target
2. **Pass 2** — check remaining letters against unconsumed target letters for yellow

This matches the behaviour of the original NYT Wordle.
