"""Check all four design previews use complete local assets and real demo audio."""
from html.parser import HTMLParser
from pathlib import Path

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets=[]
        self.ids=[]
        self.audio=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag in {'script','audio','source','img'} and 'src' in a:self.assets.append(a['src'])
        if tag=='audio':
            assert 'autoplay' not in a
            self.audio.append(a)

root=Path(__file__).resolve().parents[1]/'design-directions'
for name in ['festival','cinema','laboratory','futurism']:
    path=root/name/'index.html'
    text=path.read_text(encoding='utf-8-sig')
    p=Page();p.feed(text)
    assert len(p.ids)==len(set(p.ids)),name+' duplicate ids'
    assert len(p.audio)==2,name+' requires two listening examples'
    assert all(not s.startswith(('http:','https:','//')) and (path.parent/s).is_file() for s in p.assets),name+' missing local asset'
    assert 'Yeldar' in text and 'Aisha' in text
    assert 'prefers-reduced-motion' in text
print('PASS: four offline previews, two audio examples each, unique IDs, credits and reduced-motion support')
