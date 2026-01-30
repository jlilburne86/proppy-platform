#!/usr/bin/env python3
import os, sys, json, time, urllib.request, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONF = os.path.join(ROOT, 'data', 'google-places.json')
OUT = os.path.join(ROOT, 'data', 'google-reviews.json')


def load_cfg():
    with open(CONF, 'r', encoding='utf-8') as f:
        return json.load(f)


def fetch_details(place_id: str, api_key: str, language: str):
    base = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'name,rating,user_ratings_total,reviews',
        'key': api_key,
        'language': language,
    }
    url = base + '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode('utf-8', 'ignore'))


def main():
    if not os.path.exists(CONF):
        print(f'Missing config: {CONF}', file=sys.stderr)
        sys.exit(2)
    cfg = load_cfg()
    place_id = (cfg.get('place_id') or '').strip()
    api_env = (cfg.get('api_key_env') or 'GOOGLE_PLACES_API_KEY').strip()
    language = (cfg.get('language') or 'en-AU').strip()
    min_rating = int(cfg.get('min_rating') or 3)
    max_reviews = int(cfg.get('max_reviews') or 20)
    api_key = os.getenv(api_env, '').strip()
    if not place_id:
        print('Set place_id in data/google-places.json', file=sys.stderr)
        sys.exit(2)
    if not api_key:
        print(f'Set {api_env} in environment with a valid Google Places API key', file=sys.stderr)
        sys.exit(2)

    data = fetch_details(place_id, api_key, language)
    if data.get('status') != 'OK':
        print('Google Places error:', data.get('status'), data.get('error_message'), file=sys.stderr)
        sys.exit(1)

    result = data.get('result') or {}
    reviews = result.get('reviews') or []
    # Filter and map
    out_reviews = []
    for r in reviews:
        try:
            if float(r.get('rating', 0)) < min_rating:
                continue
        except Exception:
            continue
        out_reviews.append({
            'author_name': r.get('author_name'),
            'author_url': r.get('author_url'),
            'profile_photo_url': r.get('profile_photo_url'),
            'rating': r.get('rating'),
            'relative_time_description': r.get('relative_time_description'),
            'time': r.get('time'),
            'text': r.get('text'),
            'original_language': r.get('original_language'),
        })
        if len(out_reviews) >= max_reviews:
            break

    payload = {
        'last_updated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'place': {
            'name': result.get('name'),
            'rating': result.get('rating'),
            'user_ratings_total': result.get('user_ratings_total')
        },
        'reviews': out_reviews
    }
    with open(OUT, 'w', encoding='utf-8') as w:
        json.dump(payload, w, ensure_ascii=False, indent=2)
    print(f'Wrote {OUT} with {len(out_reviews)} reviews (rating ≥ {min_rating})')


if __name__ == '__main__':
    main()

