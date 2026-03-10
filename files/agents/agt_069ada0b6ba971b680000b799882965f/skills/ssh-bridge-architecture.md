---
name: ssh-bridge-architecture
description: SSH tunnel architecture, reverse tunnel setup, and ephemeral execution workarounds for Nebula-to-EC2 bridges. Use when setting up, diagnosing, or maintaining SSH tunnels, reverse tunnels, or remote CLI relay sessions.
created_at: 2026-03-08T16:15:50.743794+00:00
updated_at: 2026-03-08T16:15:50.743794+00:00
---

# SSH Bridge Architecture — Nebula <-> EC2

## Environment
- Remote box: AWS EC2 running OpenClaw 2026.2.1
- Nebula execution model: ephemeral sandbox (~60 second max connection lifetime)
- Goal: Relay CLI commands from Nebula to the remote EC2 box reliably

---

## Core Problem: Ephemeral Execution
Nebula code cells spin up isolated sandboxes. Long-lived SSH sessions die when the
cell exits. This means:
- A blocking `ssh host "command"` call works fine (short, fire-and-forget)
- Long-running daemons or interactive sessions CANNOT be held open from inside Nebula
- Reverse SSH tunnels initiated FROM the EC2 box (pointing back to a relay) survive
  because they are owned by the remote process, not Nebula

---

## Reverse Tunnel Pattern (Recommended)

The EC2 box opens the tunnel TO a relay endpoint. Nebula then connects to the relay
to issue commands. The tunnel lives as long as the EC2 process does.

### EC2 side (run on the remote box — persistent):
```bash
# Keep a reverse tunnel alive from EC2 -> relay
autossh -M 0 -N -R 2222:localhost:22 user@relay-host \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes
```

### Nebula side (short-lived cell):
```bash
ssh -p 2222 ec2-user@relay-host "your-command-here"
```

This way Nebula's cell only needs to survive long enough to fire the command and read stdout.

---

## Polling Loop Pattern (for long tasks)

When a remote task runs longer than ~60s, offload it to a background process on EC2
and poll for results via a status file or API endpoint.

### EC2 — run task in background, write status:
```bash
nohup bash -c 'your-long-task > /tmp/task.log 2>&1; echo done > /tmp/task.status' &
```

### Nebula — short poll cells (run repeatedly):
```bash
ssh ec2-user@host "cat /tmp/task.status 2>/dev/null || echo running"
ssh ec2-user@host "tail -20 /tmp/task.log"
```

Each poll cell is well within the 60s window.

---

## CLI Command Relay Pattern

Use a named pipe or a small relay server on EC2 to accept commands from Nebula.

### Lightweight relay server on EC2 (Python):
```python
# relay_server.py — run persistently on EC2
import socket, subprocess, threading

def handle(conn):
    cmd = conn.recv(4096).decode().strip()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    conn.sendall((result.stdout + result.stderr).encode())
    conn.close()

s = socket.socket()
s.bind(('0.0.0.0', 9922))
s.listen(5)
while True:
    conn, _ = s.accept()
    threading.Thread(target=handle, args=(conn,)).start()
```

### Nebula side — send a command:
```python
import socket
s = socket.socket()
s.connect(('ec2-host', 9922))
s.sendall(b'ls -la /home/ec2-user')
print(s.recv(65536).decode())
s.close()
```

---

## SSH Key Setup (one-time)
```bash
# On Nebula — generate ephemeral key if needed
ssh-keygen -t ed25519 -f /tmp/nebula_key -N ""
# Copy public key to EC2's authorized_keys (do once via console or existing access)
```

Store the private key as a Nebula secret (NEBULA_SSH_KEY) and write it to /tmp at
the start of each cell:
```python
import os
os.makedirs('/tmp/.ssh', exist_ok=True)
with open('/tmp/.ssh/nebula_key', 'w') as f:
    f.write(os.environ['NEBULA_SSH_KEY'])
os.chmod('/tmp/.ssh/nebula_key', 0o600)
```

---

## OpenClaw 2026.2.1 Notes
- OpenClaw runs on the EC2 instance as the primary workload
- SSH bridge is the control plane for issuing commands to OpenClaw CLI
- Typical commands: status checks, config reloads, log tailing, restart triggers

---

## Tunnel Health Check (run in any Nebula cell)
```bash
ssh -o ConnectTimeout=5 -o BatchMode=yes ec2-user@host "echo pong" 2>&1
```
Exit code 0 = tunnel alive. Non-zero = tunnel dead, needs re-establishment from EC2 side.

---

## autossh Keepalive (EC2 systemd service)
Create /etc/systemd/system/nebula-tunnel.service on EC2:
```ini
[Unit]
Description=Nebula Reverse SSH Tunnel
After=network.target

[Service]
User=ec2-user
ExecStart=/usr/bin/autossh -M 0 -N \
  -R 2222:localhost:22 user@relay \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable --now nebula-tunnel
```
