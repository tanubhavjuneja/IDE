import re
import pandas as pd
IP_REGEX = re.compile(r"\d+\.\d+\.\d+\.\d+")
TIMESTAMP_REGEX = re.compile(
    r"\[.*?\]|\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
)
REQUEST_REGEX = re.compile(r"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)")
STATUS_REGEX = re.compile(r"^[1-5][0-9]{2}$")
def infer_log_structure(lines, sample_size=10):
    positions = {
        "ip": None,
        "timestamp": None,
        "request": None,
        "endpoint": None,
        "status": None,
        "user_agent": None
    }
    for line in lines[:sample_size]:
        tokens = line.split()
        for i, token in enumerate(tokens):
            if positions["ip"] is None and IP_REGEX.match(token):
                positions["ip"] = i
            if positions["status"] is None and STATUS_REGEX.match(token):
                positions["status"] = i
            if positions["request"] is None and REQUEST_REGEX.match(token):
                positions["request"] = i
                if i + 1 < len(tokens):
                    positions["endpoint"] = i + 1
        quoted = re.findall(r'"([^"]*)"', line)
        if quoted:
            if positions["user_agent"] is None:
                positions["user_agent"] = -1
        if positions["timestamp"] is None:
            ts = TIMESTAMP_REGEX.search(line)
            if ts:
                positions["timestamp"] = ts.group()
    return positions
def parse_server_log(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.strip() for line in f if line.strip()]
    structure = infer_log_structure(lines)
    parsed = []
    for line in lines:
        tokens = line.split()
        quoted = re.findall(r'"([^"]*)"', line)
        entry = {
            "ip_address": None,
            "timestamp": None,
            "request_type": None,
            "endpoint": None,
            "status_code": None,
            "device_info": None
        }
        if structure["ip"] is not None and structure["ip"] < len(tokens):
            entry["ip_address"] = tokens[structure["ip"]]
        if structure["status"] is not None and structure["status"] < len(tokens):
            entry["status_code"] = tokens[structure["status"]]
        if structure["request"] is not None and structure["request"] < len(tokens):
            entry["request_type"] = tokens[structure["request"]]
        if structure["endpoint"] is not None and structure["endpoint"] < len(tokens):
            entry["endpoint"] = tokens[structure["endpoint"]]
        ts_match = TIMESTAMP_REGEX.search(line)
        if ts_match:
            entry["timestamp"] = ts_match.group().strip("[]")
        if quoted:
            entry["device_info"] = quoted[-1]
        parsed.append(entry)
    return pd.DataFrame(parsed)
if __name__ == "__main__":
    log_data = parse_server_log('logs/nginx_log.txt')
    if not log_data.empty:
        print(log_data)
    else:
        print("No logs found or the log file format is incorrect.")