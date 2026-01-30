#!/usr/bin/env python3
import os, re
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.abspath(os.path.dirname(__file__) + '/..')
PHONE = 'assets/placeholders/phone.svg'
TABLET = 'assets/placeholders/tablet.svg'

class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            self.parts.append(self.get_starttag_text()); return
        # Normalize attrs to dict preserving order
        attrs_list = attrs
        d = dict(attrs)
        src = d.get('src','')
        use_placeholder = False
        placeholder = PHONE
        if src and not src.startswith(('http://','https://','data:','//')):
            # local path
            p = src
            if p.startswith('/'):
                p = p[1:]
            target = os.path.join(ROOT, p)
            if not os.path.exists(target):
                # pick device type from filename hint
                s = src.lower()
                if any(k in s for k in ['tablet','ipad']):
                    placeholder = TABLET
                use_placeholder = True
        if use_placeholder:
            d['src'] = placeholder
            # rebuild attrs list replacing src in place
            attrs_list = [(k, placeholder if k=='src' else v) for (k,v) in attrs_list]
        # set lazy/decoding if not present
        if 'loading' not in d:
            attrs_list.append(('loading','lazy'))
        if 'decoding' not in d:
            attrs_list.append(('decoding','async'))
        # ensure class has nice image polish
        cls = d.get('class','')
        add = ' img-rounded img-shadow'
        if 'img-rounded' not in cls:
            cls = (cls + add).strip()
            # update or add class in attrs_list
            found=False
            for i,(k,v) in enumerate(attrs_list):
                if k=='class':
                    attrs_list[i]=(k,cls); found=True; break
            if not found:
                attrs_list.append(('class',cls))
        # reconstruct start tag
        s = '<img' + ''.join([f' {k}="{v}"' if v is not None else f' {k}' for k,v in attrs_list]) + '>'
        self.parts.append(s)
    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')
    def handle_startendtag(self, tag, attrs):
        # not expected
        self.handle_starttag(tag, attrs)
    def handle_data(self, data):
        self.parts.append(data)
    def handle_comment(self, data):
        self.parts.append(f'<!--{data}-->')
    def handle_decl(self, decl):
        self.parts.append(f'<!{decl}>')


def process_file(path):
    with open(path,'r',encoding='utf-8',errors='ignore') as f:
        html = f.read()
    p = ImgParser(); p.feed(html)
    out = ''.join(p.parts)
    if out != html:
        with open(path,'w',encoding='utf-8') as f:
            f.write(out)
        return True
    return False

if __name__ == '__main__':
    changed=0
    for name in os.listdir(ROOT):
        if name.endswith('.html'):
            if process_file(os.path.join(ROOT,name)):
                changed+=1
    print(f"Updated {changed} files with image placeholders or attrs.")
