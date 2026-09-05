from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='  .mini-card{width:82vw;}\n'
assert old in s
p.write_text(s.replace(old,'',1),encoding='utf-8')
