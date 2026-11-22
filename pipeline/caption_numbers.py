"""Turn spoken numbers in words.json into digits for captions ("Nineteen fifty-six." -> "1956.", "Six a.m." -> "6 AM").
usage: python3 pipeline/caption_numbers.py STORY_DIR   (edits STORY_DIR/words.json in place; times are kept)"""
import json, os, re, sys

PHRASES = [  # (spoken words, caption)
    (["Nineteen", "fifty-six."], "1956."), (["Nineteen", "seventy-five."], "1975."), (["Two", "thousand", "and", "one."], "2001."),
    (["Twenty", "twenty-six."], "2026."), (["twenty", "twenty-six"], "2026"), (["eighteen", "eighty-five,"], "1885,"),
    (["nineteen", "ninety-three"], "1993"), (["Six", "a.m."], "6 AM."), (["Nine", "a.m."], "9 AM."), (["One", "p.m."], "1 PM."),
    (["Five", "p.m."], "5 PM."), (["Six", "p.m."], "6 PM."), (["five", "fifty-nine..."], "5:59..."), (["Six", "o'clock."], "6:00."),
]


def main(story):
    p = os.path.join(story, "words.json"); w = json.load(open(p)); out, i = [], 0
    while i < len(w):
        for spoken, cap in PHRASES:
            n = len(spoken)
            if [x[0] for x in w[i:i + n]] == spoken:
                out.append([cap, w[i][1], w[i + n - 1][2]]); i += n; break
        else:
            out.append(w[i]); i += 1
    json.dump(out, open(p, "w")); print(story, len(w), "->", len(out), "words")


if __name__ == "__main__":
    for s in sys.argv[1:]: main(s)
