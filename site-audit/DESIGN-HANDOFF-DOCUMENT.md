# Proppy.com.au - Complete Design Handoff Document
**Date:** January 16, 2026  
**Purpose:** Comprehensive specification for complete website redesign  
**Audience:** Designers & Developers

---

## 📋 Table of Contents
1. [Site Overview](#site-overview)
2. [Global Design System](#global-design-system)
3. [Page Inventory & Components](#page-inventory--components)
4. [Reusable UI Components](#reusable-ui-components)
5. [Content Patterns](#content-patterns)
6. [Image Assets](#image-assets)
7. [Navigation & Footer](#navigation--footer)

---

## 🎯 Site Overview

### Business Context
- **Company:** Proppy Pty Ltd
- **Service:** Property investment advisory and sourcing
- **Target Audience:** Australian property investors (first-time and experienced)
- **Primary Goal:** Lead generation via "Get Started" consultation bookings
- **Key Differentiators:** 
  - Money Back Guarantee
  - 15 years experience
  - Technology platform
  - Proven track record with specific property results

### Site Structure
```
proppy.com.au/
├── Main Pages (20)
│   ├── Home
│   ├── What We Do
│   ├── Why Choose Proppy
│   ├── Properties We Source
│   ├── Our Technology
│   ├── Get Started
│   ├── Pricing
│   ├── Our Results (property showcases)
│   ├── Reviews & Customer Testimonials
│   ├── Contact Us
│   ├── About Us
│   ├── FAQ
│   ├── Terms & Conditions
│   ├── Privacy Policy
│   ├── Money Back Guarantee
│   ├── Investor Assessment Session
│   └── Sitemap
├── Resource Hubs (3)
│   ├── /market-updates (12 articles)
│   ├── /investor-guides (1+ articles)
│   └── /investor-updates (hotspot updates)
└── Property Showcases (9)
    └── /property/[slug] (individual case studies)
```

---

## 🎨 Global Design System

### Color Palette
**Primary Colors:**
- Deep Blue: `#1a365d` (headers, nav)
- Medium Blue: `#2c5282` (links, accents)
- Light Blue: `#bee3f8` (backgrounds, hover states)

**Accent Colors:**
- Gold/Yellow: `#f6ad55` → `#dd6b20` (gradient for CTAs)
- Success Green: `#48bb78` (positive stats)
- Warning Red: `#f56565` (urgent CTAs)

**Neutrals:**
- White: `#ffffff` (backgrounds)
- Light Gray: `#f7fafc` (section backgrounds)
- Medium Gray: `#a0aec0` (secondary text)
- Dark Gray: `#2d3748` (body text)
- Black: `#1a202c` (headlines)

### Typography
**Font Stack:** Sans-serif system fonts (Arial, Helvetica, system-ui)

**Hierarchy:**
- **H1 (Hero Headlines):** 48-56px, Bold (700), Line height 1.2
- **H2 (Section Headers):** 36-42px, Bold (700), Line height 1.3
- **H3 (Subsections):** 28-32px, SemiBold (600), Line height 1.4
- **H4 (Card Titles):** 20-24px, SemiBold (600), Line height 1.5
- **Body Large:** 18-20px, Regular (400), Line height 1.6
- **Body Standard:** 16-18px, Regular (400), Line height 1.7
- **Small Text:** 14-16px, Regular (400), Line height 1.5
- **Stats/Numbers:** 32-48px, Bold (700), Line height 1.1

**Text Styles:**
- Links: Underline on hover, color transition 0.2s
- Lists: 8px bottom margin per item
- Quotes: Italic, 24px, indented 32px
- Labels: Uppercase, 12-14px, Letter spacing 0.5px

### Spacing System
**Base unit:** 8px

**Scale:**
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px
- 4xl: 96px

**Component Padding:**
- Buttons: 12px 24px
- Cards: 24px
- Sections: 64px vertical, 16px horizontal (mobile) / 32px (tablet) / auto (desktop)
- Container max-width: 1200px

### Shadows & Effects
- **Card Shadow:** `0 2px 8px rgba(0,0,0,0.1)`
- **Card Hover:** `0 4px 16px rgba(0,0,0,0.15)`
- **Button Shadow:** `0 2px 4px rgba(0,0,0,0.1)`
- **Border Radius:** 8px (cards), 6px (buttons), 4px (inputs)

### Responsive Breakpoints
- **Mobile:** < 768px (single column)
- **Tablet:** 768px - 1024px (2 columns)
- **Desktop:** > 1024px (3-4 columns)

---

## 📄 Page Inventory & Components

### 1. HOMEPAGE
**Screenshot:** `pages/main/homepage.png`

**Hero Section:**
- Full-width background (light blue gradient or photo)
- H1: "Successful Property Investment Made Simple" (or similar value prop)
- Subheadline: 1-2 sentence description
- Primary CTA: "Get Started" button (gold gradient)
- Secondary CTA: "Learn More" or "See Our Results"
- Trust badge: "Money Back Guarantee" with icon

**Value Propositions (3-4 cards):**
- Icon (top)
- Heading (H3)
- Description (2-3 sentences)
- Optional: Learn more link
- Layout: 3 columns desktop, 1 column mobile

**Social Proof Section:**
- Heading: "15 Years of Customer Success"
- Stats bar: 3-4 key metrics (investors helped, properties sourced, avg return %, years experience)
- Testimonial carousel or grid
- CTA: "Read More Reviews"

**How It Works (Process Steps):**
- Step-by-step visual (1-2-3-4)
- Each step: Number badge + Heading + Description
- Visual: Connect steps with lines/arrows (desktop)
- Layout: Horizontal scroll mobile, 4 columns desktop

**Featured Properties:**
- Heading: "Recent Success Stories"
- Property cards (3-4): Image + Location + Key stats + "View Details" link
- CTA: "See All Results"

**Technology Platform Highlight:**
- Screenshot or mockup of platform interface
- Feature list (4-6 bullets)
- CTA: "Explore Our Technology"

**Final CTA Section:**
- Background: Gradient or solid color
- Heading: "Ready to Reinvent Your Property Investment Journey?"
- Description
- CTA: "Book a 15-Minute Call" + "Get Started For Free"

### 2. WHAT WE DO
**Screenshot:** `pages/main/what-we-do.png`

**Components:**
- Hero with headline + description
- Service breakdown (3-4 main services)
  - Icon
  - Service name
  - Detailed description
  - Benefits list
- Process timeline
- Comparison table (Traditional vs Proppy approach)
- CTA section

### 3. WHY CHOOSE PROPPY
**Screenshot:** `pages/main/why-choose-proppy.png`

**Components:**
- Hero section
- Unique selling points (6-8 cards)
- Money Back Guarantee callout box
- Track record statistics
- Team credentials
- Awards/Certifications (if any)
- CTA section

### 4. PROPERTIES WE SOURCE
**Screenshot:** `pages/main/properties-we-source.png`

**Components:**
- Hero section
- Property types (residential, apartments, land, etc.)
- Location focus map (interactive or static)
- Selection criteria explanation
- Example properties (carousel or grid)
- CTA: "See Our Results"

### 5. OUR TECHNOLOGY
**Screenshot:** `pages/main/our-technology.png`

**Components:**
- Hero section
- Platform screenshots/mockups
- Feature highlights (6-8 features)
- Dashboard preview
- Data sources explanation
- CTA: "Get Started to Access Platform"

### 6. GET STARTED / PRICING
**Screenshots:** `pages/main/get-started.png`, `pages/main/pricing.png`

**Get Started Components:**
- Hero with clear value proposition
- Booking calendar integration OR
- Contact form (Name, Email, Phone, Message)
- Process steps (what happens after you submit)
- FAQ accordion
- Guarantee badge

**Pricing Components:**
- Pricing tiers (if applicable) OR
- "No upfront cost" messaging
- What's included list
- Payment terms
- Money back guarantee
- Comparison table
- CTA: "Book Consultation"

### 7. OUR RESULTS (Property Showcase Hub)
**Screenshot:** `pages/main/our-results.png`

**Components:**
- Hero: "Proven Results for Real Investors"
- Filter/Sort options (Location, Year, Return type)
- Property grid (9+ properties)
  - Each card: Thumbnail + Location + Headline + Key stats preview
- Pagination or "Load More"
- Stats summary banner (Total properties, Avg return, etc.)

### 8. INDIVIDUAL PROPERTY SHOWCASE PAGE
**Screenshots:** `pages/properties/*.png` (9 examples)

**Standard Layout (ALL property pages follow this):**

**Hero Section:**
- Large property photo (full-width or 60% width)
- Location tag (suburb, state)
- Property headline (H1)
- Purchase story (2-3 paragraphs)
- CTA button: "Get Started"

**Key Stats Grid (4 columns):**
Each stat card contains:
- Icon (dollar, growth chart, house, rental)
- Large number with unit ($, %, $X/week)
- Label below
- Colors: Dollar (blue), Growth (green), Rent (blue), Rental Growth (green)

Stats shown:
1. **Purchase Price:** Dollar amount
2. **Capital Growth:** Percentage + time period (e.g., "+32% Over 3 Years")
3. **Current Rent:** Dollars per week
4. **Rental Growth:** Percentage + time period

**Illustrated Section:**
- Illustration of investor/property (consistent graphic style)
- Bullet point list of property highlights or market insights (4-6 points)

**"More Results" Carousel:**
- Heading: "More Result" (sic - appears to be typo on original)
- Horizontal scrollable cards
- Shows 3-4 other property thumbnails with titles
- Arrow navigation
- Links to other property pages

**CTA Section:**
- Background: Gradient or solid color
- Heading: "Ready to Reinvent Your Property Investment Journey?"
- Description
- Button: "Book a 15-Minute Call"

**Property Examples:**
1. **Hastings - High Growth Coastal** ($453K → +32% → $500/wk)
2. **Hastings - Waterfront Cottage** ($443K → +30% → $550/wk)
3. **Hastings - High Yield** ($390K → +24% → $720/wk)
4. **Albion - Capital & Rental** ($600K → +28% → $615/wk)
5. **Reservoir - Gem Cashflow** ($615K → +28% → $570/wk)
6. **Reservoir - Strong Rental** ($541K → +34% → $675/wk)
7. **Seaford - Rare Block** ($388K → +39% → $625/wk)
8. **Thornbury - High Growth** ($460K → +30% → $565/wk)
9. **Richmond - Gem** ($184K → +50% → $465/wk)

### 9. REVIEWS & CUSTOMER TESTIMONIALS
**Screenshot:** `pages/main/reviews-customer-testimonials.png`

**Components:**
- Hero section
- Testimonial cards (photo + name + location + quote + result)
- Video testimonials (if any)
- Trust badges (Google reviews, Trustpilot, etc.)
- Stats: Years in business, Investors helped, Satisfaction rate
- CTA: "Join Our Success Stories"

### 10. MARKET UPDATES (Hub)
**Screenshot:** `pages/main/market-updates-hub.png`

**Components:**
- Hero: "Stay Ahead of the Market"
- Description of what market updates include
- Article grid (12+ articles)
  - Each: Featured image + Date + Title + Excerpt + "Read More"
- Layout: 3 columns desktop, 1 column mobile
- Pagination
- Newsletter signup: "Get Updates Delivered"

### 11. MARKET UPDATE ARTICLE PAGE
**Screenshots:** `pages/articles/*.png` (12 examples)

**Standard Article Layout:**
- Featured image (full-width hero)
- Category tag: "Market Updates"
- Published date
- Article title (H1)
- Author/Byline (if applicable)
- Article content:
  - Introduction
  - Sections with H2 subheadings
  - Data visualizations/charts (if applicable)
  - Suburb highlights (3-5 suburbs featured)
    - Suburb name + key metrics + brief analysis
  - Bulleted insights
  - Call-outs or highlight boxes
- CTA: "Get Personalized Market Insights" or "Talk to an Expert"
- Related articles (3-4 at bottom)
- Social share buttons

**Articles Captured:**
1. January 2025 - Hottest Investment Suburbs
2. December 2024 - Final Market Insights
3. November 2024 - Year-End Opportunities
4. October 2024 - Spring Market Analysis
5. September 2024 - Post-Winter Trends
6. August 2025 - Smart Investor's Guide
7. (Plus 6 more historical)

### 12. INVESTOR GUIDES (Hub)
**Screenshot:** `pages/investor-guides-hub.png`

**Components:**
- Hero: "Expert Guides for Smart Investors"
- Description
- Article grid (similar to Market Updates)
- Categories/Tags (if multiple guide types)

### 13. INVESTOR GUIDE ARTICLE
**Screenshot:** `pages/articles/investor-guide-trust-article.png`

**Example: "Should You Purchase an Investment Property Through a Trust?"**
- Featured image
- Category: "Investor Guides"
- Title (H1)
- Article content (educational, evergreen)
  - Introduction to topic
  - Pros and cons
  - Case studies/examples
  - Expert recommendations
  - Action steps
- CTA: "Get Personalized Advice" or "Book Consultation"
- Related guides

### 14. CONTACT US
**Screenshot:** `pages/main/contact-us.png`

**Components:**
- Hero
- Contact form (Name, Email, Phone, Message, Subject dropdown)
- Contact details:
  - Email address
  - Phone number
  - Office address (if applicable)
  - Business hours
- Map embed (if physical location)
- Alternative contact methods (social media links)
- Response time expectation
- CTA: "Book a Call Instead"

### 15. ABOUT US
**Screenshot:** `pages/main/about-us.png`

**Components:**
- Hero with company mission/vision
- Company story (timeline or narrative)
- Team section:
  - Team member cards (Photo + Name + Title + Bio)
  - 3-4 key team members highlighted
- Values/Principles (4-6 cards)
- Milestones/Timeline
- Awards/Certifications
- CTA: "Join Our Community of Investors"

### 16. FAQ
**Screenshot:** `pages/main/faq.png`

**Components:**
- Hero
- Search bar (optional)
- FAQ accordion or expandable sections
- Categories:
  - Getting Started
  - Pricing & Fees
  - Investment Process
  - Technology Platform
  - Results & Track Record
  - Support & Guarantee
- Each FAQ:
  - Question (bold)
  - Answer (expandable)
- CTA: "Still Have Questions? Contact Us"

### 17. MONEY BACK GUARANTEE
**Screenshot:** `pages/main/money-back-guarantee.png`

**Components:**
- Hero with guarantee badge
- Guarantee terms (clear, bullet points)
- How it works (step-by-step)
- Eligibility criteria
- How to claim
- FAQ specific to guarantee
- Trust signals (why we offer this)
- CTA: "Start Risk-Free Today"

### 18. INVESTOR ASSESSMENT SESSION
**Screenshot:** `pages/main/investor-assessment-session.png`

**Components:**
- Hero: "Free Investment Assessment"
- What's included in the session (4-6 bullets)
- What to expect timeline
- Who it's for
- Testimonials from past participants
- Booking calendar OR contact form
- No-obligation messaging

### 19. TERMS & CONDITIONS
**Screenshot:** `pages/main/terms-conditions.png`

**Components:**
- Hero
- Formatted legal text
- Table of contents (jump links)
- Last updated date
- Sections:
  - Acceptance of Terms
  - Services Description
  - User Obligations
  - Intellectual Property
  - Limitation of Liability
  - Governing Law
  - Contact Information

### 20. PRIVACY POLICY
**Screenshot:** `pages/main/privacy-policy.png`

**Components:**
- Hero
- Formatted legal text
- Table of contents
- Last updated date
- Sections:
  - Information Collection
  - How We Use Information
  - Data Sharing
  - Security
  - Cookies
  - User Rights
  - Contact Information

---

## 🧩 Reusable UI Components

### Component: Primary CTA Button
**Appearance:**
- Background: Gold gradient (#f6ad55 → #dd6b20)
- Text: White, 16-18px, SemiBold
- Padding: 12px 24px
- Border radius: 6px
- Shadow: 0 2px 4px rgba(0,0,0,0.1)
- Hover: Slight darken + lift (shadow increases)
- Transition: 0.2s ease

**Variations:**
- Large: 16px 32px padding, 18-20px text
- Small: 8px 16px padding, 14-16px text
- Full-width (mobile)

### Component: Secondary CTA Button
**Appearance:**
- Background: Transparent
- Border: 2px solid #2c5282
- Text: #2c5282, 16-18px, SemiBold
- Padding: 12px 24px
- Border radius: 6px
- Hover: Background #2c5282, Text white
- Transition: 0.2s ease

### Component: Stat Card
**Layout:**
- Icon (top, 48-64px, circular background)
- Large number (H2 size, bold)
- Label (small text, gray)
- Background: White
- Border: 1px solid #e2e8f0
- Border radius: 8px
- Padding: 24px
- Shadow: 0 2px 8px rgba(0,0,0,0.1)
- Hover: Shadow lift

**Used in:**
- Homepage stats
- Property showcase stats
- Results pages

### Component: Property Card (Thumbnail)
**Layout:**
- Image (16:9 or 4:3 ratio, object-fit cover)
- Location tag (overlay or below image, small, gray)
- Headline (H4, 2 lines max, truncate)
- Stats (optional): 2-3 key metrics inline
- "View Details" link or button
- Background: White
- Border radius: 8px
- Shadow: 0 2px 8px rgba(0,0,0,0.1)
- Hover: Shadow lift + slight scale (1.02)

### Component: Testimonial Card
**Layout:**
- Quote icon (top left)
- Quote text (italic, 18-20px, 3-5 lines)
- Author name (bold)
- Author title/location (small, gray)
- Author photo (circular, optional)
- Background: Light gray (#f7fafc)
- Border: 1px solid #e2e8f0
- Border radius: 8px
- Padding: 24px

### Component: Article Card
**Layout:**
- Featured image (16:9 ratio)
- Category tag (small, colored)
- Published date (small, gray)
- Title (H3, 2-3 lines, truncate)
- Excerpt (optional, 2 lines, gray)
- "Read More" link
- Border radius: 8px
- Hover: Image slight zoom

### Component: Navigation Dropdown
**Behavior:**
- Trigger: Hover or click
- Animation: Fade in + slide down (0.2s)
- Background: White
- Shadow: 0 4px 16px rgba(0,0,0,0.15)
- Items: Padding 12px 16px, hover background light blue
- Icons: 24px, left of text

### Component: Footer
**Layout:**
3-4 columns (desktop), stacked (mobile)

**Column structure:**
- Column 1: Logo + Description
- Column 2-4: Link groups (headings + lists)
- Bottom bar: Copyright + Social links + Legal links

**Styling:**
- Background: Dark blue (#1a365d)
- Text: White / Light gray
- Links: Underline on hover
- Padding: 64px vertical

### Component: Newsletter Signup
**Layout:**
- Heading (H4)
- Description (1 sentence)
- Input field + Submit button (inline or stacked mobile)
- Privacy note (small text)
- Success message state

**Styling:**
- Input: White background, gray border, 12px 16px padding
- Button: Gold gradient (matches primary CTA)
- Border radius: 6px

---

## 📐 Content Patterns

### Pattern: Hero Section (Consistent across all pages)
**Structure:**
```
[Background image/gradient]
  └─ Container (centered, max-width 1200px)
     ├─ Breadcrumb (optional, small text)
     ├─ Headline (H1, 1-2 lines)
     ├─ Subheadline/Description (H2 or large paragraph, 2-3 lines)
     ├─ CTA Buttons (1-2 buttons, inline)
     └─ Trust badge or additional info (optional)
```
**Height:** 400-600px desktop, 300-400px mobile

### Pattern: Section Layout (Standard content section)
**Structure:**
```
[Section background]
  └─ Container (max-width 1200px, centered)
     ├─ Section heading (H2, centered or left-aligned)
     ├─ Section description (paragraph, centered or left-aligned)
     └─ Content grid (2-4 columns)
        └─ [Cards/Components]
```
**Spacing:** 64-96px between sections

### Pattern: Alternating Content Blocks
**Structure:**
```
Section 1: [Image Left] [Text Right]
Section 2: [Text Left] [Image Right]
Section 3: [Image Left] [Text Right]
```
**Layout:** 50/50 desktop, stacked mobile (image on top)

### Pattern: Centered CTA Section
**Structure:**
```
[Gradient/Colored background]
  └─ Container
     ├─ Heading (H2, centered, white text)
     ├─ Description (paragraph, centered, white text)
     └─ CTA Buttons (centered, inline)
```
**Styling:** Full-width, 200-300px height, contrasting background

---

## 🖼️ Image Assets

### Logo & Branding
- `images/branding/proppy-logo.png` - Primary logo (640x111px)
- `images/branding/guarantee-badge.png` - Money back guarantee badge (64x88px)

### Navigation Icons (159x159px each)
- `images/icons/nav-what-is-proppy.png`
- `images/icons/nav-customer-success.png`
- `images/icons/nav-reviews.png`
- `images/icons/nav-properties-source.png`
- `images/icons/nav-tech.png`
- `images/icons/nav-get-started.png`
- `images/icons/nav-results.png`
- `images/icons/nav-resources.png`
- `images/icons/nav-contact.png`
- `images/icons/nav-faq.png`

### Property Page Icons (96x95px each)
- `images/properties/icon-dollar.png` - Purchase price icon
- `images/properties/icon-growth.png` - Growth percentage icon
- `images/properties/icon-rent.png` - Rent per week icon
- `images/properties/icon-rental-growth.png` - Rental growth icon
- `images/properties/illustration-investor.png` - Investor illustration (1098x741px)

### Property Photos (Various sizes)
**Hero images (full resolution):**
- `hastings-2019-high-res.jpg` (2360x1232px)
- `hastings-waterfront-cottage.jpg` (770x448px)
- `hastings-high-yield.jpg`
- `albion-capital-rental.jpg`
- `reservoir-gem-cashflow.jpg`
- `reservoir-strong-rental.jpg`
- `seaford-rare-block.jpg`
- `thornbury-high-growth.jpg`
- `richmond-gem.jpg`

**Thumbnails (300x~200px):**
- `albion-2016-thumb.jpg`
- `reservoir-2016-thumb.jpg`
- `reservoir-2014-thumb.jpg`
- `hastings-2019-02-thumb.jpg`
- `hastings-2017-thumb.jpg`

### Article Featured Images
- `article-august-market-update.png` (1670x928px)
- `market-update-jan-2025.png`
- `market-update-dec-2024.png`
- `market-update-nov-2024.png`
- `market-update-oct-2024.png`
- `market-update-sep-2024.png`
- `market-update-aug-2024.png`

### Footer Graphics
- `images/footer/footer-money-back.png`
- `images/footer/footer-get-started.png`
- `images/footer/footer-success.png`

### Image Usage Guidelines
**Property photos:**
- Use high-quality photos (min 1200px width)
- Maintain 16:9 or 4:3 aspect ratio
- Compress for web (80-85% quality)
- Provide alt text with property location + key benefit

**Icons:**
- Use consistent icon style (line or solid, not mixed)
- Icons should be 48-64px in UI
- Ensure sufficient color contrast

**Article images:**
- Feature images should be 1600x900px (16:9)
- Use relevant property/market imagery
- Avoid generic stock photos

---

## 🧭 Navigation & Footer

### Primary Navigation (Desktop)
**Structure:**
```
[Logo Left] [Nav Center] [CTA Button Right]

Nav Items:
1. What is Proppy? (Dropdown)
   - Why Choose Proppy
   - What We Do
   - How We Do It
   - Properties We Source
   - Our Tech & Platform
   - How to Get Started

2. Customer Success (Dropdown)
   - Results
   - Reviews & Customer Testimonials

3. Resources (Dropdown)
   - Investor Guides
   - Market Updates
   - Investor Hotspot Updates
   - Free Investment Assessment

4. Pricing (Direct link)

5. About (Dropdown)
   - Contact Us
   - About Us
   - FAQ

[CTA] Get Started (Button, gold gradient)
```

**Styling:**
- Height: 80-100px
- Background: White
- Shadow: 0 2px 4px rgba(0,0,0,0.1) when scrolled
- Sticky/Fixed position
- Logo: 160-200px width
- Nav text: 16px, medium weight
- Hover: Light blue background on items

### Primary Navigation (Mobile)
**Structure:**
- Hamburger menu icon (right side)
- Logo (center or left)
- Drawer opens from right or top
- Full-screen overlay or panel
- Same menu structure as desktop
- CTA button at bottom of menu

### Footer
**Structure:**
```
[3 Feature Boxes Row]
- Money Back Guarantee
- Get Started For Free
- 15 Years of Customer Success

[4 Column Link Groups]
Column 1: Proppy
- Why Choose Proppy
- What We Do
- How We Do It
- Properties We Source
- Our Tech & Platform
- How to Get Started

Column 2: Customer Success
- Results
- Reviews & Customer Testimonials

Column 3: Resources
- Investor Guides
- Market Updates
- Investor Hotspot Updates
- Free Investment Assessment

Column 4: About
- Contact Us
- About Us
- FAQ
- Pricing
- Sitemap
- Terms & Conditions
- Privacy Policy

[Newsletter Signup]
"Want to stay ahead of the pack?"
[Email input] [Signup button]

[Bottom Bar]
© Proppy Pty Ltd 2025
[Social Icons] Facebook | Instagram
```

**Styling:**
- Background: Dark blue (#1a365d)
- Text: White/Light gray (#e2e8f0)
- Links: No underline, underline on hover
- Icons: 24px, light gray
- Padding: 64px vertical for main section, 24px for bottom bar

---

## ✅ Quality Checklist for Designer

### Visual Design
- [ ] All fonts specified with fallbacks
- [ ] Color palette complete with hex codes
- [ ] Spacing system defined (8px base)
- [ ] Component states defined (default, hover, active, disabled)
- [ ] Responsive breakpoints specified
- [ ] Shadow/elevation system consistent

### Components
- [ ] All reusable components identified
- [ ] Component variations documented
- [ ] Interaction states specified
- [ ] Accessibility considerations (contrast, focus states)

### Content
- [ ] All page layouts documented
- [ ] Content hierarchy clear
- [ ] Image requirements specified
- [ ] Copy placeholders provided where needed

### Assets
- [ ] All images cataloged
- [ ] Image dimensions specified
- [ ] File naming convention followed
- [ ] Alt text requirements noted

### Navigation
- [ ] All menu items listed
- [ ] Dropdown behaviors specified
- [ ] Mobile navigation pattern defined
- [ ] Footer structure complete

---

## 📞 Next Steps

1. **Designer Review:** Review this document + all screenshots in `/pages/` directories
2. **Design Phase:** Create new design system and mockups in Figma/Sketch/Adobe XD
3. **Design Handoff:** Export design specs and assets
4. **Development Phase:** Return to development with complete designs
5. **Content Migration:** Use screenshots as reference for exact copy

---

**Document Version:** 1.0  
**Last Updated:** January 16, 2026  
**Total Pages Documented:** 43  
**Total Assets Cataloged:** 41+  
**Ready for Design:** ✅
