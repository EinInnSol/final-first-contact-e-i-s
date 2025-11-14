# 🚀 Deployment Instructions

## Option 1: GitHub Pages (Easiest - FREE)

### Step 1: Enable GitHub Pages

1. Go to your GitHub repository: https://github.com/EinInnSol/final-first-contact-e-i-s
2. Click **Settings** (top right)
3. Scroll down the left sidebar and click **Pages**
4. Under "Source", select:
   - Branch: `claude/create-hifi-demo-01ABeQ16xeaERkuc6DzzVASY`
   - Folder: `/ (root)`
5. Click **Save**

### Step 2: Wait for Deployment (1-2 minutes)

GitHub will automatically deploy your site. You'll see:
- ✅ "Your site is published at https://eininnssol.github.io/final-first-contact-e-i-s/"

### Step 3: Your Live URL

Your demo will be live at:
```
https://eininnsol.github.io/final-first-contact-e-i-s/
```

The QR code on the landing page will **automatically update** to point to this URL!

### Step 4: Print the QR Code

1. Open the live URL
2. The QR code will display on the landing page
3. Right-click the QR code → "Save image as..."
4. Print it for your presentation!

---

## Option 2: Vercel (Also Easy - FREE)

### Quick Deploy:

1. Go to: https://vercel.com/new
2. Import your GitHub repo: `EinInnSol/final-first-contact-e-i-s`
3. Select branch: `claude/create-hifi-demo-01ABeQ16xeaERkuc6DzzVASY`
4. Click **Deploy**
5. Done! You'll get a URL like: `https://first-contact-eis-xxx.vercel.app`

---

## Option 3: Netlify (Also Easy - FREE)

### Quick Deploy:

1. Go to: https://app.netlify.com/drop
2. Drag and drop your entire project folder
3. Done! You'll get a URL like: `https://amazing-demo-123456.netlify.app`
4. You can customize the URL in Netlify settings

---

## After Deployment:

### ✅ What Works:

1. **The QR code automatically generates** pointing to your live URL
2. **Scan it with your phone** - it opens the demo
3. **Print it for presentations** - people can scan it live
4. **Share the URL** - send to city officials
5. **Works on any device** - phone, tablet, desktop

### 🎯 For Your Presentation:

**Option A: Scan Live**
- Print the QR code
- During presentation, have someone scan it with their phone
- They see the client onboarding flow live
- You show the caseworker/city views on the big screen

**Option B: Click Through**
- Open the URL on your laptop
- Connect to projector
- Click "Start Guided Demo"
- Walk through the workflow

### 📱 Custom Domain (Optional):

If you want a custom domain like `firstcontacteis-demo.com`:

**GitHub Pages:**
1. Buy domain from Namecheap, Google Domains, etc.
2. In GitHub Settings → Pages → Custom domain
3. Enter your domain
4. Update DNS records (GitHub will tell you how)

**Vercel/Netlify:**
- Even easier - just add your domain in their dashboard

---

## 🖨️ Printing the QR Code

### Best Practices:

1. **Size**: Print at least 3" x 3" (bigger is better)
2. **Quality**: Use high-quality printer or print shop
3. **Test**: Scan the printed QR code before your presentation
4. **Backup**: Have a shortened URL as backup (bit.ly)

### Create Business Cards:

Print QR code business cards to hand out:
```
┌─────────────────────────┐
│  First Contact EIS      │
│  [QR CODE HERE]         │
│                         │
│  Scan to see the demo   │
│  Long Beach Pilot       │
└─────────────────────────┘
```

---

## 📊 Track Demo Views (Optional)

Add Google Analytics:

1. Get Google Analytics tracking ID
2. Add this to index.html before `</head>`:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

Then you can see:
- How many people viewed the demo
- Which portals they explored
- How long they spent
- What devices they used

---

## 🔗 URL Shortener (Recommended)

Create a short URL for easier sharing:

**Using bit.ly:**
1. Go to https://bit.ly
2. Paste your long GitHub Pages URL
3. Create short URL: `bit.ly/firstcontacteis`
4. Use this for sharing (easier to type/remember)

---

## ✅ Deployment Checklist:

- [ ] Deployed to GitHub Pages (or Vercel/Netlify)
- [ ] Confirmed live URL works
- [ ] QR code displays correctly
- [ ] Tested QR code scanning with phone
- [ ] Printed QR code for presentation
- [ ] Created short URL for easy sharing
- [ ] Tested on mobile device
- [ ] Tested on desktop
- [ ] Tested workflow (Guided Demo)
- [ ] Tested navigation (Explore mode)

---

## 🆘 Troubleshooting:

**QR code not showing:**
- Wait 30 seconds after page loads
- Check browser console for errors
- Make sure qrcode.min.js library loaded

**GitHub Pages not deploying:**
- Check repository is public (or have GitHub Pro for private)
- Verify branch name is correct
- Wait 2-3 minutes for first deployment

**QR code not scanning:**
- Print larger (min 3" x 3")
- Ensure high contrast (black on white)
- Test with multiple phones/QR scanner apps
- Verify URL is correct

---

## 🎉 You're Done!

Once deployed, you have:
- ✅ Live demo URL that works anywhere
- ✅ QR code that people can scan
- ✅ Professional presentation tool
- ✅ Shareable link for city officials
- ✅ Mobile-friendly experience

**Go crush that presentation!** 🚀
