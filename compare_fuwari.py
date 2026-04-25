import urllib.request
import difflib
from pathlib import Path

files = [
    ('src/layouts/Layout.astro','https://raw.githubusercontent.com/saicaca/fuwari/main/src/layouts/Layout.astro'),
    ('src/layouts/MainGridLayout.astro','https://raw.githubusercontent.com/saicaca/fuwari/main/src/layouts/MainGridLayout.astro'),
    ('src/styles/transition.css','https://raw.githubusercontent.com/saicaca/fuwari/main/src/styles/transition.css'),
    ('astro.config.mjs','https://raw.githubusercontent.com/saicaca/fuwari/main/astro.config.mjs'),
]

for local, url in files:
    print('---', local, '---')
    try:
        remote = urllib.request.urlopen(url, timeout=20).read().decode('utf-8').splitlines()
    except Exception as e:
        print(f'ERROR fetching {url}: {e}')
        continue
    path = Path(local)
    if not path.exists():
        print(f'MISSING local {local}')
        continue
    local_lines = path.read_text('utf-8').splitlines()
    d = list(difflib.unified_diff(remote, local_lines, fromfile='remote/'+local, tofile='local/'+local, n=3))
    for line in d[:120]:
        print(line)
    if len(d) > 120:
        print('... %d more lines ...' % (len(d)-120))
