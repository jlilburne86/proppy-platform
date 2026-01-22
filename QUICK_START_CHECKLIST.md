# 🚀 Decap CMS Quick Start Checklist

**Goal:** Get your admin panel live in 30 minutes

---

## Prerequisites

- [ ] GitHub account (create at github.com if needed)
- [ ] Git installed on your computer
- [ ] Code editor (VS Code recommended)

---

## Step 1: Push Code to GitHub (5 minutes)

### Option A: Using Terminal

```bash
# Navigate to project
cd /Users/boo2/Desktop/proppy

# Initialize git (if not done)
git init
git add .
git commit -m "Add Decap CMS admin panel"

# Create repository on GitHub:
# Go to: https://github.com/new
# Repository name: proppy
# Visibility: Private
# Click "Create repository"

# Link local code to GitHub
git remote add origin https://github.com/YOUR_USERNAME/proppy.git
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Desktop (GUI)

1. Download GitHub Desktop: https://desktop.github.com/
2. Open GitHub Desktop
3. File → Add Local Repository → Choose `/Users/boo2/Desktop/proppy`
4. Publish repository → Name: `proppy` → Private → Publish

✅ **Checkpoint:** Code is now on GitHub

---

## Step 2: Deploy to Netlify (10 minutes)

### 2.1 Create Netlify Account

- [ ] Go to https://app.netlify.com/signup
- [ ] Sign up with GitHub account (easiest)
- [ ] Authorize Netlify to access GitHub

### 2.2 Deploy Site

- [ ] Click **"Add new site"** → **"Import an existing project"**
- [ ] Choose **"Deploy with GitHub"**
- [ ] Select your **`proppy`** repository
- [ ] Configure settings:
  - **Branch:** `main`
  - **Build command:** (leave empty)
  - **Publish directory:** `.`
- [ ] Click **"Deploy site"**
- [ ] Wait 1-2 minutes for deployment

✅ **Checkpoint:** Site is live at `https://random-name-12345.netlify.app`

### 2.3 Set Custom Domain (Optional)

- [ ] Go to **Site settings → Domain management**
- [ ] Click **"Add custom domain"**
- [ ] Enter: `proppy.com.au`
- [ ] Follow DNS configuration instructions
- [ ] Wait for DNS to propagate (up to 24 hours)

---

## Step 3: Enable Authentication (10 minutes)

### 3.1 Enable Netlify Identity

- [ ] In Netlify dashboard, go to **Site settings → Identity**
- [ ] Click **"Enable Identity"**
- [ ] Under **Registration**, select:
  - ✅ **Invite only** (recommended for now)
- [ ] Under **External providers**, click **"Add provider"**
  - [ ] Choose **GitHub**
  - [ ] Click **"Enable"**

### 3.2 Enable Git Gateway

- [ ] Scroll down to **Services** section
- [ ] Click **"Enable Git Gateway"**
- [ ] Confirm by clicking **"Enable Git Gateway"** again

✅ **Checkpoint:** Authentication is configured

---

## Step 4: Invite Yourself as Editor (2 minutes)

- [ ] Go to **Identity** tab in Netlify dashboard
- [ ] Click **"Invite users"**
- [ ] Enter your email address
- [ ] Click **"Send"**
- [ ] Check your email for invitation link
- [ ] Click link and set your password

✅ **Checkpoint:** You can now login

---

## Step 5: Test Admin Panel (5 minutes)

### 5.1 Login

- [ ] Visit `https://your-site.netlify.app/admin/`
- [ ] Click **"Login with Netlify Identity"**
- [ ] Enter your email and password
- [ ] You should see the admin dashboard!

### 5.2 Create Test Article

- [ ] Click **"Articles"** in sidebar
- [ ] Click **"New Article"** button
- [ ] Fill in required fields:
  - **Title:** "Test Article - Delete Me"
  - **Description:** "This is a test article"
  - **Category:** Strategy
  - **Publication Status:** published
  - **Body:** "# Test\n\nThis is a test article. Delete me after testing."
- [ ] Click **"Save"**
- [ ] Click **"Publish" → "Publish now"**

### 5.3 Verify Automation

- [ ] Go to GitHub repository
- [ ] Click **"Actions"** tab
- [ ] You should see a workflow running (yellow dot)
- [ ] Wait for it to complete (green checkmark)
- [ ] Check that HTML files were regenerated

✅ **Checkpoint:** Admin panel works, automation runs

---

## Step 6: Delete Test Article (1 minute)

- [ ] Back in admin panel, click **"Articles"**
- [ ] Find "Test Article - Delete Me"
- [ ] Click **three dots** (⋮) → **"Delete entry"**
- [ ] Confirm deletion
- [ ] Click **"Publish" → "Publish now"**

✅ **Checkpoint:** You know how to delete content

---

## Step 7: Invite Other Editors (Optional)

- [ ] Go to Netlify **Identity** tab
- [ ] Click **"Invite users"**
- [ ] Enter email addresses (one per line)
- [ ] Click **"Send"**
- [ ] Share **EDITOR_GUIDE.md** with them

✅ **Checkpoint:** Team can now collaborate

---

## Step 8: Customize Site URL (Optional)

Currently your site is at: `https://random-name-12345.netlify.app`

To use a custom domain:

### Option A: Use Netlify Subdomain

- [ ] Go to **Site settings → Domain management**
- [ ] Click **"Options" → "Edit site name"**
- [ ] Enter: `proppy` (becomes `proppy.netlify.app`)

### Option B: Use Your Own Domain

- [ ] Go to **Site settings → Domain management**
- [ ] Click **"Add custom domain"**
- [ ] Enter: `proppy.com.au`
- [ ] Click **"Verify"**
- [ ] Follow DNS instructions:
  - Go to your domain registrar
  - Add CNAME record: `proppy.com.au` → `random-name-12345.netlify.app`
  - Wait for DNS propagation (1-24 hours)
- [ ] Netlify will automatically provision SSL certificate

✅ **Checkpoint:** Professional domain configured

---

## Verification Checklist

Before going live, verify:

- [ ] ✅ Admin panel loads at `/admin/`
- [ ] ✅ You can login with email/password
- [ ] ✅ You can create a new article
- [ ] ✅ You can edit existing articles
- [ ] ✅ You can upload images
- [ ] ✅ Publishing triggers GitHub Actions
- [ ] ✅ HTML files are regenerated automatically
- [ ] ✅ Changes appear on the live site
- [ ] ✅ Other editors can be invited
- [ ] ✅ You've read the **EDITOR_GUIDE.md**

---

## Common Issues & Quick Fixes

### "Can't access /admin/"

**Problem:** 404 error on admin page

**Fix:**
```bash
# Make sure files are pushed to GitHub
cd /Users/boo2/Desktop/proppy
git add admin/
git commit -m "Add admin panel"
git push
```
Wait 1-2 minutes for Netlify to redeploy.

---

### "Error loading CMS configuration"

**Problem:** Red error message on admin page

**Fix:** Check `/admin/config.yml` for syntax errors
- Spaces matter in YAML (no tabs!)
- Check indentation is correct
- Validate YAML at: https://www.yamllint.com/

---

### "Unable to authenticate"

**Problem:** Login button doesn't work

**Fix:**
1. Verify Netlify Identity is enabled
2. Verify Git Gateway is enabled
3. Clear browser cache and try again
4. Use incognito/private window

---

### "GitHub Actions not running"

**Problem:** Workflow doesn't trigger on publish

**Fix:**
```bash
# Verify workflow file is pushed
cd /Users/boo2/Desktop/proppy
git add .github/workflows/
git commit -m "Add GitHub Actions workflow"
git push
```

Go to GitHub → Actions → Check if workflow appears

---

### "Changes not showing on site"

**Problem:** Published article doesn't appear

**Fix:**
1. Check **Publication Status** is "published" not "draft"
2. Go to GitHub Actions → Verify workflow completed
3. Check if HTML file was regenerated
4. Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)

---

## What to Do Next

### Immediate (Next 24 Hours)

- [ ] Test creating 2-3 real articles
- [ ] Upload some real images
- [ ] Invite 1-2 team members to test
- [ ] Read through **EDITOR_GUIDE.md** thoroughly
- [ ] Bookmark `/admin/` for easy access

### Short Term (Next Week)

- [ ] Set up custom domain (if not done)
- [ ] Create editorial calendar
- [ ] Assign article topics to team
- [ ] Set up editorial workflow (Draft → Review → Publish)
- [ ] Create author profiles for all writers

### Long Term (Next Month)

- [ ] Publish 10+ high-quality articles
- [ ] Monitor GitHub Actions usage (stay under free tier)
- [ ] Gather feedback from editors
- [ ] Optimize article templates based on usage
- [ ] Consider upgrading to paid plans if needed

---

## Support Resources

### Documentation (In This Project)

- 📄 **CMS_IMPLEMENTATION_COMPLETE.md** - Full technical overview
- 📄 **DECAP_CMS_SETUP_GUIDE.md** - Detailed setup instructions
- 📄 **EDITOR_GUIDE.md** - How to use the CMS (share with editors)
- 📄 **BACKEND_ASSESSMENT_AND_RECOMMENDATIONS.md** - Why we chose this solution

### External Resources

- **Decap CMS Docs:** https://decapcms.org/docs/
- **Netlify Identity Docs:** https://docs.netlify.com/visitor-access/identity/
- **Markdown Guide:** https://www.markdownguide.org/basic-syntax/
- **GitHub Actions Docs:** https://docs.github.com/en/actions

### Getting Help

1. **Check documentation** (start with EDITOR_GUIDE.md)
2. **Search Decap CMS docs** (most questions answered there)
3. **Check GitHub Actions logs** (if automation fails)
4. **Contact site administrator** (for technical issues)

---

## Success Criteria

You're ready to go live when:

✅ Admin panel is accessible and secure
✅ You can create/edit/delete articles without errors
✅ Images upload and display correctly
✅ GitHub Actions runs automatically on publish
✅ HTML regenerates without manual intervention
✅ Team members can login and create content
✅ Editorial workflow is understood by all editors

---

## Final Checklist

- [ ] ✅ Code pushed to GitHub
- [ ] ✅ Site deployed to Netlify
- [ ] ✅ Netlify Identity enabled
- [ ] ✅ Git Gateway enabled
- [ ] ✅ Admin panel tested
- [ ] ✅ Test article created and published
- [ ] ✅ GitHub Actions verified working
- [ ] ✅ Editors invited and trained
- [ ] ✅ EDITOR_GUIDE.md shared with team
- [ ] ✅ Ready to create real content!

---

**🎉 Congratulations!** You now have a professional CMS for managing your Proppy content.

**Time to complete:** ~30 minutes to 1 hour
**Monthly cost:** $0 (using Netlify free tier)
**Maintenance:** Minimal (editors manage themselves)

**Questions?** Check the documentation files listed above.

**Ready to publish?** Share the admin panel URL with your team and start creating data-driven property investment content!

---

*Last updated: 22 January 2026*
