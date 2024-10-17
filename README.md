
# CyberLens 🔍

## What is it?
CyberLens is a web-based tool designed to assist cybersecurity analysts in investigating and analyzing suspicious IP addresses, domains, and file hashes. It aggregates data from multiple sources into a single, easy-to-use interface, highlighting pre-set rules and points of interest. CyberLens provides analysts with a broad overview of relevant information, allowing them to use other specialized tools to focus on specific threat indicators.

![alt text](https://github.com/DrTurtlebot/CyberLens/blob/main/.github/workflows/docs/KHMBA15MQKW3_Hero.png)

## Why is it?
Cyberlens was designed to fill a hole in a Cyber Security SOCs assessment flow. The idea is that Cyberlens will auto highlight things of interest for a basic understanding of possible threats.

## Key Features
- 🔍 **Data Aggregation**: Collects information from multiple data sources (e.g., APIs) and consolidates it into one unified interface for quick, comprehensive analysis.
- 🚨 **Rule-based Highlighting**: Automatically flags suspicious activities and patterns using pre-set rules, helping analysts focus on what matters most.
- 📊 **Visual Data Representation**: Offers clear and dynamic graphs of the data, helping analysts visualize trends, patterns, and anomalies.
- 🧠 **AI Summary Reports**: Automatically generates summaries of findings using AI, giving analysts a high-level overview without the need to comb through raw data.
- ⚡ **User-friendly Interface**: An intuitive design makes it simple to interpret complex data, helping users make quick and informed decisions.
- 📂 **Image Export of Widgets**: Allows users to export graphs and widgets as images, making it easy to share and report findings.
- 🔗 **Integration Ready**: CyberLens comes with its own API, allowing it to be integrated with other tools seamlessly.
- 🚀 **Fast and Scalable**: Built for performance and scalability with FastAPI and Docker.

- ## 👨‍💻 Note from Me 
This project was created for a Security Operations Center (SOC) to improve its cybersecurity workflow while I was a student. I identified a gap in the analysts' process and developed CyberLens to help streamline their first responses. Today, CyberLens is an active part of the SOC's toolset.

Many of the tools and techniques I used in this project were things I learned along the way, and what started as a small idea quickly grew into something much larger. As a result, you might come across parts of the code and think, "What is going on here?" (though I hope you won’t!). That said, this project reflects my learning process, and while some aspects could probably be optimized, it's been a valuable experience for my growth as a developer. e.g. I didnt have enough time to finish my tests..

If you decide to run CyberLens, I hope you find it useful! Feel free to share any cool ideas you have or ways to improve it. 😊

-Alex

## 🛠️ System Overview
CyberLens consists of:
- A **frontend** built with Vue.js for data visualization and user interaction.
- A **backend** built with Python and FastAPI for gathering and processing data from external sources.
- A **MongoDB** server to store cached data.
- **Nginx** for reverse proxy routing.

## 🧪 Local Testing Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-repo/cyberlens.git
cd cyberlens
```

### 2. Environment Setup

#### Frontend Configuration
In `/frontend/.env`, set:
```env
VITE_BACKEND_ADDRESS=http://localhost:5000
```
This sets the backend address for local testing.

#### Backend Configuration
In `/backend/.env`, set up the following environment variables. These tokens can be gathered from the respective API providers (Please check their Terms of Use before using in a commercial setting):
```env
ENV_API_PROXYCHECK_KEY=
ENV_API_PROXYCHECK_URL=https://proxycheck.io/v2/

ENV_API_ABUSEIPDB_KEY=
ENV_API_ABUSEIPDB_URL=https://api.abuseipdb.com/api/v2/check

ENV_API_VIRUSTOTAL_KEY=
ENV_API_URLSCAN_KEY=
ENV_API_URLSCAN_URL=https://urlscan.io/api/v1/scan/

ENV_API_WHODAT_URL=https://who-dat.as93.net/
ENV_API_OPENAI_KEY=
ENV_CACHE_RETENTION_HOURS=5
ENV_MONGO_URI=localhost:27017
ENV_CORS_WHITELIST=http://localhost:5000
```

### 3. Running Local Services

#### Start MongoDB
To start a local instance of MongoDB, run:
```bash
docker compose up mongodb
```
This will expose port `27017` for MongoDB.

#### Start the Backend
```bash
cd backend
python dev_start.py
```

#### Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

The site will be available at `http://localhost:5000/`.

###  4. 🔌 Required Ports
Ensure the following ports are available:
- 4000 (Backend)
- 5000 (Frontend)
- 27017 (MongoDB)

## ⚙️ GitHub Actions Setup

### Variables and Secrets
In GitHub Actions, add the following variables and secrets. These tokens can be gathered by the individual API providers (Please check with API Terms of Use). Ensure that the secrets correspond to the correct tokens from the providers. If you dont want to use a service, e.g. dont have a 'VirusTotal' key, set the secret to equal an empty string, eg ENV_API_VIRUSTOTAL_KEY = "", and include the default variable for the URL.

#### 🔐 Secrets:
- `ENV_API_PROXYCHECK_KEY`
- `ENV_API_ABUSEIPDB_KEY`
- `ENV_API_VIRUSTOTAL_KEY`
- `ENV_API_URLSCAN_KEY`
- `ENV_API_OPENAI_KEY`
- `ENV_LOGFIRE_TOKEN` : Pydantic Logfire
- `ENV_MONGO_URI` : default(`mongodb:27017`), change it to something else for external MongoDB

#### Variables:
- `ENV_API_PROXYCHECK_URL`: `https://proxycheck.io/v2/`
- `ENV_API_ABUSEIPDB_URL`: `https://api.abuseipdb.com/api/v2/check`
- `ENV_API_URLSCAN_URL`: `https://urlscan.io/api/v1/scan/`
- `ENV_API_WHODAT_URL`: `https://who-dat.as93.net/`
- `ENV_CACHE_RETENTION_HOURS`: `5`
- `ENV_CORS_WHITELIST`: `http://localhost:5000` 
- `VITE_BACKEND_ADDRESS`: `http://localhost:5000`

## Security Note

### CORS Whitelist Configuration
Currently, the CORS whitelist in `main.py` accepts all traffic, which can pose a security risk. To restrict access, modify the `main.py` file and remove `['*']` from the CORS whitelist. Instead, use the Env Var

## 🚀☁️ Linode Deployment

### 1. 🖥️ Create a Linode Server
- Spin up a Linode with Ubuntu in your preferred region.
- Use a shared CPU plan (2GB is recommended, though 1GB might work).
- Set a secure root password (save it for later use). Optionally, set up SSH for added security/connection.

### 2. 👤 Configure Linode

#### Create a New User
Instead of using the root account, it's best practice to create a new user for security purposes. This ensures that GitHub Actions does not have root access to the system.
```bash
adduser coolman
sudo adduser coolman sudo
su coolman
```
You can replace `coolman` with any username of your choice. Ensure that the password you set is secure.

#### Install Docker and Docker-Compose
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo apt install docker-compose
sudo usermod -aG docker coolman
newgrp docker
```

### 3. ⚙️ GitHub Actions Runner Setup

To automate deployments, GitHub Actions is used. Go to **Settings > Actions > Runners** in your GitHub repository and create a new self-hosted runner:

- Select "New Self-Hosted Runner" and follow the instructions on GitHub.
- Once on your Linode server, switch to the new user (`coolman`) and run the commands given by GitHub, starting with:
```bash
$ mkdir actions-runner && cd actions-runner
```
Continue through the steps provided by GitHub to configure the runner.

```bash
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status
```
This installs the runner as a service that will start automatically on startup.

### 4. 🌐 NGINX Setup

Nginx is used as a reverse proxy to route traffic to the appropriate services.

#### Install Nginx
```bash
sudo apt install nginx
```

#### Configure Nginx
Edit the default configuration file:
```bash
sudo nano /etc/nginx/sites-available/default
```

> **Note**: Feel free to change any of these settings below to match your config, including setting a specific server name rather than using the default `_`.

Replace the contents with the following configuration:
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name _;

    location / {
       proxy_pass http://localhost:5000;
    }

    location /api {
        proxy_pass http://localhost:4000;
    }
}
```

Test the configuration:
```bash
sudo nginx -t
```

Restart Nginx:
```bash
sudo systemctl restart nginx
```

### 5. ✅ Final Steps
- Test the server at your Linode IP address. Test `/api` to ensure the backend is working.
- Make sure your Linode firewall is configured to allow ports 80 (HTTP), 443 (HTTPS), and any other ports needed for services.
- If needed, add the Linode IP to your DNS records (e.g., Cloudflare).
- You can set the IP to be an 'a' record on your domain provider, with cloudflare feel free to use flexible proxy for SSL

Your CyberLens instance should now be live!

## 🔒 Security Considerations
Ensure that all environment variables are securely set and that no sensitive data (such as API keys) is exposed publicly. Always use HTTPS in production to avoid potential security risks.

## ⏱️ API Rate Limiting and Quotas
Be aware that third-party services such as AbuseIPDB, VirusTotal, and ProxyCheck impose rate limits on API calls. Exceeding these limits may result in temporary suspension of access to their services.

The Default rate Limit for Cyberlens aswell is 10 requests per minute, this can be modified in the main.py file

### 💡 Strategies for Managing Rate Limits:
1. **Data Caching**: Cached data is stored in MongoDB to reduce unnecessary API calls. You can configure cache retention using the `ENV_CACHE_RETENTION_HOURS` environment variable.
2. **API Key Quota**: Ensure that the API keys are properly managed, and you are aware of any quota limitations imposed by the services. Some may require an upgraded plan for higher request limits.

## License

Copyright (c) 2024 Alex Dalton

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, and/or distribute copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
   
2. **Selling this software or its source code is not permitted.** You may use it for commercial purposes, but any distribution of the software must be free of charge, and the source code must remain free to download if published.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
