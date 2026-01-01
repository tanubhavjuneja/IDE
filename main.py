import random
import datetime
import os

# Define some sample data for the log files
ip_addresses = ["192.168.1.{}".format(i) for i in range(1, 101)]
endpoints = ["/home", "/about", "/contact", "/products", "/services", "/login", "/signup"]
http_methods = ["GET", "POST", "PUT", "DELETE"]
status_codes = [200, 301, 400, 404, 500]
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36"
]

# Define a function to generate Apache log format
def generate_apache_log():
    ip_address = random.choice(ip_addresses)
    timestamp = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S +0000')
    method = random.choice(http_methods)
    endpoint = random.choice(endpoints)
    status_code = random.choice(status_codes)
    user_agent = random.choice(user_agents)
    log_entry = f'{ip_address} - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status_code} 1234 "{user_agent}"\n'
    return log_entry

# Define a function to generate Nginx log format
def generate_nginx_log():
    ip_address = random.choice(ip_addresses)
    timestamp = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S +0000')
    method = random.choice(http_methods)
    endpoint = random.choice(endpoints)
    status_code = random.choice(status_codes)
    user_agent = random.choice(user_agents)
    log_entry = f'{ip_address} - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status_code} 456 "{user_agent}"\n'
    return log_entry

# Define a function to generate IIS log format
def generate_iis_log():
    ip_address = random.choice(ip_addresses)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    method = random.choice(http_methods)
    endpoint = random.choice(endpoints)
    status_code = random.choice(status_codes)
    user_agent = random.choice(user_agents)
    log_entry = f'{timestamp} {ip_address} GET {endpoint} HTTP/1.1 {status_code} {random.randint(1000, 2000)} "{user_agent}"\n'
    return log_entry

# Function to create log files
def create_log_files():
    # Directory to save log files
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # Apache log file
    with open(os.path.join(log_dir, 'apache_log.txt'), 'w') as apache_log:
        for _ in range(50):
            apache_log.write(generate_apache_log())
    print("Apache log file created with 50 entries.")

    # Nginx log file
    with open(os.path.join(log_dir, 'nginx_log.txt'), 'w') as nginx_log:
        for _ in range(50):
            nginx_log.write(generate_nginx_log())
    print("Nginx log file created with 50 entries.")

    # IIS log file
    with open(os.path.join(log_dir, 'iis_log.txt'), 'w') as iis_log:
        for _ in range(50):
            iis_log.write(generate_iis_log())
    print("IIS log file created with 50 entries.")

# Run the function to generate the logs
if __name__ == "__main__":
    create_log_files()
