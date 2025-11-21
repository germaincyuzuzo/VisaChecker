# Visa Entry Checker

A comprehensive web application that provides instant visa requirement information between any two countries. This application combines multiple free APIs to deliver detailed visa requirements, necessary documents, and country information.

## Table of Contents


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

### Technologies

- Flask - Web framework
- Nginx - Web server & reverse proxy
- HAProxy - Load balancer
- Python - Backend programming language

## License

This project is open source and available under the MIT License.

## Author

- **Name:** Gemain Cyuzuzo
- **Email:** germaincyuzuzo1@gmail.com
- **GitHub:** https://github.com.germaincyuzuzo

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


**Last Updated:** December 2024

**Application Version:** 1.0.0

**Status:** Production Ready