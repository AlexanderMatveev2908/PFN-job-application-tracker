# PFN-job-application-tracker 📈

## 📌 About This Project

The idea for this app was born while I was applying to jobs on LinkedIn and jotting down basic information in a simple notepad.  
So I decided to build a proper application to track them:

- First to consolidate the **Python tools** I've recently learned.

- Second, to create something useful that anyone can clone and use to manage their own applications.

---

## 🧱 Tech Stack

### 🖥️ **Client**

- **Next.js** (App Router) — Framework for React with built-in SSR, ISR, routing, and SEO optimization
- **React** + **TypeScript** — Component-based UI with static typing for maintainable, scalable front-ends
- **React Hook Form** + **Zod** — Type-safe form handling with schema-based validation
- **Redux Toolkit** + **RTK Query** — Centralized state and API caching
- **Axios** — Preconfigured HTTP client integrated with RTK Query
- **Framer Motion** — Smooth, customizable UI animations
- **Tailwind CSS** + **Sass** — Utility-first styling with support for custom, complex styles

---

### 💾 **Server**

- **Python** `>=3.12` — Primary backend language with strong async support
- **FastAPI** — High-performance async API framework
- **SQLAlchemy** + **Alembic** — ORM and schema migrations for relational DBs
- **Pydantic** — Data validation and parsing
- **Mypy** — Static type checking for Python code quality
- **Poetry** — Dependency and environment management
- **Gunicorn** + **Uvicorn** — ASGI stack for running FastAPI in production
- **Amazon SES** — Transactional & notification email service
- **Aiosmtplib** — Async SMTP client
- **Amazon S3** — Cloud object storage for files and assets
- **Redis** — In-memory key-value store for caching, rate limiting, and temporary data
- **Argon2** — Modern memory-hard password hashing algorithm, used to securely store user passwords and protect against brute-force or GPU attacks
- **JWT** — Used as short-lived access tokens for authenticating user requests.
- **JWE—** Used as refresh tokens, securely storing session renewal data.
- **CBC-HMAC tokens with HKDF-derived keys** — Special short-lived tokens, mainly for sensitive actions like account verification, password resets, or email confirmation.
- **APScheduler** — Schedules recurring tasks

---

### 🧪 **Testing**

- **Playwright** — End-to-end testing for UI flows
- **Vitest** — Unit testing for the client
- **Pytest** — Unit and integration testing for the server
- **Postman** — API testing

---

### 🛠️ **DevOps & Deployment**

- **Turborepo** — Monorepo project structure for managing client and server together, with coordinated scripts and parallel builds
- **Docker** — Ensures consistent environments for development and production across both client and server
- **Docker Hub** — Publishing and managing images
- **GitHub Actions** — Automated pipelines for testing, building, and deploying both apps
- **Fly.io** — Hosting platform (client and server deployed as separate services)
- **Supabase** — PostgreSQL hosting
- **Upstash** — Hosting platform for Redis
- **Brevo (SMTP)** — Outbound transactional email deliver
- **Zoho Mail** — Inbound email hosting for custom domain addresses
- **Namecheap** — Domain provider, configured with DNS records (SPF, DKIM, DMARC) to support both Brevo + Zoho
- **Zsh** — Custom shell scripts for scaffolding and developer productivity

## 📦 Setup

After cloning the repository, start by installing dependencies:

```bash
yarn install && yarn install_pkg
```

This will initialize the project and install all required packages for both the client and server.

---

### 🔒 Environment Variables

All required environment variables are listed and validated inside:

```bash
apps/server/src/conf/env.py
```

This file uses **Pydantic** to:

- Define expected variables
- Enforce correct types
- Raise validation errors if anything is missing

This approach ensures that all variables needed by both client and server are defined in one central place — making your app easier to configure and maintain.

There’s no strict separation between client and server variables, but variables used by the client are easy to identify because **Next.js** requires them to start with **NEXT_PUBLIC**.

You can choose between two options:

1.  Full file reuse:
    Define all environment variables once (**server-side**), and copy the same .env file into the client folder.
    This is the easiest and safest approach.

2.  Split setup:
    Create a minimal .env file in the client folder, containing only the **NEXT_PUBLIC** variables.
    This reduces redundancy but requires you to manage two separate files.

---

### 🚀 Start App

To start a development session, run:

```bash
yarn dev
```

This uses **Turborepo** to run both the **Python server** and the **Next.js client** in parallel:

- 🐍 **Python** runs via **Uvicorn**, with **auto-reload** on **src** changes, at http://localhost:3000
- 🖥️ **Next.js** runs at http://localhost:3001

---

TO build the app run:

```bash
yarn build
```

This uses **Turborepo** to build both the client and server in parallel:

- 🐍 Python: Generates a .tar.gz and .whl (wheel) distribution packages.
  The wheel file is stored inside a custom **app_wheel** folder and used for **local** build.
- 🖥️ Next.js will follow his normal flow to generate **SSR** or **CSR** pages based on top page declaration and inner fetch logic.

---

Once the build is complete, you can run:

```bash
yarn start
```

This uses **Turborepo** to start both the **Python server** and the **Next.js client** in parallel:

- 🐍 **Python** runs via **Gunicorn**, using **8 workers**, available at http://localhost:3000

- 🖥️ **Next.js** is served at http://localhost:3001

---

### 🐋 Docker Setup

The following Docker helper scripts are designed to support **dynamic file locations**, making it easy to delete or adjust paths as needed depending on your project structure.

---

#### 🖥️ Build Client

To build the **client** Docker image, use:

```bash
dbc() {
  local dockerfile="Dockerfile.client"
  local context="."

  if [[ ! -f "$dockerfile" ]]; then
    dockerfile="apps/client/Dockerfile"
    context="apps/client"
  fi

  docker build \
    --no-cache \
    -f "$dockerfile" \
    -t app-client \
    --build-arg NEXT_PUBLIC_ENV=development \
    --build-arg NEXT_PUBLIC_BACK_URL_DEV=http://localhost:3000/api/v1 \
    --build-arg NEXT_PUBLIC_FRONT_URL_DEV=http://localhost:3001 \
    "$context"
}

```

---

#### 💾 Build Server

To build the **server** Docker image, use:

```bash
dbs() {
  local dockerfile="Dockerfile.server"
  local context="."

  if [[ ! -f "$dockerfile" ]]; then
    dockerfile="apps/server/Dockerfile"
    context="apps/server"
  fi

  docker build \
    --no-cache \
    -f "$dockerfile" \
    -t app-server \
    "$context"
}

```

---

#### 🐳 Start Containers

To start a container for either the client or the server, use the following function:

```bash
dsi() {
  local port="${1:-1}"
  local name
  local env_p

  if [[ "$port" == "1" ]]; then
    name="client"
    env_p="apps/client/.env"
  elif [[ "$port" == "0" ]]; then
    name="server"
    env_p="apps/server/.env"
  else
    echo "❌ Unknown port '$port'. Use 1 (client) or 0 (server)"
    return 1
  fi

  local cname="app-${name}"

  docker rm -f "$cname" &>/dev/null || true

  docker run \
    --rm \
    --env-file "$env_p" \
    --name "$cname" \
    -p 300${port}:300${port} \
    "$cname"
}
```

---

To run both client and server containers in **parallel**:

```bash
dsi 0 & dsi 1
```

---

#### 🔗 Result

- 🖥️ **Next.js** is built into a Docker image and served from a container listening on http://localhost:3001
- 🐍 **Python** is packaged with Poetry, installs the .whl build, and runs from a container listening on http://localhost:3000/api/v1

---

### 🛡️ Reverse Proxy (optional)

As part of my local development setup, I prefer to start an `NGINX` server so the environment closely mirrors the production setup.

This allows me to:

- Test CORS issues directly in development
- Simulate deployment flow more realistically

---

💡 **Note:**

- You’ll need to configure **Node.js** to trust self-signed certs.

Add the following line to your `.bashrc` or `.zshrc`:

```bash
export NODE_OPTIONS="--use-system-ca"
```

---

For Self-signed certs I used `mkcert` and `nss`(optional for `Chrome` — required for `Firefox`).
Setup includes:

```bash
sudo pacman -S mkcert nss && \
mkcert -install && \
mkcert localhost
```

---

#### 📜 NGINX Config Script

💡 **Note:**

- Wherever you see `ninja` in paths (e.g. `/home/ninja/`), replace it with **your Linux username**, which you chose during OS installation.
  You can check your current username with:

```bash
echo $USER
```

---

```bash
# ❕ http is the default NGINX user on Manjaro (Arch-based distros).

user http;
worker_processes auto;

events {
    worker_connections 1024;
}

# ❕ HTTP block
http {
    # 📷 load MIME types from file to recognize extensions
    include mime.types;

     # ❓ fallback type if unknown: raw binary
    default_type application/octet-stream;

    # 💾 let the kernel handle file transfers for performance
    sendfile on;

    # ⌛ keep connections open for 60s before timing out
    keepalive_timeout 60;

    # 🥸 hide the NGINX version (like Helmet does for Node apps)
    server_tokens off;

    # 🗃️ allocate more memory for MIME type hash table
    types_hash_max_size 2048;
    types_hash_bucket_size 128;

    # 🔀 HTTP → HTTPS redirect
    server {
        listen 80;
        server_name localhost;

    # ❕ 301 code is a permanent redirection
        location / {
            return 301 https://$host$request_uri;
        }
    }

    # 🔐 HTTPS server block
    server {
        listen 443 ssl;
        server_name localhost;

        # 🗄️ increase body size limit (useful for file uploads)
        client_max_body_size 200M;

        # ⛔ restrict to modern TLS versions only
        ssl_protocols TLSv1.2 TLSv1.3;
        # ⛔ exclude ciphers that allow anonymous key exchange and weak hashing algorithms
        ssl_ciphers HIGH:!aNULL:!MD5;

        # ℹ️ basic logging
        access_log /var/log/nginx/access.log;
        error_log  /var/log/nginx/error.log warn;

        # 🔐 SSL cert paths (use absolute paths)
        ssl_certificate     /home/ninja/certs/nginx-dev/localhost.pem;
        ssl_certificate_key /home/ninja/certs/nginx-dev/localhost-key.pem;

      # 🐍 proxy to Python FastAPI or 🟩 Node.js Fastify server
        location /api/v1/ {
            proxy_pass http://localhost:3000/api/v1/;

            # 📱 useful if you later will need web-socket
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # 🖥️ proxy to Next.js or Vite app
        location / {
            proxy_pass http://localhost:3001/;

            # 📱 useful if you later will need web-socket
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

---

### ⚗️ Testing & Type Checking

#### ✒️ Type Checking & Formatting

- **Client**: Formatting with **ESLint** • Type checking with **TypeScript**
- **Server**: Formatting with **Ruff** • Type checking with **Mypy**

Run:

```bash
yarn check
```

- 💡 **Note**: **Ruff** is configured to allow ambiguous variables (**E741**).
  To disallow them, remove E741 from the ignore array in **tool.ruff.lint** in **pyproject.toml**

---

#### 🧪 Tests

##### 📜 Environment Variables

If you use **NGINX reverse proxies** and your dev URLs use **HTTPS**, both client and server need **test-specific URLs** for local and **CI/CD pipelines** testing.

The variables that set **test mode** are:

- **PY_ENV** for server
- **NEXT_PUBLIC_ENV** for client

So them are the same that also set **development** or **production** environment

---

##### 🔬 Test Flow

Running tests directly on a Next.js app can be slow and flaky due to rebuild times.

Instead:

1. **Build** the client

   ```bash
   yarn build
   ```

2. **Start** both client & server

   ```bash
   yarn start
   ```

3. **Run tests** on both client & server in parallel with maximum workers available on current machine

   ```bash
   yarn tests
   ```

## ✏️ Final Notes

I hope you find the project interesting — if not, the app doesn’t come with a refund policy 💰

Thanks for checking out the repo ✌🏼
