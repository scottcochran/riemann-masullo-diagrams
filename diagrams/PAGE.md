# The page behind the cards

In the light theme, the page of every poster is `#e8e8e8`, 90.8% white. The rule is riemann-diagrams' (its
`diagrams/PAGE.md`, which says why a grey and not white): the page matches the mean luminance of what sits on it.
PLAN.md, rule 7, asks for it to be measured again on this repository's first poster, since a page of mostly tables
and code is not a page of mostly cards.

## The measurement

`tools/measure-page.py`, copied from riemann-diagrams at f87256e, on 2026.11.25, with the page still at
riemann-diagrams' `#eeeeee`. It renders the poster twice at 1700 pixels wide with `rsvg-convert`, once as it is
and once with the page painted magenta as a mask, and averages the relative luminance of the pixels that are not
page.

| Poster | Pixels | Page | Content | Mean relative luminance of the content | As an sRGB grey |
|---|---|---|---|---|---|
| M1, the one the rule names | 1700 × 2539 | 63.4% | 36.6% | 0.8037 | 231.6, 90.8% white, `#e8e8e8` |
| M2, for comparison | 1700 × 2471 | 41.7% | 58.3% | 0.8043 | 231.7, 90.9% white, `#e8e8e8` |
| M3, for comparison | 1700 × 2040 | 79.1% | 20.9% | 0.7315 | 222.1, 87.1% white, `#dedede` |

The `page` token in `diagrams/src/lib.py` was set to M1's value. M2 agrees. M3 is darker: most of its content is
the dots, at full colour. It keeps the common page, since the token is one for all posters.

To measure again: `uv run --with pillow python tools/measure-page.py diagrams/M1-floor-<date>.svg --width 1700`
(needs `rsvg-convert`). Not checked by the build: a change to the posters can move the mean without failing.
