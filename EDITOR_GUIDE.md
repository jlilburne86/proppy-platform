# Proppy Content Editor Guide

**Welcome to the Proppy admin panel!** This guide will help you create and edit content without any coding knowledge.

## Quick Start

1. **Login:** Go to `https://proppy.com.au/admin/`
2. **Choose what to edit:** Articles, Authors, or Pages
3. **Make changes:** Use the visual editor
4. **Publish:** Click "Publish" to make changes live

---

## Logging In

### First Time Login

1. Check your email for an **invitation link** from Netlify
2. Click the link
3. Set your password
4. You're in!

### Returning Login

1. Go to `https://proppy.com.au/admin/`
2. Click **"Login with Netlify Identity"** (or "Login with GitHub")
3. Enter your email and password
4. Click **"Log in"**

---

## Understanding the Interface

When you login, you'll see:

- **Left Sidebar:** Content types (Articles, Authors, Pages)
- **Main Area:** List of content or editor
- **Top Bar:** Workflow status, publish button

### Workflow Status

Articles can have three statuses:

- **Draft** 📝 - Not visible on the website
- **In Review** 👀 - Ready for someone to review
- **Ready** ✅ - Approved and ready to publish

---

## Creating a New Article

### Step 1: Click "New Article"

1. Click **"Articles"** in the left sidebar
2. Click **"New Article"** button (top right)

### Step 2: Fill in Article Details

**Required Fields:**

1. **Title** (e.g., "Sydney Market Analysis Q1 2024")
   - Keep it under 70 characters
   - Make it clear and specific

2. **Description** (for Google search results)
   - 150-160 characters
   - Include key words people would search for
   - Example: "Analysis of Sydney property market Q1 2024 with vacancy rates, price trends, and investor insights from CoreLogic data."

3. **Category** - Choose from dropdown:
   - Market Trends
   - Suburb Profiles
   - Strategy
   - Cycles
   - Case Studies
   - Risk

4. **Audience** - Who is this for?
   - Both (Newer & Experienced) ← Most common
   - Newer Investors
   - Experienced Investors

5. **Reading Time**
   - Format: "7 min" (include the word "min")
   - Calculate: word count ÷ 200 = minutes

6. **Publication Status**
   - Draft (not visible) ← Start with this
   - Published (visible on site)

7. **Author** - Usually "Proppy Editorial"

8. **Owner Email** - Usually "editor@proppy.com.au"

9. **Next Review Date**
   - When to check if this article needs updates
   - Usually 6 months from now
   - Click the calendar icon to pick a date

10. **Sources** - Leave defaults (CoreLogic, ABS, etc.)
    - Click "+ Add sources" to add more
    - Enter name and URL

11. **Version** - Leave as "2" (current version)

### Step 3: Write the Article Body

The **Body** field is where you write your article using **Markdown**.

#### Markdown Basics

**Headings:**
```
## Main Section (use for major sections)
### Subsection (use for subsections)
```

**Text Formatting:**
```
**Bold text** - for emphasis
*Italic text* - for subtle emphasis
```

**Lists:**
```
Bullet list:
- First point
- Second point
- Third point

Numbered list:
1. First step
2. Second step
3. Third step
```

**Links:**
```
[Link text](https://website.com)
```

**Quotes:**
```
> This is a quote
```

**Code:**
```
Inline code: `like this`

Code block:
```
Multiple lines of code
go here
```
```

#### Standard Article Structure

**All Proppy articles should follow this structure:**

```markdown
# Article Title (automatically added from title field)

Brief introduction paragraph explaining what this article covers.

## Market Context

Background and context for the analysis. Include recent data (2020-2023) and longer-term (10-20 year) trends.

## Key Drivers

**Driver 1:** Explanation with data
**Driver 2:** Explanation with data
**Driver 3:** Explanation with data

## What the Data Shows

Analysis of CoreLogic, PropTrack, and ABS data. Include specific numbers, dates, and sources.

## 🔍 Proppy Data Lens

Multi-signal analysis section. ALWAYS include this emoji heading exactly as shown.

Explain how multiple indicators interact to reveal opportunities.

## Expert Insight

Quotes from CoreLogic, PropTrack, RBA, or other authoritative sources. Always attribute.

Example:
> Tim Lawless, Research Director at CoreLogic, noted in November 2023: "Quote here."

## Investor Lens

### For Newer Investors

**Start with X.** Advice for beginners.

**Key principles:**
- Point 1
- Point 2
- Point 3

**Example:** Real-world scenario

### For Experienced Investors

**Strategy for experienced investors.** Advanced advice.

**Key principles:**
- Point 1
- Point 2
- Point 3

**Example:** Real-world scenario

## Risks & Considerations

**Risk 1:** Explanation and mitigation
**Risk 2:** Explanation and mitigation
**Risk 3:** Explanation and mitigation

## Practical Checklist

Before acting:

1. **Check item 1**
2. **Check item 2**
3. **Check item 3**

## Key Takeaways

1. **Takeaway 1 with data support**
2. **Takeaway 2 with data support**
3. **Takeaway 3 with data support**

> **Disclaimer:** This article is general information only and does not constitute financial, taxation or legal advice. Australian property markets are influenced by numerous factors and past performance does not guarantee future results. Seek professional guidance tailored to your circumstances before making investment decisions.
```

### Step 4: Add Images (Optional)

1. Place cursor where you want the image
2. Click the **image icon** in the toolbar
3. Choose **"Upload an image"** or **"Choose from library"**
4. Select file from your computer
5. Add **Alt text** (description for accessibility)
6. Click **"Insert"**

The image will appear like this in markdown:
```
![Alt text](/assets/uploads/image-name.jpg)
```

### Step 5: Preview Your Article

1. Click the **eye icon** (👁️) in the top right
2. See how your article will look on the website
3. Check formatting, headings, links
4. Click **"Close"** to return to editing

### Step 6: Save as Draft

1. Click **"Save"** button (top right)
2. Your article is saved as a draft
3. Not visible on the website yet

### Step 7: Publish

**When your article is ready:**

1. Change **Publication Status** from "draft" to "published"
2. Click **"Save"**
3. Click **"Publish" → "Publish now"**

**Your article is now live!**

⚠️ **Important:** After publishing, someone needs to run the build scripts to regenerate HTML. See "After Publishing" section below.

---

## Editing Existing Articles

### Step 1: Find the Article

1. Click **"Articles"** in left sidebar
2. Browse or use search box
3. Click on the article title

### Step 2: Make Changes

- Edit any field
- Update the body text
- Add/remove images

### Step 3: Save and Publish

1. Click **"Save"**
2. If you want changes live immediately:
   - Click **"Publish" → "Publish now"**

---

## Working with Images

### Uploading New Images

1. While editing, click **image icon** in toolbar
2. Click **"Upload an image"**
3. Choose file (JPG, PNG, WebP under 2MB recommended)
4. Add **alt text** (what's in the image)
5. Click **"Insert"**

### Best Practices for Images

✅ **DO:**
- Use high-quality images (at least 1200px wide)
- Compress images before uploading (use tinypng.com)
- Write descriptive alt text ("Brisbane skyline from Story Bridge")
- Use relevant images that support the content

❌ **DON'T:**
- Upload huge files (over 5MB)
- Use copyrighted images without permission
- Skip alt text (important for accessibility)
- Use generic stock photos (prefer Australian locations)

### Managing Uploaded Images

All uploaded images go to `/assets/uploads/`.

To reuse an image:
1. Click image icon
2. Choose **"Choose from library"**
3. Select the image
4. Click **"Insert"**

---

## Editorial Workflow

### Draft → Review → Publish

Proppy uses a 3-stage workflow:

#### Stage 1: Draft
- Your article is saved but not visible
- You can edit freely
- **Status: Draft**

#### Stage 2: In Review
- When ready for review, click **"Set status" → "In review"**
- Reviewer can see it and leave comments
- **Status: In Review**

#### Stage 3: Ready
- Reviewer approves: click **"Set status" → "Ready"**
- Article is approved but not yet published
- **Status: Ready**

#### Stage 4: Published
- Click **"Publish" → "Publish now"**
- Article goes live on the website
- **Status: Published**

### Collaboration

**Leaving comments:**
1. Select text in the article
2. Click the comment icon
3. Type your comment
4. Click **"Add comment"**

**Responding to comments:**
1. Click on the comment bubble
2. Type your response
3. Click **"Reply"**

**Resolving comments:**
- Click **"Resolve"** when addressed

---

## After Publishing: Important!

⚠️ **Critical:** When you publish content through the CMS, the **HTML files are NOT automatically regenerated**.

### What Needs to Happen

After publishing an article, someone (you or a developer) must:

1. Open terminal/command line
2. Run these commands:
   ```bash
   cd /Users/boo2/Desktop/proppy
   source .venv/bin/activate
   python3 tools/convert-articles-to-html.py
   python3 tools/generate-articles.py
   ```
3. Deploy the updated files to the website

### Automated Option

**Ask your developer to set up GitHub Actions** to automate this. Then publishing will be truly one-click.

---

## Managing Authors

### Adding a New Author

1. Click **"Authors"** in left sidebar
2. Click **"New Author"**
3. Fill in:
   - Name
   - Email
   - Bio (optional)
   - Photo (optional)
   - LinkedIn URL (optional)
4. Click **"Publish" → "Publish now"**

### Editing Author Info

1. Click **"Authors"**
2. Find and click the author
3. Update fields
4. Click **"Save"** and **"Publish"**

---

## Editing Page Content

### Results Page

1. Click **"Pages"** in left sidebar
2. Click **"Results Page"**
3. Edit:
   - Hero headline
   - Hero description
   - Individual results (click "+ Add results")
4. Click **"Save"** and **"Publish"**

### Resources Page

1. Click **"Pages"**
2. Click **"Resources Page"**
3. Edit:
   - Hero headline
   - Hero description
   - Newsletter CTA text
4. Click **"Save"** and **"Publish"**

---

## Tips for Great Content

### Writing Style

✅ **DO:**
- Use clear, direct language
- Include specific data with sources
- Cite CoreLogic, PropTrack, ABS, RBA data
- Use examples from real markets
- Explain "why" not just "what"

❌ **DON'T:**
- Use hype language ("guaranteed returns," "booming market")
- Make predictions as certainties
- Give personal financial advice
- Use generic statements without data

### Data Quality

**Always cite sources:**
```
Bad: "Brisbane prices are rising."

Good: "Brisbane median house prices rose 42.7% between March 2020 and June 2022 (CoreLogic, 2022)."
```

**Be specific with dates:**
```
Bad: "Recently, vacancy rates fell."

Good: "Perth's vacancy fell to 0.7% in mid-2022, preceding 12-15% annual price growth in 2023 (PropTrack, 2023)."
```

### SEO Best Practices

1. **Use keywords naturally** in title and first paragraph
2. **Write for humans first**, Google second
3. **Include questions** people might search for
4. **Link to other articles** on the site (internal linking)
5. **Use descriptive headings** (H2, H3) that include keywords

---

## Troubleshooting

### "I can't log in"

**Fix:**
- Check you're using the correct email
- Try "Forgot password" link
- Contact admin to re-send invitation

### "My changes aren't showing on the website"

**Fix:**
- Did you click "Publish"?
- If yes, HTML needs to be regenerated (contact developer)

### "I can't upload an image"

**Fix:**
- Check file size (under 5MB)
- Check file type (JPG, PNG, WebP only)
- Try a different image

### "The editor is not saving"

**Fix:**
- Check your internet connection
- Try refreshing the page (your draft is auto-saved)
- Contact admin if problem persists

### "I accidentally deleted something"

**Fix:**
- Decap CMS uses Git version control
- Every change is saved
- Ask developer to restore from Git history

---

## Keyboard Shortcuts

Speed up your editing with these shortcuts:

- **Ctrl/Cmd + S** - Save
- **Ctrl/Cmd + B** - Bold
- **Ctrl/Cmd + I** - Italic
- **Ctrl/Cmd + K** - Insert link
- **Ctrl/Cmd + Z** - Undo
- **Ctrl/Cmd + Shift + Z** - Redo

---

## Need Help?

### Documentation

- **Decap CMS Docs:** https://decapcms.org/docs/
- **Markdown Guide:** https://www.markdownguide.org/basic-syntax/

### Contact

For technical issues or questions:
- Email: editor@proppy.com.au
- Or contact your site administrator

---

## Quick Reference Card

**Login:** `https://proppy.com.au/admin/`

**Create Article:**
1. Articles → New Article
2. Fill title, description, category
3. Write body in markdown
4. Save → Publish

**Edit Article:**
1. Articles → Click article
2. Make changes
3. Save → Publish

**Upload Image:**
1. Click image icon
2. Upload file
3. Add alt text
4. Insert

**Editorial Workflow:**
Draft → In Review → Ready → Published

**After Publishing:**
→ Rebuild HTML (contact developer)
→ Deploy to production

---

**Happy editing!** 🎉

Remember: When in doubt, save as a draft and ask for help. You can't break anything permanently—everything is version-controlled.
