import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')
IDX = os.path.join(ROOT, 'index.html')

def remove_all_pages_block(txt: str) -> str:
    # Remove block inserted by ALL_PAGES_SECTION markers if present
    txt = re.sub(r'<!-- ALL_PAGES_SECTION_START -->[\s\S]*?<!-- ALL_PAGES_SECTION_END -->\n?', '', txt)
    # Also remove any Site Map list section we might have appended without markers by matching a conservative pattern
    txt = re.sub(r'<section[^>]*>\s*<div[^>]*>\s*<div class="text-center mb-6">[\s\S]*?The Platform[\s\S]*?</section>', lambda m: m.group(0), txt)
    return txt

def move_platform_section(txt: str) -> str:
    # Identify the platform showcase section by its badge text
    plat_m = re.search(r'<section[\s\S]*?<span[^>]*>\s*<span[^>]*>apps</span>\s*The Platform[\s\S]*?</section>', txt)
    if not plat_m:
        return txt
    platform = plat_m.group(0)
    # Remove it from current location
    txt_wo = txt[:plat_m.start()] + txt[plat_m.end():]
    # Find main open/close and insert right after the first section inside <main>
    main_open = re.search(r'<main[^>]*>', txt_wo, flags=re.I)
    main_close = re.search(r'</main>', txt_wo, flags=re.I)
    if not main_open or not main_close:
        return txt
    after_main = main_open.end()
    inner = txt_wo[after_main:main_close.start()]
    first_sec = re.search(r'<section[\s\S]*?</section>', inner, flags=re.I)
    insert_at = after_main + (first_sec.end() if first_sec else 0)
    new_txt = txt_wo[:insert_at] + '\n' + platform + '\n' + txt_wo[insert_at:]
    return new_txt

def main():
    txt = open(IDX, 'r', encoding='utf-8', errors='ignore').read()
    orig = txt
    txt = remove_all_pages_block(txt)
    txt = move_platform_section(txt)
    if txt != orig:
        with open(IDX, 'w', encoding='utf-8') as w:
            w.write(txt)
        print('Rearranged index.html flow and removed All Pages list (if present).')
    else:
        print('No changes made to index.html')

if __name__ == '__main__':
    main()
