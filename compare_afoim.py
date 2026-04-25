import urllib.request
import difflib
from pathlib import Path
files = [
    ('src/layouts/Layout.astro','https://raw.githubusercontent.com/afoim/fuwari/main/src/layouts/Layout.astro'),
    ('src/layouts/MainGridLayout.astro','https://raw.githubusercontent.com/afoim/fuwari/main/src/layouts/MainGridLayout.astro'),
    ('src/styles/transition.css','https://raw.githubusercontent.com/afoim/fuwari/main/src/styles/transition.css'),
    ('astro.config.mjs','https://raw.githubusercontent.com/afoim/fuwari/main/astro.config.mjs'),
]
with open('diff_afoim.txt', 'w', encoding='utf-8') as out:
    for local, url in files:
        out.write('--- ' + local + ' ---\n')
        try:
            remote = urllib.request.urlopen(url, timeout=20).read().decode('utf-8').splitlines()
        except Exception as e:
            out.write(f'ERROR fetching {url}: {e}\n')
            continue
        path = Path(local)
        if not path.exists():
            out.write(f'MISSING local {local}\n')
            continue
        local_lines = path.read_text('utf-8').splitlines()
        d = list(difflib.unified_diff(remote, local_lines, fromfile='remote/'+local, tofile='local/'+local, n=3))
        for line in d[:180]:
            out.write(line + '\n')
        if len(d) > 180:
            out.write('... %d more lines ...\n' % (len(d)-180))
