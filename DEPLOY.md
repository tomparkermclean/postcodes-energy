# 🚀 Deployment Guide for postcodes.energy

## Current Status: Ready to Deploy! ✅

Your website is fully functional and tested locally. Time to go live!

---

## Step 1: Push to GitHub

### 1.1 Initialize Git (if not already done)

Open PowerShell in the project folder and run:

```powershell
cd "C:\Users\blueb\OneDrive\Documents\postcodes-energy"
git init
git add .
git commit -m "Initial commit - postcodes.energy V1"
```

### 1.2 Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `postcodes-energy`
3. Description: "Find UK postcodes in the same electricity substation area"
4. **Keep it Public** (for free Cloudflare Pages hosting)
5. **Don't add README** (you already have one)
6. Click "Create repository"

### 1.3 Push to GitHub

GitHub will show you commands. Run these:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/postcodes-energy.git
git branch -M main
git push -u origin main
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username

---

## Step 2: Deploy to Cloudflare Pages

### 2.1 Sign Up / Log In

1. Go to: https://dash.cloudflare.com/
2. Sign up or log in
3. Navigate to: **Pages** (in left sidebar)

### 2.2 Create New Project

1. Click **"Create a project"**
2. Click **"Connect to Git"**
3. Choose **GitHub**
4. Authorize Cloudflare to access your GitHub
5. Select the **`postcodes-energy`** repository

### 2.3 Configure Build Settings

When asked for build settings:

- **Project name**: `postcodes-energy`
- **Production branch**: `main`
- **Framework preset**: `None` (or select "None" from dropdown)
- **Build command**: *Leave empty*
- **Build output directory**: `public`

Click **"Save and Deploy"**

### 2.4 Wait for Deployment

- First deployment takes ~2-3 minutes
- You'll see a URL like: `postcodes-energy.pages.dev`
- Test it works!

---

## Step 3: Configure Custom Domain

### 3.1 Add Custom Domain in Cloudflare

1. In your Cloudflare Pages project, go to **"Custom domains"**
2. Click **"Set up a custom domain"**
3. Enter: `postcodes.energy`
4. Click **"Continue"**

### 3.2 Update DNS Settings

If your domain is already in Cloudflare:
- DNS records will be added automatically
- Wait 5-15 minutes for SSL

If your domain is elsewhere (e.g., Namecheap, GoDaddy):
1. Add a CNAME record:
   - Name: `@` (or blank)
   - Value: `postcodes-energy.pages.dev`
2. Or point nameservers to Cloudflare (recommended)

### 3.3 Enable HTTPS

- Cloudflare automatically provisions SSL certificate
- Takes 15-30 minutes
- Your site will be live at: **https://postcodes.energy**

---

## Step 4: Test Production Site

Visit: https://postcodes.energy

Test these postcodes:
- ✅ N15 5QA (Tottenham)
- ✅ BS8 1TH (Bristol)
- ✅ SW1A 1AA (Westminster)
- ✅ E5 8BG (Hackney)
- ✅ G2 1DY (Glasgow)

Check:
- ✅ Map loads and displays UK
- ✅ Postcode search works
- ✅ Substation boundary appears
- ✅ Postcode list displays
- ✅ CSV export works
- ✅ Feedback form submits
- ✅ Mobile responsive

---

## Step 5: Share With Friends! 🎉

Your site is live! Share it:

- Direct link: https://postcodes.energy
- Tweet about it
- Post in community energy groups
- Share on LinkedIn
- Get feedback!

---

## Troubleshooting

### "Build failed"
- Check that `public/` folder is committed to git
- Verify all files are in place

### "Page not loading"
- Wait 2-3 minutes after first deployment
- Check browser console for errors (F12)
- Verify data files are present

### "Custom domain not working"
- DNS propagation takes 15-30 minutes
- Check DNS records are correct
- SSL certificate takes 15-30 minutes

### "Data not loading"
- Open browser console (F12)
- Check for 404 errors on data files
- Verify `public/data/` folder structure is correct

---

## Post-Launch Checklist

After going live:

- ✅ Test on different devices (phone, tablet, desktop)
- ✅ Share with 5-10 friends for feedback
- ✅ Monitor feedback form responses
- ✅ Check analytics (Cloudflare has built-in analytics)
- ✅ Note down feature requests
- ✅ Plan V2 features based on feedback

---

## What's Next? (V2 Features)

Based on feedback, consider adding:
- Population data per substation
- EPC energy consumption data
- Solar potential estimates
- Deprivation index (IMD)
- Autocomplete (if requested)

---

## Need Help?

- Cloudflare Docs: https://developers.cloudflare.com/pages/
- GitHub Docs: https://docs.github.com/
- Leave feedback form responses enabled to hear from users!

---

**You've got this! 🚀**

Deploy with confidence - your V1 is solid and will provide real value to community energy projects across the UK.
