# RESTORE GUIDE — If VPS Goes Down

Last backup: 2026-06-04

## What's Backed Up (GitHub)
Repo: https://github.com/arturo7gonzalez7-viora/Viora-

Everything is there:
- All workspace files (MEMORY.md, SOUL.md, scripts, CRM, etc.)
- memory/ folder (all daily logs)
- openclaw-memory-backup/ (SQLite memory database)
- All Viora, FlipRight, Casa Mariachi, trading files

## To Restore on New VPS

1. Install OpenClaw fresh on new server
2. Clone the repo into the workspace:
   ```
   cd /root/.openclaw/
   git clone https://github.com/arturo7gonzalez7-viora/Viora-.git workspace
   ```
3. Copy memory database back:
   ```
   cp workspace/openclaw-memory-backup/main.sqlite memory/
   ```

## Keys You'll Need to Re-enter
(Keep these somewhere safe — NOT on GitHub)
- Anthropic API key (Claude)
- Discord bot token
- Retell AI key
- Vercel token: vcp_4xZ5GTvJMgBbiHQs65wqDgW7BSNW6pbMATHB9SSQzq6AGkzcjB0FCTdJ

## Viora Deploy
- Auto-deploys from GitHub to Vercel on push
- URL: https://viora-deploy.vercel.app

## Discord Channels
Discord messages live on Discord's servers — they don't disappear when VPS goes down.
Jarvis won't respond while VPS is offline, but history is all still there.
