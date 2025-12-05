# Snake (Web Version) — Deployable to Render

This folder contains a web version of Snake (HTML/CSS/JS) that can be deployed as a static site on Render.

Files added:
- `index.html` — game UI & canvas
- `style.css` — styling
- `snake.js` — JavaScript game logic

Preview locally
----------------
Quick preview with Python's simple HTTP server (PowerShell):

```powershell
cd "C:\all projects\pygame"
python -m http.server 8000
# then open http://localhost:8000/index.html in your browser
```

Or just open `index.html` directly in your browser (recommended to use the HTTP server for consistent behavior).

Deploy to Render (Static Site)
------------------------------
1. Create a new GitHub repository and push this folder (`snake/`) to it (or push this folder's contents to the repo root).

2. In Render:
   - New → Static Site
   - Connect your GitHub repo
   - Build Command: (leave empty)
   - Publish Directory: `/` (or the directory where `index.html` is located)
   - Click Create — Render will build and publish the static site.

3. Visit the generated Render URL — your Snake game will be live.

Optional improvements
---------------------
- Add `CNAME` or custom domain via Render settings.
- Add compression and image assets.
- Add scoreboard backend (if you want server-side high-score persistence).

Need help pushing to GitHub or composing a repo? Tell me and I will provide exact git commands and a ready `.gitignore`.