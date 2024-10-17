
# CyberLens

## What is it?
CyberLens is a web-based tool designed to assist cybersecurity analysts in investigating and analyzing suspicious IP addresses, domains, and file hashes. It aggregates data from multiple sources into a single, easy-to-use interface, highlighting pre-set rules and points of interest. CyberLens provides analysts with a broad overview of relevant information, allowing them to use other specialized tools to focus on specific threat indicators.

## Why is it?
Cyberlens was designed to fill a hole in a Cyber Security SOCs assessment flow. The idea is that Cyberlens will auto highlight things of interest for a basic understanding of possible threats.

## Key Features
- 🔍 **Data Aggregation**: Collects information from multiple data sources (e.g., APIs) and consolidates it into one unified interface for quick, comprehensive analysis.
- 🚨 **Rule-based Highlighting**: Automatically flags suspicious activities and patterns using pre-set rules, helping analysts focus on what matters most.
- 📊 **Visual Data Representation**: Offers clear and dynamic graphs of the data, helping analysts visualize trends, patterns, and anomalies.
- 🧠 **AI Summary Reports**: Automatically generates summaries of findings using AI, giving analysts a high-level overview without the need to comb through raw data.
- ⚡ **User-friendly Interface**: An intuitive design makes it simple to interpret complex data, helping users make quick and informed decisions.
- 📂 **Image Export of Widgets**: Allows users to export graphs and widgets as images, making it easy to share and report findings.
- 🔗 **Integration Ready**: CyberLens comes with its own API, allowing it to be integrated with other tools seamlessly. This enables cybersecurity analysts to call the CyberLens API for deeper threat analysis or to automate workflows.
- 🛠️ **Customizable Alerts**: Set up custom alerts for emerging threats or user-defined triggers, ensuring timely responses to critical incidents.
- 🚀 **Fast and Scalable**: Built for performance and scalability with a robust architecture using FastAPI and Docker.

## System Overview
The system consists of:
- A **frontend** built with Vue.js for data visualization and user interaction.
- A **backend** built with Python and FastAPI for gathering and processing data from external sources.
- A connection to a **MongoDB** to store the cached data.

### Notes
> **Important**: This setup will configure a production-ready deployment using GitHub Actions. Ensure that all required GitHub Secrets and Variables are correctly set before proceeding with deployment.

## Requirements
- GitHub account
- Correctly configured **GitHub Secrets** and **GitHub Variables**
- Cloudflare Pages access.
- A Backend Server with external world access. 
- MongoDB Server
- Logfire Logging 

## Module Requirements
Important, some of these modules may have terms of service for commercial purposes imposing minimum plan requirements.
If you do not want to use a particular module just leave the URL and key as an empty string `""` in the GitHub environments, and CyberLens will ignore them.

- AbuseIPDB   
- ProxyCheck  
- UrlScan	
- VirusTotal 	
- WhoDat  	

## Environment Variables and Secrets requirements for backend and frontend

### Secrets:
- `ENV_API_ABUSEIPDB_KEY`
- `ENV_API_OPENAI_KEY`
- `ENV_API_PROXYCHECK_KEY`
- `ENV_API_URLSCAN_KEY`
- `ENV_API_VIRUSTOTAL_KEY`
- `ENV_MONGO_URI`
- `LOGFIRE_TOKEN`

### Variables:
- `ENV_API_ABUSEIPDB_URL` : default `https://api.abuseipdb.com/api/v2/check`
- `ENV_API_PROXYCHECK_URL` : default `https://proxycheck.io/v2/`
- `ENV_API_URLSCAN_URL` : default `https://urlscan.io/api/v1/scan/`
- `ENV_API_WHODAT_URL` : default `https://who-dat.as93.net/`
- `ENV_CACHE_RETENTION_HOURS` : default `5`
- `ENV_CORS_WHITELIST` : Comma-separated list of allowed origins for CORS. eg `'https://site1.local, https://site2.local'`
- `PROD_CHECK` : default `True`
- `WIL_BACKEND_ADDRESS` : default `https://myepicwilprojects.online` (Address of the backend server)

### Debug Variable:
- `CUSTOM_DOCKER_ARGS` : This is a strange one, if you want custom args on the docker run, you can add them here
**Important**: In production, this value should be set to atleast '-d' which will stop printing debug messages to the CLI, it can be removed for debugging. If its still there when not needed, you will eat up Github Minutes and it will fail to deploy as the action will constantly be waiting to print from docker. This is done so you can read the github docker run output without having to recommit, but rather change the var. 

## Environment Variables for Default setup (Digital Oceans droplet and Cloudflare pages)

This is not required depending on how you deploy your services.

### Secret: 
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`
- `DOP_API_TOKEN`
- `DOP_IP`
- `DOP_SSHKEY`
- `DOP_USERNAME`

## Deployment

### 1. Clone the repository
To begin, you will need to clone the repository to your local machine:

```bash
git clone https://github.com/your-repo/cyberlens.git
cd cyberlens
```

### 2. Configure GitHub Actions Variables
Next, set up the required GitHub Secrets and Variables to ensure the automated CI/CD pipeline works correctly. These settings are essential for both the frontend deployment to Cloudflare Pages and the backend deployment to DigitalOcean.

#### Frontend Deployment (Cloudflare Pages)
The frontend is automatically built and deployed using GitHub Actions whenever code is pushed to the `main` branch. Follow these steps:

1. Clone the repository as instructed above.
2. Configure the necessary GitHub Secrets and Variables for Cloudflare.
3. Push your changes or trigger a manual build via the GitHub Actions tab in your repository.

#### Backend Deployment (DigitalOcean Droplet)
The backend is deployed to a DigitalOcean Droplet via SSH using GitHub Actions. This involves connecting to the droplet, deploying code, and configuring the environment:

1. Ensure that the DigitalOcean Droplet is set up and that you have the necessary SSH access.
2. Push changes to the repository or trigger a deployment manually via GitHub Actions.
3. The backend will be built and configured automatically using the GitHub Actions pipeline.

## HTTPS Requirements

For security reasons, it is recommended that all communications between the frontend and backend are made over HTTPS. If your backend server is not configured for HTTPS, you may encounter browser security warnings or blocked requests due to mixed content issues.

### Using Cloudflare Proxy to Convert HTTPS to HTTP

If your backend only supports HTTP, you can use Cloudflare to proxy and convert HTTPS requests to HTTP, ensuring secure communication between the frontend and backend.

1. **Enable Cloudflare Proxying**: 
   Set up your domain with Cloudflare and enable proxying to your backend server.
   
2. **Force HTTPS**: 
   In Cloudflare’s SSL/TLS settings, enable "Full" or "Full (Strict)" mode to force secure HTTPS connections.
   
3. **Backend HTTP Configuration**: 
   Ensure the backend server is set to receive HTTP traffic without forcing HTTPS when proxied via Cloudflare.

4. **CORS Configuration**: 
   Make sure the `ENV_CORS_WHITELIST` environment variable includes the HTTPS domain of your frontend to allow cross-origin communication without issues.

> **Note**: Failing to implement HTTPS properly can lead to security conflict warnings or blocked API requests.

Below is a Diagram showing which services require HTTPS SSL and which do not.

![alt text](https://imgur.com/zG8njkI.png)

## API Rate Limiting and Quotas
Be aware that third-party services such as AbuseIPDB, VirusTotal, and ProxyCheck impose rate limits on API calls. Exceeding these limits may result in temporary suspension of access to their services.

The Default rate Limit for Cyberlens aswell is 10 requests per minute, this can be modified in the main.py file

### Strategies for Managing Rate Limits:
1. **Data Caching**: Cached data is stored in MongoDB to reduce unnecessary API calls. You can configure cache retention using the `ENV_CACHE_RETENTION_HOURS` environment variable.
2. **API Key Quota**: Ensure that the API keys are properly managed, and you are aware of any quota limitations imposed by the services. Some may require an upgraded plan for higher request limits.

## License

Copyright (c) 2024 Alex Dalton

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, and/or distribute copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
   
2. **Selling this software or its source code is not permitted.** You may use it for commercial purposes, but any distribution of the software must be free of charge, and the source code must remain free to download.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
