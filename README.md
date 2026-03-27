# MCU Chronological Watch Order 🛡️

A premium, interactive web application designed to track the entire **Marvel Cinematic Universe** in strict chronological (story-wise) order. From Captain America in the 1940s all the way through the Multiverse Saga!

## ✨ Features
* **True Chronological Timeline**: Organized perfectly by in-universe set dates rather than theatrical release dates to "connect all the dots."
* **Smart Download Links**: Includes options to easily access torrent pages or direct Magnet Links.
* **Live Magnet Health Tracking**: Every magnet link is paired with an intuitive 4-tier Health Badge (🟢 Best, 🔵 Better, 🟡 Good, 🔴 Bad) indicating download speed efficiency.
* **Immersive UI/UX**: Built entirely utilizing Vanilla JS, HTML, and CSS with a stunning dark-mode "glassmorphism" aesthetic, glowing ambient orbs, and beautiful typography.

## 🛠️ The Health Checker (`update_health.py`)
This project includes a built-in Python script that dynamically connects to the BitTorrent network to scan the swarm metadata of every magnet link in the database. 

It checks the exact number of **Seeds** and **Peers** without downloading any video files, scores the health from Red to Green, and automatically injects that live status directly back into the application's `movies.js` file for users to see.

### How to use the Health Checker:
```bash
# 1. Install the libtorrent library
pip3 install libtorrent

# 2. Run the script
python3 update_health.py

# 3. Commit and push your updated movies.js!
```

## 🚀 Deployment
This repository is configured for instantaneous deployment via **Vercel**. Any updates to `movies.js` (such as adding new movies or updating health markers via the Python script) will be deployed globally within seconds of a `git push`.
