# TOOLS.md - Local Notes

## VPS / Hosting
- **Hostinger VPS**: srv1342183.hstgr.cloud, IP 31.97.7.46, KVM 2, expires 2026-03-06
- **Inbound ports blocked** by Hostinger's network — SSH and direct port access don't work from outside
- **Dashboard access**: via Cloudflare quick tunnel (systemd service: `cloudflared-tunnel`)
- **To get dashboard URL**: `journalctl -u cloudflared-tunnel --no-pager -n 20 | grep trycloudflare`
- **Token**: stored in openclaw.json gateway.auth.token
- **URL format**: `https://<tunnel-url>/#token=<token>`

## ⚠️ CRITICAL: Gateway Port Configuration
- **Gateway always runs on port 18789** (actual runtime port)
- **Config file (openclaw.json) MUST have gateway.port set to 18789**
- If port mismatch (config says 443 but runs on 18789), Chrome extension can't connect
- **Always verify**: `ss -tlnp | grep 18789` to confirm gateway is listening
- **If extension says "ON" but dashboard can't see tab**: check port mismatch first
- **Fix with**: `gateway config.patch` to set `{"gateway":{"port":18789}}`

## Dashboard Quick Access
When Arturo asks for the dashboard link:
1. Grab tunnel URL from journalctl
2. Grab token from config
3. Send combined URL with `#token=`

## Browser Relay / Chrome Extension
- Extension must be clicked ON while on the target tab (Google Sheets, etc.)
- Dashboard shows "tab connected" only when port config matches actual runtime port
- If connection fails despite extension being ON: restart gateway and verify port config
