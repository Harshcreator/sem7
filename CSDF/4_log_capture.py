import logging
import argparse
from datetime import datetime, timedelta

LOG_FILE = 'app.log'

def setup_logger():
    """Configure logging to file and console."""
    logger = logging.getLogger('EventLogger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # File handler
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

def generate_sample_logs(logger):
    """Generate sample log messages of various severity levels."""
    logger.debug("Debugging the application.")
    logger.info("Application started successfully.")
    logger.warning("Low disk space warning.")
    logger.error("Failed to connect to database.")
    logger.critical("System crash imminent!")
    logger.warning("Recovered from error.")
    logger.info("Routine check completed.")

def parse_log_line(line):
    """Parse a log line into timestamp, level, and message."""
    try:
        parts = line.strip().split(' ', 2)
        timestamp_str = parts[0] + ' ' + parts[1]
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
        level, message = parts[2].split(' ', 1)
        return timestamp, level, message
    except Exception:
        return None, None, None

def correlate_events(time_window=5):
    """
    Read the log file and correlate events:
    - Events within 'time_window' seconds of each other.
    - Severity correlation: ERROR followed by WARNING, etc.
    """
    correlated = []
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    events = []
    for line in lines:
        timestamp, level, message = parse_log_line(line)
        if timestamp:
            events.append({'timestamp': timestamp, 'level': level, 'message': message})

    # Correlate events based on time proximity and severity
    for i in range(len(events) - 1):
        curr = events[i]
        next_ev = events[i + 1]
        # Time proximity
        if (next_ev['timestamp'] - curr['timestamp']) <= timedelta(seconds=time_window):
            # Severity pattern: ERROR followed by WARNING
            if curr['level'] == 'ERROR' and next_ev['level'] == 'WARNING':
                correlated.append((curr, next_ev))
            # Or any two events within the window
            elif curr['level'] != next_ev['level']:
                correlated.append((curr, next_ev))

    # Print correlated events
    print(f"\nCorrelated Events (within {time_window} seconds):")
    for pair in correlated:
        for ev in pair:
            print(f"{ev['timestamp']} {ev['level']}: {ev['message']}")
        print('-' * 40)

def main():
    parser = argparse.ArgumentParser(description="Log capture and event correlation tool")
    parser.add_argument('--generate', action='store_true', help='Generate sample logs')
    parser.add_argument('--correlate', action='store_true', help='Correlate events in the log file')
    parser.add_argument('--window', type=int, default=5, help='Time window (seconds) for correlation')
    args = parser.parse_args()

    logger = setup_logger()

    if args.generate:
        generate_sample_logs(logger)
        print(f"Sample logs generated in {LOG_FILE}")

    if args.correlate:
        correlate_events(time_window=args.window)

if __name__ == "__main__":
    main()

# Steps:
# 1. Set up logging to file and console.
# 2. Provide CLI to generate logs or correlate events.
# 3. Parse log file, correlate events by time and severity.
# 4. Print correlated event pairs with timestamps and severity.