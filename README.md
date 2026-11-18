# The World — 18 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261118)

A newspaper front page that sums up 18 November 2026 in one image:
six verified stories, drawn with Pillow and nothing else.

## The six stories

1. **Quad meets in Manila** — Trump in Manila for Quad leaders' talks,
   first stop of a three-day Asia trip ending in China; APEC leaders meet
   in Shenzhen 18–19 Nov, and Xi, Trump and Putin meet there on Thursday.
2. **Britain sanctions settlement firms** — asset freezes and director
   disqualifications for eight Israeli settlement firms and the Tzav 9
   activist group, announced by Foreign Secretary Ed Miliband to protect
   the two-state solution.
3. **Canada–China extend trade deals** — Xi meets Carney in Shenzhen;
   China cuts tariffs on about C$400m of Canadian pork and seafood, and
   Canada extends steel and aluminium remission measures by two years.
4. **Cyclone Akvan bears down** — a Severe Cyclonic Storm in the Bay of
   Bengal, forecast to make landfall near noon on 20 Nov with winds of
   120–130 km/h, gusting to 145 km/h.
5. **Dhoni calls time on IPL** — MS Dhoni retires from playing after five
   IPL titles and 5,439 runs, and becomes Chennai Super Kings mentor
   from 2027.
6. **Amazon bets $7bn on green India** — $7bn in renewable energy by
   2030, on top of $4bn already contracted, including four new wind and
   solar projects totalling 934 MW.

## How to run it

```sh
python3 gen_image.py   # renders entry.png (1024x1024, deterministic)
```

`main.ts` copies `entry.png` to the output folder (defaults to
`/output`, override with `MAKEFUN_OUTPUT_DIR`):

```sh
node main.ts
```

## Licence

MIT — see [LICENSE](LICENSE).
