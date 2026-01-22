# Decap CMS Setup Guide for Proppy

**Status:** ✅ Admin panel installed, authentication setup required

## What Has Been Installed

✅ **Admin panel** at `/admin/index.html`
✅ **CMS configuration** at `/admin/config.yml`
✅ **Content collections** for articles, authors, and pages
✅ **Media library** for image uploads (`/assets/uploads/`)
✅ **Editorial workflow** (Draft → Review → Publish)

## What You Need to Complete

🔧 **GitHub authentication setup** (choose ONE option below)

---

## Setup Options

### Option A: Using Netlify (Recommended - Easiest) ⭐

**Best if you're deploying to Netlify or want the simplest setup.**

#### Step 1: Deploy to Netlify

1. **Push code to GitHub:**
   ```bash
   cd /Users/boo2/Desktop/proppy
   git init
   git add .
   git commit -m "Add Decap CMS admin panel"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/proppy.git
   git push -u origin main
   ```

2. **Connect to Netlify:**
   - Go to https://app.netlify.com/
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select your `proppy` repository
   - Build settings:
     - Build command: (leave empty - static site)
     - Publish directory: `.` (current directory)
   - Click "Deploy site"

#### Step 2: Enable Netlify Identity

1. In Netlify dashboard, go to **Site Settings → Identity**
2. Click **"Enable Identity"**
3. Under **Registration preferences**, select:
   - **Invite only** (recommended) or **Open** if you want anyone to sign up
4. Under **External providers**, enable **GitHub**:
   - Click "Add provider" → GitHub
   - Leave default settings and click "Enable"

#### Step 3: Enable Git Gateway

1. Still in **Identity** settings
2. Scroll to **Services** section
3. Click **"Enable Git Gateway"**
4. This allows Decap CMS to commit directly to your GitHub repo

#### Step 4: Invite Editors

1. Go to **Identity** tab in Netlify dashboard
2. Click **"Invite users"**
3. Enter email addresses of editors
4. They'll receive invitation emails with login links

#### Step 5: Access Admin Panel

1. Visit `https://your-site.netlify.app/admin/`
2. Click "Login with Netlify Identity"
3. Use the invitation link from email to set password
4. You're in! Start editing content.

**Done!** Your admin panel is now fully functional.

---

### Option B: GitHub OAuth (No Netlify Required)

**Best if you're NOT using Netlify for hosting (e.g., using Hostinger, AWS, etc.)**

#### Step 1: Create GitHub OAuth App

1. Go to https://github.com/settings/developers
2. Click **"New OAuth App"**
3. Fill in:
   - **Application name:** Proppy CMS
   - **Homepage URL:** `https://proppy.com.au`
   - **Authorization callback URL:** `https://proppy.com.au/admin/`
4. Click **"Register application"**
5. **Save these credentials:**
   - Client ID: `abc123...`
   - Client Secret: `xyz789...` (click "Generate a new client secret")

#### Step 2: Update CMS Configuration

Replace the `backend` section in `/admin/config.yml`:

```yaml
backend:
  name: github
  repo: YOUR_GITHUB_USERNAME/proppy # e.g., jlilburne86/proppy
  branch: main
  base_url: https://your-auth-server.com # See Step 3
  auth_endpoint: /auth
```

#### Step 3: Set Up Authentication Server

You need a simple server to handle GitHub OAuth. **Two options:**

**Option 3A: Use External Service (Easiest)**

Use a free service like **https://github.com/vencax/netlify-cms-github-oauth-provider**

1. Deploy to Heroku/Render/Railway:
   ```bash
   git clone https://github.com/vencax/netlify-cms-github-oauth-provider.git
   cd netlify-cms-github-oauth-provider
   # Follow their README for deployment
   ```

2. Set environment variables:
   ```
   OAUTH_CLIENT_ID=your_github_client_id
   OAUTH_CLIENT_SECRET=your_github_client_secret
   ```

3. Use the deployed URL as your `base_url` in config.yml

**Option 3B: Self-Host Auth Server (Advanced)**

Create a simple Node.js server (code provided in appendix below).

#### Step 4: Access Admin Panel

1. Visit `https://proppy.com.au/admin/`
2. Click "Login with GitHub"
3. Authorize the OAuth app
4. You're in!

---

### Option C: Local Development (Testing Only)

**For testing the admin panel locally before deploying.**

#### Step 1: Enable Local Backend

Uncomment this line in `/admin/config.yml`:

```yaml
local_backend: true
```

#### Step 2: Run Local Backend Server

```bash
cd /Users/boo2/Desktop/proppy
npx decap-server
```

#### Step 3: Run Dev Server

In another terminal:

```bash
cd /Users/boo2/Desktop/proppy
python3 devserver.py
```

#### Step 4: Access Local Admin

1. Visit `http://localhost:8000/admin/`
2. No login required in local mode
3. Edit content, it saves directly to local files

**Note:** This ONLY works locally, not in production.

---

## How to Use the Admin Panel

### Creating a New Article

1. **Login** to `https://proppy.com.au/admin/`
2. Click **"Articles"** in left sidebar
3. Click **"New Article"** button
4. Fill in the form:
   - **Title:** Your article title
   - **Description:** SEO meta description
   - **Category:** Select from dropdown
   - **Publication Status:** Select "published" when ready
   - **Body:** Write your article in markdown
5. Click **"Save"** (creates draft)
6. Click **"Publish" → "Publish now"** to make it live

### Editing Existing Articles

1. Click **"Articles"** → find the article
2. Click on it to open
3. Make changes
4. Click **"Save"**
5. Click **"Publish" → "Publish now"**

### Uploading Images

1. While editing an article, click the **image icon** in the toolbar
2. Choose **"Upload an image"**
3. Select file from your computer
4. Image is uploaded to `/assets/uploads/`
5. Markdown code is inserted automatically

### Editorial Workflow

Decap CMS has a built-in workflow:

1. **Drafts** - Not visible on site
2. **In Review** - Ready for review
3. **Ready** - Approved, ready to publish

To use workflow:
1. Save article as draft
2. Click **"Set status" → "In review"**
3. Reviewer approves: **"Set status" → "Ready"**
4. Publisher: **"Publish" → "Publish now"**

---

## Rebuilding the Site After Changes

When editors publish content through Decap CMS, **the HTML files are NOT automatically regenerated**.

### Option 1: Manual Rebuild (Current Setup)

After publishing new articles:

```bash
cd /Users/boo2/Desktop/proppy
source .venv/bin/activate
python3 tools/convert-articles-to-html.py
python3 tools/generate-articles.py
```

Then deploy updated files to production.

### Option 2: Automated Rebuild with GitHub Actions (Recommended)

I can set up GitHub Actions to automatically:
1. Detect when articles are published
2. Run the Python scripts
3. Commit regenerated HTML files
4. Deploy to production

**Would you like me to set this up?** This makes the workflow fully automated.

---

## Troubleshooting

### "Error loading the CMS configuration"

**Fix:** Check `/admin/config.yml` for syntax errors. YAML is whitespace-sensitive.

### "Unable to authenticate"

**Option A (Netlify):**
- Verify Git Gateway is enabled
- Check Netlify Identity is enabled
- Try re-inviting the user

**Option B (GitHub OAuth):**
- Verify OAuth app credentials are correct
- Check callback URL matches exactly
- Ensure auth server is running

### "Changes not appearing on site"

**Fix:** You need to rebuild HTML files:
```bash
python3 tools/convert-articles-to-html.py
python3 tools/generate-articles.py
```

### "Can't upload images"

**Fix:** Ensure `/assets/uploads/` directory exists and has write permissions.

---

## Next Steps

**Choose your authentication method:**

1. **Netlify (Easiest)** → Follow Option A above
2. **GitHub OAuth (No Netlify)** → Follow Option B above
3. **Local Testing First** → Follow Option C, then deploy with Option A or B

**After authentication is set up:**

1. Invite editors
2. Train them on how to use the admin panel
3. (Optional) Set up automated rebuilds with GitHub Actions

**Questions?** See the FAQ below or refer to Decap CMS documentation: https://decapcms.org/docs/

---

## Appendix: Self-Hosted Auth Server (Option B3)

If you want to self-host the GitHub OAuth server:

### server.js

```javascript
const express = require('express');
const cors = require('cors');
const simpleOauthModule = require('simple-oauth2');

const app = express();
const PORT = process.env.PORT || 3000;

const oauth2 = simpleOauthModule.create({
  client: {
    id: process.env.OAUTH_CLIENT_ID,
    secret: process.env.OAUTH_CLIENT_SECRET,
  },
  auth: {
    tokenHost: 'https://github.com',
    tokenPath: '/login/oauth/access_token',
    authorizePath: '/login/oauth/authorize',
  },
});

app.use(cors());

app.get('/auth', (req, res) => {
  const authorizationUri = oauth2.authorizationCode.authorizeURL({
    redirect_uri: `${process.env.BASE_URL}/callback`,
    scope: 'repo,user',
    state: req.query.state,
  });
  res.redirect(authorizationUri);
});

app.get('/callback', async (req, res) => {
  const { code, state } = req.query;
  const options = {
    code,
    redirect_uri: `${process.env.BASE_URL}/callback`,
  };

  try {
    const result = await oauth2.authorizationCode.getToken(options);
    const token = oauth2.accessToken.create(result);

    res.send(`
      <script>
        window.opener.postMessage(
          'authorization:github:success:${JSON.stringify({
            token: token.token.access_token,
            provider: 'github',
          })}',
          '*'
        );
        window.close();
      </script>
    `);
  } catch (error) {
    console.error('Access Token Error', error.message);
    res.status(500).json('Authentication failed');
  }
});

app.listen(PORT, () => {
  console.log(`Auth server running on port ${PORT}`);
});
```

### package.json

```json
{
  "name": "proppy-cms-auth",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "simple-oauth2": "^5.0.0"
  },
  "scripts": {
    "start": "node server.js"
  }
}
```

### Deploy to Railway/Render/Heroku

```bash
npm install
# Set environment variables in hosting dashboard:
# - OAUTH_CLIENT_ID
# - OAUTH_CLIENT_SECRET
# - BASE_URL (e.g., https://your-auth-server.com)
npm start
```

---

## Summary

✅ **Admin panel is ready** at `/admin/`
🔧 **Complete GitHub authentication** (Option A or B)
📝 **Start editing content** via web interface
🚀 **Rebuild HTML** after publishing changes

**Estimated time to complete authentication:** 15-30 minutes (Option A) or 1-2 hours (Option B)

Let me know which option you'd like to use and I can provide more specific guidance!
