Proppy Assessment API (Cloudflare Worker)

Endpoints
- POST /api/assessment/draft -> { draft_id, resume_token, expires_at }
- PATCH /api/assessment/draft/:id -> { ok: true }
- POST /api/assessment/submit -> { engagement_id, priority, next_action }
- GET /api/listing/preview?url=... -> { title, image, site, ok }

Storage
- KV namespace: ASSESS_KV (bind in wrangler.toml)

Local dev
- npm i -g wrangler
- cd cf-worker
- wrangler dev

Publish
- wrangler publish
- Set KV binding and routes in Cloudflare dashboard if not set by wrangler.

Config (wrangler.toml)
- PUBLIC_BASE_URL: origin base used for resume link construction
- ALLOWED_PREVIEW_DOMAINS: comma-separated domains allowed in preview (default: realestate.com.au, domain.com.au)

