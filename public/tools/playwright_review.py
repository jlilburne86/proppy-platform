from pathlib import Path
import re
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000"
OUT = Path("/Users/boo2/Desktop/proppy/site-audit/playwright")
OUT.mkdir(parents=True, exist_ok=True)

def words_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={'width': 1366, 'height': 900})
        page = ctx.new_page()

        # Resources page checks
        page.goto(f"{BASE}/resources.html")
        page.wait_for_load_state('domcontentloaded')
        page.screenshot(path=str(OUT/"resources.png"))

        # Validate cards have: thumbnail, tags, score-mini
        cards = page.locator("article")
        count = cards.count()
        print(f"Found {count} resource cards")
        assert count > 0, "No resource cards found"

        hrefs = []
        max_check = min(12, count)
        for idx in range(max_check):
            art = cards.nth(idx)
            has_thumb = art.locator(".card-thumb img").count() > 0
            has_tags = art.locator(".tag-list .tag").count() > 0
            has_score = art.locator(".score-mini .score-grid").count() > 0
            cta = art.locator(".mt-auto a").first
            href = cta.get_attribute("href") if cta.count() > 0 else None
            hrefs.append(href)
            print(f"Card {idx+1}: thumb={has_thumb} tags={has_tags} score={has_score} href={href}")

        # Visit a handful of article pages to validate structure
        checked = 0
        for href in filter(None, hrefs):
            if not href.startswith("/articles/"):
                continue
            url = BASE + href
            page.goto(url)
            page.wait_for_load_state('domcontentloaded')
            page.screenshot(path=str(OUT/f"article_{checked+1}.png"), full_page=True)

            # Required elements (use locator to avoid adoption errors)
            assert page.locator("main h1").count() > 0
            assert page.locator(".outlook-badge").count() > 0
            assert page.locator(".hero-img img").count() > 0
            assert page.locator(".score-grid").count() > 0
            assert page.locator("details summary").filter(has_text="How to read these tiles").count() > 0
            assert page.locator("details summary").filter(has_text="In this article").count() > 0

            # Word count check
            main_txt = page.inner_text("main")
            wc = words_count(main_txt)
            print(f"{url} words={wc}")
            assert wc >= 1000, f"Article under 1000 words: {wc}"

            checked += 1
            if checked >= 6:
                break

        print(f"Validated {checked} article pages")
        ctx.close()
        browser.close()

if __name__ == "__main__":
    main()
