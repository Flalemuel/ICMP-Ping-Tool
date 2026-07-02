# ICMP Ping Tool

A lightweight, dark-themed GUI tool for pinging multiple IP addresses concurrently — built with Python and CustomTkinter.

<img width="506" height="345" alt="image" src="https://github.com/user-attachments/assets/7c8301af-35ce-4bc9-a387-5865d4e0fc34" />

---

## Overview

**ICMP Ping Tool** is a desktop application designed for network engineers who need to quickly check reachability of multiple hosts at once. It sends concurrent ICMP pings using `icmplib` and displays results in a clean, color-coded console — green for UP, red for DOWN.

---

## Features

- **Multi-target ping** — paste any number of IPs and ping them all concurrently (up to 50 simultaneous tasks)
- **Color-coded results** — green (UP), red (DOWN), amber (warnings/errors)
- **Configurable settings** — set ping packet count and timeout per run
- **Cancel support** — stop an in-progress ping session at any time
- **Live console output** — results stream in as they complete, not after
- **Summary line** — total UP / DOWN count displayed after each run
- **Dark themed UI** — GitHub-style dark interface built with CustomTkinter

---

## Requirements

- Python 3.10 or higher
- Windows (tested), Linux/macOS should work with minor adjustments for ICMP privileges

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/Flalemuel/icmp-ping-tool.git
cd icmp-ping-tool
```

**2. Install dependencies**
```bash
pip install customtkinter icmplib
```

> **Windows note:** `icmplib` in unprivileged mode (`privileged=False`) works out of the box on Windows without admin rights.
>
> **Linux/macOS note:** Unprivileged ICMP may require setting socket permissions:
> ```bash
> sudo sysctl -w net.ipv4.ping_group_range="0 2147483647"
> ```

---

## Usage

**Run the script directly:**
```bash
python ping_tool.py
```
**Alternative: run the .exe file included in this repo**


**Using the app:**

1. Enter IP addresses in the left panel — one IP per line
2. Lines starting with `#` are treated as comments and ignored
3. Set **Ping Packet Count** and **Timeout (s)** in the settings card
4. Click **▶ Run Ping** to start
5. Results appear in the right console panel in real time
6. Click **✕ Cancel** to stop mid-run
7. Click **Clear Results** to reset the console

**Example input:**
```
# Core routers
192.168.1.1
10.0.0.1

# BNG
172.16.0.104

# CSR
172.16.0.105
```

**Example output:**
```
────────────────────────────────────────────────────────────
  Ping started : 2026-06-01 10:30:00
  Targets      : 4 IPs  |  Packets: 2  |  Timeout: 1s
────────────────────────────────────────────────────────────

IP                   STATUS  AVG RTT (ms)  LOSS %
───────────────────────────────────────────────────────
192.168.1.1          UP      1.24          0%
10.0.0.1             UP      0.98          0%
172.16.0.104         DOWN    -             100%
172.16.0.105         UP      2.11          0%

───────────────────────────────────────────────────────
  Total: 4   UP: 3  DOWN: 1
```

---

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| Ping Packet Count | 2 | Number of ICMP packets sent per host |
| Timeout (s) | 1 | Seconds to wait for a reply per packet |
| Concurrent tasks | 50 | Max simultaneous pings (hardcoded) |
| Interval | 0.2s | Interval between packets (hardcoded) |

---

## Author

**Flalemuel** — [github.com/Flalemuel](https://github.com/Flalemuel)
