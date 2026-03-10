---
name: openclaw-remote-ops
description: OpenClaw 2026.2.1 remote operation patterns via SSH bridge. Use when issuing commands to OpenClaw on EC2, checking its status, reloading config, or interpreting its log output through the SSH relay.
created_at: 2026-03-08T16:15:51.118671+00:00
updated_at: 2026-03-08T16:15:51.118671+00:00
---

# OpenClaw 2026.2.1 — Remote Operations via SSH Bridge

## Context
OpenClaw 2026.2.1 runs on an AWS EC2 instance. Nebula controls it via SSH relay.
All commands below assume a working SSH connection (see ssh-bridge-architecture skill).

---

## Common SSH Invocation Pattern
```python
import subprocess

SSH_CMD = [
    "ssh",
    "-i", "/tmp/.ssh/nebula_key",
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=10",
    "ec2-user@YOUR_EC2_HOST"
]

def remote(cmd: str) -> str:
    result = subprocess.run(SSH_CMD + [cmd], capture_output=True, text=True, timeout=50)
    return result.stdout + result.stderr
```

---

## Health & Status Checks
```bash
# Is OpenClaw running?
pgrep -a openclaw || systemctl status openclaw

# Tail recent logs
journalctl -u openclaw -n 50 --no-pager
# or if file-based:
tail -50 /var/log/openclaw/openclaw.log

# Version confirm
openclaw --version
```

---

## Config Reload (no restart)
```bash
openclaw reload
# or send SIGHUP if reload CLI not available:
pkill -HUP -x openclaw
```

---

## Restart
```bash
sudo systemctl restart openclaw
# Verify it came back up:
sleep 3 && systemctl is-active openclaw
```

---

## Log Monitoring via Poll Loop
Since Nebula cells are ephemeral, monitor logs by polling:

```python
# Cell 1: kick off a log-watch task on EC2
remote("tail -f /var/log/openclaw/openclaw.log > /tmp/oc_watch.log 2>&1 & echo $! > /tmp/oc_watch.pid")

# Cell 2 (run after a delay): read buffered output
remote("cat /tmp/oc_watch.log")

# Cell N: stop the watcher
remote("kill $(cat /tmp/oc_watch.pid) 2>/dev/null; rm -f /tmp/oc_watch.pid /tmp/oc_watch.log")
```

---

## File Transfer (EC2 <-> Nebula)
```python
import subprocess

# Download file from EC2 to Nebula /tmp
subprocess.run([
    "scp", "-i", "/tmp/.ssh/nebula_key",
    "-o", "StrictHostKeyChecking=no",
    "ec2-user@HOST:/remote/path/file.txt",
    "/tmp/file.txt"
], timeout=50)

# Upload file from Nebula to EC2
subprocess.run([
    "scp", "-i", "/tmp/.ssh/nebula_key",
    "-o", "StrictHostKeyChecking=no",
    "/tmp/local_file.txt",
    "ec2-user@HOST:/remote/path/"
], timeout=50)
```

---

## Environment Variables & Secrets
Store these as Nebula secrets and inject at cell start:
- NEBULA_SSH_KEY — private key for EC2 access (ed25519 recommended)
- EC2_HOST — IP or DNS of the EC2 instance
- EC2_USER — default: ec2-user (Amazon Linux) or ubuntu (Ubuntu AMI)

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Connection refused` | Reverse tunnel down | Restart autossh on EC2 |
| `Permission denied (publickey)` | Wrong key / key not in authorized_keys | Re-add public key to EC2 |
| `Timeout` | Security group blocks port 22 | Check AWS SG inbound rules |
| Command hangs | Interactive prompt waiting | Add `-o BatchMode=yes` to SSH args |
| OpenClaw not responding | Process crashed | `sudo systemctl restart openclaw` |
