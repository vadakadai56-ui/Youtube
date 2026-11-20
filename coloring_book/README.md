# Cozy Christmas Critters: KDP colouring book

- `patterns.py`: code-drawn mandala, snowflake and ornament pages (vector, original).
- `build.py`: builds `output/interior.pdf` (8.5x11, no bleed, blank backs) and `output/cover.pdf` (KDP wrap, white paper).
- Put animal line-art pages (PNG/JPG, made in Canva) into `animals/`, then run `python3 build.py`.
  They alternate with the pattern pages; the first animal page also goes on the front cover.
