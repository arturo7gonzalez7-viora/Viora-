# DISCORD CHANNEL FIX - PERMANENT SOLUTION

## Problem
New Discord channels create sessions but don't get added to OpenClaw config automatically.
**Symptom:** Bot can send TO channel but can't receive FROM channel.

## Instant Fix Command

```bash
cd /root/.openclaw
python3 -c "
import json
CHANNEL_ID='PUT_CHANNEL_ID_HERE'
with open('openclaw.json', 'r') as f: config = json.load(f)
config['channels']['discord']['accounts']['jarvis']['guilds']['1471327350187753658']['channels'][CHANNEL_ID] = {'requireMention': False}
with open('openclaw.json', 'w') as f: json.dump(config, f, indent=2)
print('Channel added successfully!')
"
```

Then restart: `gateway restart`

## Prevention
- Auto-Fix Discord Channels cron runs every 15 minutes
- Detects and fixes missing channels automatically
- **This should never be needed manually anymore**

## Last Fixed
- Trading channel 1475953649539747920 on 2026-02-24 20:44 UTC
- Solution tested and confirmed working