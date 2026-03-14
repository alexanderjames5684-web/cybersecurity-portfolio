import re
import time
import json
import datetime
from collections import defaultdict

# ── Configuration ─────────────────────────────────────────
LOG_FILE = "/home/aj/sample_auth.log"
ALERT_THRESHOLD = 3      # Failed attempts before alert
TIME_WINDOW = 60         # Seconds to track attempts in
CHECK_INTERVAL = 2       # How often to check log (seconds)
BLOCK_THRESHOLD = 5      # Failed attempts before IP is blocked

# ── Data Storage ──────────────────────────────────────────
failed_attempts = defaultdict(list)  # ip -> [timestamps]
blocked_ips = set()
alerts_log = []

def print_banner():
    print("\n" + "="*55)
    print("      REAL-TIME BRUTE FORCE DETECTION SYSTEM")
    print("="*55)
    print(f"  Log File       : {LOG_FILE}")
    print(f"  Alert Threshold: {ALERT_THRESHOLD} attempts")
    print(f"  Time Window    : {TIME_WINDOW} seconds")
    print(f"  Block Threshold: {BLOCK_THRESHOLD} attempts")
    print(f"  Started        : {datetime.datetime.now()}")
    print("="*55)
    print("  [*] Monitoring for suspicious activity...")
    print("  [*] Press CTRL+C to stop and save report\n")

def parse_line(line):
    """Extract timestamp, status, user, and IP from a log line."""
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (FAILED LOGIN|SUCCESSFUL LOGIN) user=(\w+) ip=([\d.]+)'
    match = re.search(pattern, line)
    if match:
        return {
            "timestamp": match.group(1),
            "status": match.group(2),
            "user": match.group(3),
            "ip": match.group(4)
        }
    return None

def check_brute_force(ip, timestamp):
    """Check if an IP has exceeded the threshold within the time window."""
    now = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    # Add this attempt to the IP's history
    failed_attempts[ip].append(now)

    # Only keep attempts within the time window
    cutoff = now - datetime.timedelta(seconds=TIME_WINDOW)
    failed_attempts[ip] = [t for t in failed_attempts[ip] if t > cutoff]

    attempt_count = len(failed_attempts[ip])

    # Check if IP should be blocked
    if attempt_count >= BLOCK_THRESHOLD and ip not in blocked_ips:
        blocked_ips.add(ip)
        alert = {
            "level": "CRITICAL",
            "time": str(now),
            "ip": ip,
            "attempts": attempt_count,
            "message": f"IP {ip} BLOCKED — exceeded {BLOCK_THRESHOLD} attempts in {TIME_WINDOW}s"
        }
        alerts_log.append(alert)
        print(f"  🚫 CRITICAL — IP {ip} BLOCKED after {attempt_count} attempts!")
        return

    # Check if IP has hit alert threshold
    if attempt_count >= ALERT_THRESHOLD and ip not in blocked_ips:
        alert = {
            "level": "WARNING",
            "time": str(now),
            "ip": ip,
            "attempts": attempt_count,
            "message": f"Possible brute force from {ip} — {attempt_count} attempts in {TIME_WINDOW}s"
        }
        alerts_log.append(alert)
        print(f"  ⚠️  WARNING  — {ip} has {attempt_count} failed attempts in {TIME_WINDOW}s")

def monitor_log():
    """Main monitoring loop — reads log and processes each line."""
    print_banner()

    processed_lines = 0
    total_failed = 0
    total_success = 0

    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()

        print(f"  [*] Processing {len(lines)} existing log entries...\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            entry = parse_line(line)
            if not entry:
                continue

            processed_lines += 1

            if entry["status"] == "FAILED LOGIN":
                total_failed += 1

                # Skip if IP is already blocked
                if entry["ip"] in blocked_ips:
                    print(f"  🚫 BLOCKED IP activity: {entry['ip']} "
                          f"still attempting as user '{entry['user']}'")
                    continue

                print(f"  [-] Failed login — user='{entry['user']}' "
                      f"ip={entry['ip']} at {entry['timestamp']}")

                check_brute_force(entry["ip"], entry["timestamp"])

            elif entry["status"] == "SUCCESSFUL LOGIN":
                total_success += 1

                # Flag successful login from a blocked IP
                if entry["ip"] in blocked_ips:
                    alert = {
                        "level": "CRITICAL",
                        "time": entry["timestamp"],
                        "ip": entry["ip"],
                        "user": entry["user"],
                        "message": f"CRITICAL — Successful login from BLOCKED IP {entry['ip']} as '{entry['user']}'"
                    }
                    alerts_log.append(alert)
                    print(f"\n  🚨 CRITICAL — Successful login from BLOCKED IP "
                          f"{entry['ip']} as '{entry['user']}'!\n")
                else:
                    print(f"  [+] Successful login — user='{entry['user']}' "
                          f"ip={entry['ip']} at {entry['timestamp']}")

            # Small delay to simulate real-time monitoring
            time.sleep(CHECK_INTERVAL * 0.1)

    except KeyboardInterrupt:
        pass

    # ── Final Report ─────────────────────────────────────
    print("\n" + "="*55)
    print("                 DETECTION SUMMARY")
    print("="*55)
    print(f"  Log lines processed  : {processed_lines}")
    print(f"  Failed login attempts: {total_failed}")
    print(f"  Successful logins    : {total_success}")
    print(f"  Total alerts raised  : {len(alerts_log)}")
    print(f"  IPs blocked          : {len(blocked_ips)}")

    if blocked_ips:
        print(f"\n  Blocked IPs:")
        for ip in blocked_ips:
            print(f"    🚫 {ip}")

    # Save report
    report = {
        "scan_time": str(datetime.datetime.now()),
        "log_file": LOG_FILE,
        "configuration": {
            "alert_threshold": ALERT_THRESHOLD,
            "time_window_seconds": TIME_WINDOW,
            "block_threshold": BLOCK_THRESHOLD
        },
        "summary": {
            "lines_processed": processed_lines,
            "failed_logins": total_failed,
            "successful_logins": total_success,
            "total_alerts": len(alerts_log),
            "blocked_ips": list(blocked_ips)
        },
        "alerts": alerts_log
    }

    filename = f"brute_force_report_{datetime.date.today()}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=4)

    print(f"\n  [*] Report saved to: {filename}")
    print("="*55 + "\n")

# Run the detector
monitor_log()