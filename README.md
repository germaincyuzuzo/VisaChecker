# Visa Entry Checker

A comprehensive web application that provides instant visa requirement information between any two countries. This application combines multiple free APIs to deliver detailed visa requirements, necessary documents, and country information.


## Overview

The Visa Entry Checker is a practical travel application that helps users understand visa requirements for international travel. Instead of manually researching embassies and government websites, users can simply enter their passport country and destination to receive comprehensive visa information in seconds.

**Problem Solved:** Travelers often struggle to find accurate, up-to-date visa requirements information scattered across multiple sources. This application consolidates that information into one easy-to-use interface.

## Features

### Core Features

- **Single Destination Check** - Get visa requirements for one destination
- **Visa Status Information** - Know if you need a visa, visa-free access, visa-on-arrival, or e-visa
- **Maximum Stay Duration** - See how long you can stay without a visa
- **Essential Documents List** - Get a comprehensive list of required documents based on visa type
- **Country Information** - View capital, region, currency, and languages
- **Smart Caching** - Reduced API calls for repeated queries
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **Error Handling** - Gracefully manages invalid inputs and API errors

### Visa Type Classifications

- **Visa Free** - No visa required for entry
- **Visa on Arrival** - Visa obtained upon arrival at border
- **e-Visa** - Electronic visa obtained online before travel
- **Visa Required** - Standard visa required before travel

## Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Requests** - HTTP library for API calls

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (with responsive design)
- **JavaScript (Vanilla)** - Client-side logic and interactivity

### External APIs
- **Passport Visa API** (https://rough-sun-2523.fly.dev) - Visa requirements data
- **REST Countries API** (https://restcountries.com) - Country information

### Deployment
- **Apache/Nginx** - Web servers
- **HAProxy** - Load balancer
- **Linux** - Server OS

## Project Structure

```
visa-checker/
├── app.py                          
├── templates/
│   └── index.html                  
├── static/                         
├── requirements.txt                
├── README.md                       
├── .env.example                    

```

## Prerequisites

- **Python 3.8+** installed
- **pip** (Python package manager)
- **Internet connection** (for API calls)
- For deployment: Linux servers with sudo access

## Local Installation

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/germaincyuzuzo/VisaChecker.git
cd visa-checker
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Environment File

```bash
cp .env.example .env
# Edit .env if needed (currently no API keys required)
```

### Step 5: Verify Installation

```bash
# Check if all packages are installed
pip list
```

## Running the Application

### Local Development

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

### Testing the Application

1. Open your browser to `http://localhost:5000`
2. Enter passport country code: `US`
3. Enter destination country code: `JP`
4. Click "Check Visa"
5. View the comprehensive visa information

## API Integration

### Passport Visa API

**Endpoint:** `https://rough-sun-2523.fly.dev/visa/{passport}/{destination}`

**Example Request:**
```
GET https://rough-sun-2523.fly.dev/visa/US/JP
```

**Example Response:**
```json
{
  "passport": {
    "code": "US",
    "name": "United States"
  },
  "destination": {
    "code": "JP",
    "name": "Japan"
  },
  "category": {
    "name": "Visa Free",
    "code": "VF"
  },
  "dur": 90,
  "last_updated": "2024-12-15"
}
```

### REST Countries API

**Endpoint:** `https://restcountries.com/v3.1/alpha/{country_code}`

**Used for:** Capital, region, currency, languages, and population data

## Deployment Guide

### Part 1: Prepare Servers

#### On Each Server (Web01, Web02)

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv -y

# Install Nginx
sudo apt install nginx -y

# Create application directory
sudo mkdir -p /var/www/visa-checker
cd /var/www/visa-checker

# Clone application
sudo git clone https://github.com/yourusername/visa-checker.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service file
sudo nano /etc/systemd/system/visa-checker.service
```

#### Systemd Service File (`/etc/systemd/system/visa-checker.service`)

```ini
[Unit]
Description=Visa Entry Checker Flask Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/visa-checker
Environment="PATH=/var/www/visa-checker/venv/bin"
ExecStart=/var/www/visa-checker/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable visa-checker
sudo systemctl start visa-checker
sudo systemctl status visa-checker
```

#### Configure Nginx as Reverse Proxy

**File:** `/etc/nginx/sites-available/visa-checker`

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Enable Nginx Site

```bash
sudo ln -s /etc/nginx/sites-available/visa-checker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Part 2: Configure Load Balancer (Lb01)

#### Install HAProxy

```bash
sudo apt update
sudo apt install haproxy -y
```

#### Configure HAProxy

**File:** `/etc/haproxy/haproxy.cfg`

```
global
    log stdout local0
    log stdout local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    log global

frontend visa_checker_frontend
    bind *:80
    default_backend visa_checker_backend
    option httplog
    option forwardfor

backend visa_checker_backend
    balance roundrobin
    option httpchk GET / HTTP/1.1\r\nHost:\ localhost
    server web01 <WEB01_IP>:80 check inter 5s rise 2 fall 2
    server web02 <WEB02_IP>:80 check inter 5s rise 2 fall 2
```

Replace `<WEB01_IP>` and `<WEB02_IP>` with your actual server IP addresses.

#### Verify and Start HAProxy

```bash
sudo haproxy -f /etc/haproxy/haproxy.cfg -c
sudo systemctl restart haproxy
sudo systemctl status haproxy
```

## Load Balancer Configuration

### How It Works

```
                    ┌──────────────────┐
                    │   Users          │
                    │  (Browser)       │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Load Balancer   │
                    │    (Lb01)        │
                    │   Port 80        │
                    └────────┬─────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼────────┐       ┌───────▼────────┐
        │    Web01       │       │    Web02       │
        │   Port 80      │       │   Port 80      │
        │  (Nginx →      │       │  (Nginx →      │
        │  Flask:5000)   │       │  Flask:5000)   │
        └────────────────┘       └────────────────┘
```

### Load Balancing Algorithm

**Round Robin:** Requests are distributed equally between Web01 and Web02

**Example:**
- Request 1 → Web01
- Request 2 → Web02
- Request 3 → Web01
- Request 4 → Web02

### Health Checks

HAProxy checks server health every 5 seconds:
- **Rise 2:** Mark as UP after 2 successful checks
- **Fall 2:** Mark as DOWN after 2 failed checks

### Sticky Sessions (if needed)

Add to HAProxy config for session persistence:

```
cookie SERVERID insert indirect nocache
backend visa_checker_backend
    balance roundrobin
    cookie SERVERID rewrite
    server web01 <WEB01_IP>:80 check cookie web01
    server web02 <WEB02_IP>:80 check cookie web02
```

## Testing

### Local Testing

```bash
# Start the application
python app.py

# Test with curl
curl -X POST http://localhost:5000/api/check-visa \
  -H "Content-Type: application/json" \
  -d '{"passport": "US", "destination": "JP"}'
```

### Load Balancer Testing

```bash
# Test load balancer distribution
for i in {1..10}; do
    curl http://<LB_IP>/
done

# Check which server handled each request (look at server logs)
# Web01: sudo tail -f /var/log/nginx/access.log
# Web02: sudo tail -f /var/log/nginx/access.log
```

### Verify Traffic Distribution

Monitor both servers to confirm traffic is balanced:

**On Web01:**
```bash
sudo tail -f /var/log/nginx/access.log
```

**On Web02:**
```bash
sudo tail -f /var/log/nginx/access.log
```

Both logs should show incoming requests.

### Load Testing (Optional)

```bash
# Install Apache Bench
sudo apt install apache2-utils -y

# Simulate 1000 requests with 10 concurrent connections
ab -n 1000 -c 10 http://<LB_IP>/

# Monitor load balancer stats
curl http://<LB_IP>:8404/stats  # If stats page enabled
```

## Troubleshooting

### Application won't start

```bash
# Check Python version
python3 --version

# Check if port 5000 is in use
lsof -i :5000

# Check Flask logs
python app.py
```

### 503 Bad Gateway Error

```bash
# Check if Flask is running
sudo systemctl status visa-checker

# Restart Flask service
sudo systemctl restart visa-checker

# Check Nginx config
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### API Returns No Data

```bash
# Check internet connection
ping rough-sun-2523.fly.dev
ping restcountries.com

# Check firewall rules
sudo ufw status

# Allow HTTPS if needed
sudo ufw allow 443
```

### Load Balancer Not Distributing Traffic

```bash
# Check HAProxy status
sudo systemctl status haproxy

# Check HAProxy config
sudo haproxy -f /etc/haproxy/haproxy.cfg -c

# View HAProxy stats
sudo tail -f /var/log/haproxy.log

# Restart HAProxy
sudo systemctl restart haproxy
```

## Credits

### APIs Used

- **Passport Visa API** - Free Passport Visa API (https://github.com/nickypangers/passport-visa-api)
- **REST Countries API** - Country information data (https://restcountries.com)

### Documenting

- claude.ai

### Technologies

- Flask - Web framework
- Nginx - Web server & reverse proxy
- HAProxy - Load balancer
- Python - Backend programming language

## License

This project is open source and available under the MIT License.

## Author

- **Name:** Germain Cyuzuzo
- **Email:** germaincyuzuzo1@gmail.com
- **GitHub:** https://github.com/germaincyuzuzo

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


**Last Updated:** December 2024

**Application Version:** 1.0.0

**Status:** Production Ready