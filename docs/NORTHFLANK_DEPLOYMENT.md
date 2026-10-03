# Northflank Deployment Guide

Deploying `gemini-web2api` on Northflank is straightforward because the repository provides a `Dockerfile`. Northflank allows you to automatically build and deploy this Dockerfile directly from your connected Git repository.

## Prerequisites
1. A [Northflank account](https://northflank.com/).
2. Your fork or clone of the `gemini-web2api` repository pushed to GitHub, GitLab, or Bitbucket.

## Step 1: Create a New Project
1. Log in to the Northflank dashboard.
2. Click **Create new project**.
3. Give your project a name (e.g., `gemini-proxy`) and select your preferred region.

## Step 2: Create a New Service
1. Inside your project, click **Create new service**.
2. Select **Combined service** (this handles both building and deploying).
3. Under **Repository**, select the provider where your `gemini-web2api` code lives (GitHub, GitLab, Bitbucket) and choose your repository and branch.

## Step 3: Configure Build Settings
1. **Build Type**: Select **Dockerfile**.
2. **Dockerfile Location**: Leave as `/Dockerfile` (or adjust if you moved it).
3. **Build Engine**: Northflank defaults to **BuildKit**. Leave this enabled for faster, cached builds.

## Step 4: Configure Deployment & Networking
1. **Ports**: Northflank should automatically detect port `8081` from the `EXPOSE` instruction in the `Dockerfile`.
   - Name it (e.g., `web`).
   - Protocol should be `HTTP`.
   - Check **Publicly Accessible** to route external traffic to your service.
2. **Resources**: Select the compute plan (the free tier or the smallest paid tier is usually sufficient, as the proxy is I/O bound, not CPU bound).

## Step 5: Environment Variables & Secrets
To configure the proxy, you should inject environment variables.
1. Scroll down to **Environment Variables** or go to your Project's **Secret Groups** to manage them globally.
2. Add the following variables as needed:
   - `GEMINI_BL`: Usually required to match Google's latest build label.
   - `API_KEYS`: A JSON string array, e.g., `["sk-my-secret-key"]`. Set this to prevent unauthorized public access!
   - `COOKIE_FILE`: Set to `/app/cookie.txt` if you plan to provide cookies.

### Providing Cookies (Optional)
If you need to use `gemini-3.1-pro`, you must provide your Google session cookies. Since you shouldn't commit `cookie.txt` to Git:
1. In Northflank, go to your service's **Volumes**.
2. Add an Ephemeral or Persistent Volume mounted at `/app`.
3. You can either use a startup command to write the cookie to the file, or pass the raw cookies directly as environment variables if using the Cloudflare Worker approach, but for Docker, writing it to a volume is standard. Alternatively, you can modify the Dockerfile to echo a secret into `cookie.txt` during runtime.

## Step 6: Deploy
1. Click **Create Service**.
2. Northflank will clone your repo, build the Docker image, and deploy the container.
3. Watch the build logs. Once complete, your service will display a public `.northflank.app` URL.

## Step 7: Access the API
Use the provided Northflank URL as your Base URL in your clients.
```bash
curl https://gemini-web2api-xxxx.northflank.app/v1/models \
  -H "Authorization: Bearer sk-my-secret-key"
```

## Maintenance & Observability
- **Logs**: Real-time server logs are available in the **Logs** tab of your service. You can monitor for `502 Bad Gateway` or `405 Method Not Allowed` errors here.
- **Auto-Deploys**: If configured, Northflank will automatically rebuild and deploy your service every time you push to your branch.
