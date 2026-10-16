import re, sys
src, out = sys.argv[1], sys.argv[2]
text = open(src).read()
parts = re.split(r'(?m)^(?=## \d+\. )', text)
sections = {}
for p in parts[1:]:
    num = int(re.match(r'## (\d+)\.', p).group(1))
    sections[num] = p.rstrip().rstrip('-').rstrip() + '\n'

PAGES = [  # file, title, section numbers
    ('getting-started.md', 'Getting started', [1, 2, 3]),
    ('runtime.md', 'Runtime API', [4, 5, 6, 7, 8, 9]),
    ('audio-studio.md', 'Audio Studio', [10]),
    ('audio-debug.md', 'Audio Debug', [11]),
    ('ffmpeg.md', 'FFmpeg (optional)', [12]),
    ('demo.md', 'Demo scenes', [13]),
    ('performance.md', 'Performance and recipes', [14, 15]),
    ('limitations.md', 'Limitations and tests', [16, 17]),
]
owner = {n: f for f, _, ns in PAGES for n in ns}
owner[18] = '../support.md'

def fix_links(body, page):
    def repl(m):
        anchor = m.group(1)
        num = int(re.match(r'(\d+)-', anchor).group(1))
        target = owner[num]
        return f'(#{anchor})' if target == page else f'({target}#{anchor})'
    return re.sub(r'\(#(\d+-[a-z0-9-]+)\)', repl, body)

for f, title, nums in PAGES:
    body = '\n'.join(sections[n] for n in nums)
    body = fix_links(body, f)
    open(f'{out}/{f}', 'w').write(f'# {title}\n\n' + body)
print('ok', sorted(sections))
