# Proppy Backend Infrastructure Assessment

**Date:** 22 January 2026
**Status:** ⚠️ **CRITICAL GAP IDENTIFIED**

## Executive Summary

**Current State:** The Proppy website is a **fully static HTML/CSS/JavaScript site** with **no backend, database, or content management system (CMS)**.

**User Requirement:** Backend login with ability to edit and manage:
- Articles (markdown/HTML content)
- Resources page
- Results page
- Other content without requiring code/terminal access

**Current Reality:** ❌ **NO BACKEND EXISTS** - Content editing currently requires:
- Command line access
- Python script execution
- Markdown file editing
- Git/version control knowledge
- Manual HTML regeneration

---

## Current Architecture

### What Exists ✅
1. **Static HTML Pages** - All pages are pre-generated HTML files
2. **Markdown Articles** - 46 articles stored as `.md` files in `/articles/`
3. **Python Build Scripts** - Convert markdown to HTML
4. **Development Server** - `devserver.py` (local preview only, no admin panel)
5. **No Database** - All content stored in files
6. **No API** - No server-side endpoints
7. **No Authentication** - No user login system

### What Does NOT Exist ❌
1. **Admin Panel/Dashboard** - No web interface for content editing
2. **Database** - No MySQL, PostgreSQL, MongoDB, etc.
3. **Backend Server** - No Node.js, Python Flask/Django, PHP server
4. **User Authentication** - No login system
5. **WYSIWYG Editor** - No visual content editor
6. **Media Management** - No file upload system
7. **Content API** - No RESTful or GraphQL endpoints

### Current Content Editing Workflow
```bash
# Extremely technical - requires terminal access
cd /Users/boo2/Desktop/proppy
source .venv/bin/activate

# Edit article markdown file manually
nano articles/my-article.md

# Regenerate HTML
python3 tools/convert-articles-to-html.py
python3 tools/generate-articles.py

# Deploy to production (FTP upload or git push)
```

**This is NOT sustainable for non-technical editors.**

---

## Recommended Solutions

### Option 1: Headless CMS (FASTEST, RECOMMENDED) ⭐

**Use a headless CMS that generates static HTML:**

#### A. **Netlify CMS** (Free, Open Source)
- Add a `/admin` panel to existing site
- Git-based (commits to repository)
- Markdown editing with live preview
- No backend server needed
- Works with static sites

**Pros:**
- No server/database required
- Free forever
- Works with existing workflow
- GitHub-based authentication

**Cons:**
- Requires GitHub account for editors
- No real-time collaboration
- Limited media library

**Implementation Time:** 4-6 hours

#### B. **Decap CMS** (formerly Netlify CMS, modernized)
- Same as Netlify CMS but actively maintained
- Better UI/UX
- Improved performance

**Implementation Time:** 4-6 hours

#### C. **Tina CMS** (Modern, Visual)
- Visual editing directly on pages
- Git-based like Netlify CMS
- Better editor experience
- Free tier available

**Pros:**
- Best editor experience
- Visual editing (WYSIWYG-like)
- Modern interface

**Cons:**
- Requires Next.js migration (major refactor)
- Or use with static site builder

**Implementation Time:** 8-12 hours (static) or 3-5 days (Next.js migration)

---

### Option 2: Traditional CMS Backend (FULL-FEATURED)

#### A. **Strapi** (Headless CMS with Database)
- Node.js backend + PostgreSQL/MySQL
- Full admin panel
- User management
- Media library
- RESTful + GraphQL API

**Architecture:**
```
Strapi Backend (admin.proppy.com.au)
├── PostgreSQL database
├── Admin panel at /admin
├── API endpoints
└── Generates JSON for frontend

Static Frontend (proppy.com.au)
├── Fetches content from Strapi API
├── Builds HTML at deploy time
└── Hosted on Netlify/Vercel
```

**Pros:**
- Full CMS experience
- Multi-user support
- Rich media management
- Workflow/publishing features

**Cons:**
- Requires server hosting ($10-50/month)
- Requires database setup
- More complex maintenance

**Implementation Time:** 2-3 weeks

#### B. **WordPress Headless** (Keep WordPress, New Frontend)
- Keep WordPress admin panel
- Replace frontend with static HTML
- Use WordPress REST API
- Familiar interface for editors

**Pros:**
- WordPress admin (familiar to most)
- Existing plugins/themes
- Proven stability

**Cons:**
- PHP/MySQL hosting required
- WordPress security maintenance
- Defeats purpose of leaving WordPress

**Implementation Time:** 1-2 weeks

---

### Option 3: Low-Code Solutions

#### A. **Webflow CMS**
- Visual editor + CMS
- No code required
- Hosting included
- Designer-friendly

**Pros:**
- Non-technical editors
- Visual design + content editing
- Fast setup

**Cons:**
- Vendor lock-in
- Expensive ($29-74/month)
- Migration effort required

**Implementation Time:** 2-3 weeks (full migration)

#### B. **Sanity.io**
- Headless CMS
- Excellent editor experience
- Real-time collaboration
- GraphQL API

**Pros:**
- Modern, fast
- Great UX
- Free tier (100K requests/month)

**Cons:**
- Requires frontend rebuild
- Learning curve

**Implementation Time:** 2-3 weeks

---

## Comparison Matrix

| Solution | Cost | Setup Time | Technical Skill Required | Maintenance | Recommendation |
|----------|------|------------|-------------------------|-------------|----------------|
| **Netlify/Decap CMS** | Free | 4-6 hours | Low | Low | ⭐ **Best for your needs** |
| **Tina CMS** | Free-$29/mo | 1-2 weeks | Medium | Low | Good alternative |
| **Strapi** | $10-50/mo | 2-3 weeks | Medium-High | Medium | If need full CMS |
| **WordPress Headless** | $10-30/mo | 1-2 weeks | Low | Medium | If must keep WordPress |
| **Webflow** | $29-74/mo | 2-3 weeks | None | None | Expensive, overkill |
| **Sanity.io** | Free-$99/mo | 2-3 weeks | Medium | Low | Modern, but complex |

---

## Immediate Recommendation: Netlify/Decap CMS

**Why this is the best fit:**

1. **Minimal disruption** - Works with existing markdown/HTML workflow
2. **Free forever** - No hosting costs
3. **Git-based** - All changes tracked in version control
4. **No server required** - Static site remains static
5. **Quick implementation** - 4-6 hours to add admin panel
6. **Familiar interface** - Similar to WordPress admin

### How It Works:

```
Editor logs in at proppy.com.au/admin
├── GitHub OAuth authentication
├── Visual markdown editor
├── Preview before publish
└── Saves to Git → triggers rebuild → site updates

No database, no server, just files + Git
```

### What You'll Get:

✅ **Admin panel at `/admin`**
✅ **Login with GitHub account**
✅ **Visual markdown editor** (no code required)
✅ **Live preview** before publishing
✅ **Media upload** (images for articles)
✅ **Draft/publish workflow**
✅ **Multi-user support** (invite editors)
✅ **Version history** (Git commits)
✅ **No hosting costs**

### What You Won't Get:

❌ User comments (need separate service like Disqus)
❌ E-commerce (need Shopify/Stripe integration)
❌ Complex workflows (need full CMS like Strapi)
❌ Real-time collaboration (Tina CMS has this)

---

## Implementation Plan: Netlify/Decap CMS

### Phase 1: Setup (2 hours)
1. Install Decap CMS
2. Configure content collections (articles, authors, etc.)
3. Set up GitHub OAuth
4. Deploy admin panel to `/admin`

### Phase 2: Content Configuration (2 hours)
1. Define article schema (title, description, category, etc.)
2. Configure markdown editor
3. Set up media library
4. Create preview templates

### Phase 3: Testing (1 hour)
1. Test article creation
2. Test editing existing articles
3. Test publishing workflow
4. Train editor(s)

### Phase 4: Documentation (1 hour)
1. Write editor guide
2. Document workflow
3. Create troubleshooting guide

**Total Time:** 6 hours
**Cost:** $0

---

## Alternative: Full CMS with Strapi (If Budget Allows)

If you need more features (multi-user permissions, workflow, media management, etc.), **Strapi** is the best option.

### Requirements:
- VPS/Cloud server ($10-50/month)
- PostgreSQL database
- Node.js hosting
- Domain for admin panel (admin.proppy.com.au)

### Features You'll Get:
✅ Full admin panel
✅ User roles & permissions
✅ Media library with CDN
✅ Draft/publish/schedule
✅ RESTful + GraphQL API
✅ Webhook triggers
✅ Email notifications
✅ Audit logs

### Cost Breakdown:
- Hosting: $10-50/month (DigitalOcean, Render, Railway)
- Database: Included or $5-10/month
- CDN: Free (Cloudflare) or $5-20/month
- **Total:** $15-80/month

---

## Decision Framework

**Choose Netlify/Decap CMS if:**
- Budget is tight ($0)
- 1-3 editors
- Content is mostly text/markdown
- Don't need complex workflows
- Want simplicity

**Choose Strapi if:**
- Budget allows ($15-50/month)
- 5+ editors with different permissions
- Need media management
- Need workflow (draft → review → publish)
- Want room to scale

**Choose WordPress Headless if:**
- Editors refuse to leave WordPress
- Already have WordPress hosting
- Need plugin ecosystem

---

## Next Steps

### Option A: Implement Netlify/Decap CMS (Recommended)

I can implement this in **6 hours** with the following deliverables:

1. `/admin` panel accessible at `proppy.com.au/admin`
2. GitHub OAuth login
3. Visual markdown editor for articles
4. Media upload functionality
5. Preview before publish
6. Editor documentation

**Ready to proceed?** I can start immediately.

### Option B: Implement Strapi Backend

This requires:
1. Server provisioning (DigitalOcean/Render/Railway)
2. Database setup (PostgreSQL)
3. Strapi installation & configuration
4. Frontend API integration
5. Deployment automation

**Timeline:** 2-3 weeks
**Cost:** $15-50/month recurring

### Option C: Evaluate Other Solutions

I can create detailed implementation plans for:
- Tina CMS
- Sanity.io
- WordPress Headless
- Custom solution

---

## Critical Question

**Do you want to proceed with Netlify/Decap CMS implementation?**

This will give you a working admin panel in 6 hours with zero hosting costs.

**Or do you prefer a different solution?** Let me know your:
- Budget
- Number of editors
- Required features
- Timeline

I'll tailor the implementation plan accordingly.
