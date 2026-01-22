# Proppy.com.au - Complete Site Audit Summary

**Audit Date:** January 16, 2026
**Site:** https://proppy.com.au
**Purpose:** Complete documentation of existing site for rebuild

---

## Executive Summary

Proppy.com.au is a property investment consultancy website built on WordPress with the Divi theme. The site features:
- 21+ main pages
- 12 market update articles
- 1+ investor guides
- 9 property showcase pages
- Extensive use of third-party integrations
- Heavy reliance on JavaScript animations and carousels

---

## Site Structure Overview

### Main Navigation Pages (21 pages)
1. **Homepage** (/) - Hero, value props, reviews, features ✅ DOCUMENTED
2. **About Us** (/about-us) - Company story, team, values ✅ DOCUMENTED
3. **Contact Us** (/contact-us) - Contact form, phone, email, location ✅ CAPTURED
4. **Pricing** (/pricing) - Service pricing information ✅ CAPTURED
5. **What We Do** (/what-we-do) - Service overview ✅ CAPTURED
6. **Why Choose Proppy** (/why-choose-proppy) - ⏳ TIMEOUT
7. **How We Do It** (/how-we-do-it) - Process explanation ⏳ TIMEOUT
8. **Properties We Source** (/properties-we-source) - ⏳ TIMEOUT
9. **Our Technology** (/our-technology) - Platform features ⏳ TIMEOUT
10. **Our Results** (/our-results) - Portfolio/case studies ⏳ TIMEOUT
11. **Get Started** (/get-started) - Onboarding page
12. **Reviews & Testimonials** (/reviews-and-customer-testimonials) - ✅ CAPTURED
13. **FAQ** (/faq) - Frequently asked questions ✅ CAPTURED
14. **Investor Assessment** (/investor-assessment-session) - Lead magnet
15. **Money Back Guarantee** (/money-back-guarantee) - Trust builder
16. **Privacy Policy** (/privacy-policy) - Legal
17. **Terms & Conditions** (/terms-and-conditions) - Legal
18. **Sitemap** (/sitemap) - Site map
19. **Investor Guides** (/investor-guides) - Article hub
20. **Market Updates** (/market-updates) - Article hub
21. **Investor Updates** (/investor-updates) - Article hub

### Content Pages

#### Market Updates (12 articles)
- August 2025
- July 2025
- June 2025
- May 2025
- April 2025
- March 2025
- February 2025
- January 2025
- December 2024
- November 2024
- October 2024
- September 2024

#### Investor Guides (1+ articles)
- "Should You Purchase an Investment Property Through a Trust?"

#### Property Showcase (9 properties)
- Hastings coastal gem
- Hastings waterfront
- Hastings high-yield
- Albion exceptional
- Reservoir rare
- Reservoir strong rental
- Seaford rare block
- Thornbury standout
- Richmond gem

---

## Key Brand Elements

### Contact Information
- **Phone:** 1300 122 914
- **Email:** hello@proppy.com.au
- **WhatsApp:** 0485 994 964
- **Address:** Level 3, 55 Collins St, Melbourne VIC 3000
- **Business Hours:** Monday – Friday, 9 AM – 5 PM (AEST)

### Social Media
- **Facebook:** https://www.facebook.com/proppy.com.au
- **Instagram:** https://www.instagram.com/proppy.com.au

### Trust Signals
- **Google Rating:** 5.0 stars (10+ reviews documented)
- **Experience:** 15+ years
- **Guarantee:** Money Back Guarantee prominently featured

---

## Design System

### Color Palette
- **Primary:** Blue (CTA buttons, links)
- **Background:** White/Light gray
- **Text:** Dark gray/Black
- **Accent:** Yellow/Gold (stars, ratings)
- **Status:** Needs extraction from CSS

### Typography
- **Font Family:** Sans-serif (specific font needs identification)
- **Hierarchy:** H1 (large, bold) → H2 → H3 → Body
- **Weights:** Regular, Medium, Bold

### Layout System
- **Max Width:** Appears to be container-based (needs measurement)
- **Grid:** Multi-column layouts (2-3 columns typical)
- **Spacing:** Consistent padding/margin system (needs measurement)

---

## Component Library (Identified)

### Navigation Components
1. **Header Navigation** - Logo + horizontal menu + CTA button
2. **Dropdown Menus** - Hover-activated submenus
3. **Mobile Menu** - Hamburger (assumption, needs verification)
4. **Top Banner** - Sticky notification bar

### Content Components
1. **Hero Section** - H1 + subheading + CTA + illustration
2. **Statistics Grid** - Animated counters (3-column)
3. **Feature Cards** - Icon + headline + description
4. **Problem/Solution Cards** - Expandable/hoverable
5. **Testimonial Carousel** - Slick slider with pagination
6. **Review Cards** - Google review format with stars
7. **CTA Sections** - Multiple variations throughout
8. **Three-Column Benefits** - Image + text + CTA
9. **Icon Grid** - 2x3 problem statement grid

### Form Components
1. **Contact Form** - Multi-field with reCAPTCHA
2. **Newsletter Signup** - Email capture (iframe embedded)
3. **Calendar Booking** - Appointment scheduler (iframe)
4. **Country Code Selector** - Phone input with dropdown

### Footer Components
1. **Icon Blocks** - 3-column feature highlights
2. **Footer Navigation** - 5-column link structure
3. **Newsletter Form** - Email signup
4. **Social Links** - Facebook, Instagram
5. **Copyright** - Legal text

### Interactive Elements
1. **Chat Widget** - Floating bottom-right button
2. **Hover States** - Button and link interactions
3. **Scroll Animations** - GSAP-powered reveals
4. **Carousel Navigation** - Arrows + pagination dots
5. **Accordion/Expandable** - FAQ-style components

---

## Images Catalog

### Brand Assets
- `proppy-logo.png` (175x30px) - Main logo

### Navigation Icons (34x34px each)
- ChatGPT-style icons (multiple)
- Reviews icon
- Properties icon
- Tech icon
- Results icon
- Contact icon
- FAQ icon

### Hero/Feature Illustrations
- `Group.png` (178x140px) - Main hero illustration
- Various "Group 13213XXXXX" numbered illustrations
- "Personal Finance" icons
- "Startup" icons
- "Team Success" icons

### Problem/Solution Icons
- "Output Learned Knowledge"
- "Frame 2095585777"
- Various numbered groups

### Feature Icons
- "Pie And Charts 1"
- "Money Growing On Trees 4"
- "Team Work 3"

### Property Images
- Hastings properties (90x98px thumbnails)
- Investment properties images

### Review/Profile Images
- Customer profile pictures (circular)
- Google review photos

---

## Technical Stack

### CMS & Framework
- **CMS:** WordPress
- **Theme:** Divi (Elegant Themes)
- **Builder:** Divi Builder (visual page builder)

### JavaScript Libraries
- jQuery
- Slick Carousel (for image/testimonial sliders)
- GSAP (GreenSock Animation Platform) with ScrollTrigger
- Divi Filter plugin

### Third-Party Integrations
1. **Forms & CRM:** LeadConnector/GoHighLevel (iframe embeds)
2. **Reviews:** Google Reviews API
3. **Analytics:** Facebook Pixel
4. **Security:** reCAPTCHA v3
5. **Calendar:** Embedded booking widget
6. **Chat:** Live chat widget (vendor TBD)

### Known Issues (From Console)
- Slick carousel initialization errors
- GSAP element not found (#faqContainer)
- Form tracking errors (LeadConnector backend)
- Some pages timeout during crawl (heavy content/slow loading)

---

## Page Load Performance Notes

### Fast Loading Pages
- Pricing
- What We Do
- Reviews & Testimonials
- FAQ
- Contact Us

### Slow Loading Pages (30s+ timeouts)
- Why Choose Proppy
- How We Do It
- Properties We Source
- Our Technology
- Our Results

**Recommendation:** These pages likely have heavy animations, large images, or complex Divi Builder layouts that need optimization in the rebuild.

---

## Conversion Optimization Elements

### Primary CTAs
- **Text:** "Get Started for Free" (appears 5+ times per page)
- **Secondary:** "Schedule a call", "Learn more"
- **Phone:** Clickable tel: links
- **WhatsApp:** Direct messaging link

### Trust Builders
1. Google 5.0 rating (prominently displayed)
2. 10+ customer testimonials with photos
3. Money Back Guarantee (repeated multiple times)
4. "15 years experience" statistic
5. Real customer names and photos
6. Property transaction numbers

### Lead Magnets
- Free investment assessment
- Free starter guide
- Instant property alerts signup
- Market update newsletters

### Urgency/Scarcity
- "Get Expert Help in 15 Minutes"
- Limited calendar availability (visual)
- "Start your journey with confidence"

---

## Forms & Data Capture

### Contact Form (Contact Us page)
**Fields:**
- First Name * (required)
- Last Name
- Phone * (required, with country code selector)
- Email * (required)
- Message * (required)
- reCAPTCHA protection
- "Send" button

### Newsletter Signup (Footer - all pages)
**Fields:**
- Email * (required)
- "Signup" button
- reCAPTCHA protection
- Embedded via iframe (LeadConnector)

### Calendar Booking
- Interactive calendar widget
- Time zone selector
- Available slot selection
- Embedded via iframe

---

## Responsive Breakpoints

**Status:** Needs testing
- Desktop: Full layouts
- Tablet: Expected ~768px breakpoint
- Mobile: Expected ~480px breakpoint

**Elements to Test:**
- Navigation collapse to hamburger
- Grid layouts stack to single column
- Image scaling
- Form layout adjustments
- Chat widget repositioning

---

## SEO Elements

### Meta Information
- **Title Format:** "[Page Name] - Proppy"
- **H1 Usage:** Present on all pages
- **Semantic HTML:** Proper article, nav, footer tags
- **Alt Text:** Partially present (many images missing alt text)

### Internal Linking
- Comprehensive footer navigation
- Cross-linked content (guides, updates, properties)
- CTA links throughout pages
- Breadcrumbs: Not observed (should check)

---

## Content Patterns

### Copywriting Style
- **Tone:** Professional but approachable
- **Focus:** Benefits-driven, investor-focused
- **Pain Points:** Addresses common investor concerns
- **Social Proof:** Heavy emphasis on reviews and results

### Common Sections Per Page
1. Hero with H1 and CTA
2. Problem statement
3. Solution/benefits
4. Social proof (reviews/stats)
5. Feature highlights
6. Final CTA
7. Footer (identical across all pages)

---

## Files Created

### Documentation
1. `00-MASTER-AUDIT-SUMMARY.md` (this file)
2. `01-HOMEPAGE.md` - Complete homepage documentation
3. `CRAWL_RESULTS.json` - Technical crawl data
4. `crawl-all-pages.js` - Page list for reference

### Screenshots
1. `homepage-full.png` - Full homepage screenshot
2. `about-us-full.png` - Full about page screenshot

---

## Next Steps for Complete Audit

### Remaining Tasks

1. **Visit Remaining Pages** (15 pages)
   - Retry timeout pages with different strategy
   - Capture screenshots of each page
   - Document unique components per page

2. **Download All Images**
   - Create organized image library
   - Catalog dimensions and usage
   - Identify duplicates and variations

3. **Content Pages**
   - All 12 market update articles
   - All investor guide articles
   - All 9 property showcase pages

4. **Extract Design System**
   - CSS color palette (exact hex codes)
   - Font families and sizes
   - Spacing system (margins/padding)
   - Button styles and variations
   - Form field styles

5. **Document Interactions**
   - Hover animations
   - Scroll triggers
   - Carousel behaviors
   - Form validations
   - Mobile menu behavior

6. **Component Library**
   - Create visual component guide
   - Document props/variations
   - Screenshot each component
   - Note responsive behaviors

7. **Content Inventory**
   - Extract all copy
   - Catalog all images with contexts
   - List all links and destinations
   - Document embedded content

---

## Rebuild Recommendations

### Performance Improvements
1. Optimize images (WebP format, proper sizing)
2. Lazy load below-fold content
3. Reduce JavaScript bundle size
4. Minimize third-party scripts
5. Implement proper caching

### User Experience
1. Faster page load times
2. Smoother animations (CSS vs JS where possible)
3. Mobile-first responsive design
4. Accessibility improvements (alt text, ARIA labels)
5. Form validation feedback

### Technical Stack Options
1. **Option A:** Modern WordPress with custom theme
2. **Option B:** Next.js/React static site
3. **Option C:** Webflow for visual editing
4. **Option D:** Headless CMS + React frontend

### Must-Have Features
1. Google Reviews integration
2. Contact form with validation
3. Calendar booking system
4. Newsletter signup
5. Property showcase system
6. Blog/article publishing
7. Mobile responsiveness
8. Fast page loads
9. SEO optimization
10. Analytics tracking

---

## Contact for Clarification

**Questions to ask client:**
1. Which pages are most important?
2. What's working well that must be preserved?
3. What's not working that should be improved?
4. Are there features they want to add?
5. What's the target audience profile?
6. What are the main conversion goals?
7. Any brand guidelines or style guide?
8. Access to WordPress admin for complete content export?
9. Access to analytics data?
10. Budget and timeline for rebuild?

---

## File Structure

```
/Users/boo2/Desktop/proppy/site-audit/
├── 00-MASTER-AUDIT-SUMMARY.md (this file)
├── 01-HOMEPAGE.md
├── CRAWL_RESULTS.json
├── crawl-all-pages.js
├── pages/
│   ├── homepage-full.png
│   └── about-us-full.png
├── images/ (to be populated)
├── components/ (to be populated)
├── interactions/ (to be documented)
└── content/ (to be extracted)
```

---

**Status:** ✅ Foundation audit complete | 🔄 Detailed crawl in progress | ⏳ Component library pending
