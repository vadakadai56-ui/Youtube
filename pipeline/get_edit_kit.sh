#!/bin/sh
# Fetch the owner's Creator Edit Kit (SFX, 2 original music tracks, fonts, white transitions) from their Drive into
# assets/edit-kit/ (git-ignored: the kit's licence says don't resell it, and this repo is public). Run once per session.
set -e
D=assets/edit-kit; [ -d "$D/01 SFX" ] && exit 0
T=$(mktemp -d); curl -sSfL -o "$T/kit.zip" "https://drive.usercontent.google.com/download?id=1qW4MIJagKYqbntqmACVrL8w7_JbqsC6l&export=download&confirm=t"
mkdir -p "$D"; python3 -I -c "
import sys, zipfile; z = zipfile.ZipFile(sys.argv[1])
for i in z.infolist():
    n = i.filename.split('/', 1)[-1]
    if n.startswith(('01 ', '02 ', '03 Fonts & Captions/Fonts', '05 ')) and '..' not in n and not i.is_dir():
        p = sys.argv[2] + '/' + n; import os; os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(z.read(i))
" "$T/kit.zip" "$D"; rm -rf "$T"; echo "edit kit in $D"
