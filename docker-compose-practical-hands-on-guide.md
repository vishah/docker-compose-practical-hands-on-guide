# Docker and Docker Compose Practical Hands-On Guide

This guide is for learners who want to understand Docker by doing, not by memorizing commands.
You will start with a single container, then build your own image, then move into multi-service Docker Compose labs.
Each lab explains not only what to type, but why the step matters.

## What You Will Learn

By the end of the guide, you should be able to:

- Explain the difference between an image, a container, a volume, a network, and a Compose project.
- Build a custom image from a `Dockerfile`.
- Run containers with port mappings and environment variables.
- Use `docker compose` to manage a local development stack.
- Connect multiple services together with Compose networking.
- Persist state with named volumes.
- Read logs, inspect services, and clean up correctly.
- Understand a more production-like Compose setup with healthchecks, env files, and a reverse proxy.

## How To Use This Guide

- Work through the labs in order. Each lab builds on the previous one.
- Type commands yourself instead of copy-pasting everything at once.
- After each lab, pause and explain the result in your own words.
- Break things on purpose. Change a port, remove a volume, or stop a dependency and see what happens.

## Prerequisites

- Docker Desktop, or Docker Engine plus the Compose plugin.
- A terminal.
- Basic shell navigation such as `cd` and `ls`.
- Free local ports: `5000`, `5001`, `8080`, and `8081`.

Verify your setup:

```bash
docker --version
docker compose version
docker run --rm hello-world
```

What this proves:

- `docker --version` confirms the Docker CLI is installed.
- `docker compose version` confirms the modern Compose subcommand is available.
- `docker run --rm hello-world` confirms Docker can pull an image and start a container.

## Core Mental Model

Before the labs, keep these five ideas straight:

### 1. Image

An image is a packaged filesystem plus metadata and a startup command.
Think of it as a blueprint or template.

### 2. Container

A container is a running instance of an image.
If an image is a class, a container is an object.
Containers are disposable by design.

### 3. Volume

A volume stores data outside the container lifecycle.
Delete and recreate the container, and the volume can still keep the data.

### 4. Network

Containers can talk to each other over a Docker-managed network.
Compose creates a project network automatically, so services can usually reach each other by service name.

### 5. Compose

Compose is a way to declare a multi-container application in YAML.
Instead of remembering long `docker run` commands, you describe services once and run them together.

## Lab 1: Run Your First Real Container

Path: no starter files required.

### Goal

Run a web server container, inspect it, enter it, and remove it cleanly.

### Step 1: Start Nginx

```bash
docker run -d --name web1 -p 8081:80 nginx:alpine
```

Explanation:

- `docker run` creates and starts a container.
- `-d` runs it in detached mode.
- `--name web1` gives it a human-friendly name.
- `-p 8081:80` maps your machine's port `8081` to the container's port `80`.
- `nginx:alpine` is the image name and tag.

Open `http://localhost:8081`.

What happened:

- Docker pulled the image if it was not already local.
- A container started from that image.
- Nginx listened on port `80` inside the container.
- Docker published that port to `8081` on your machine.

### Step 2: See Running Containers

```bash
docker ps
```

Explanation:

- This shows active containers only.
- Notice the container name, image, status, and published ports.

### Step 3: Read Container Logs

```bash
docker logs web1
```

Explanation:

- Logs are often the fastest way to see whether an app started correctly.
- For long-running apps, this is usually your first debugging command.

### Step 4: Open a Shell in the Container

```bash
docker exec -it web1 sh
```

Inside the container, try:

```sh
ls
ps
cat /etc/os-release
exit
```

Explanation:

- `docker exec` runs a command inside an already-running container.
- `-it` gives you an interactive terminal session.
- This helps you inspect files, environment variables, and running processes.

### Step 5: Stop and Remove the Container

```bash
docker stop web1
docker rm web1
```

Explanation:

- `stop` sends a signal to end the main process.
- `rm` removes the stopped container.
- Removing a container does not remove the image.

### What You Learned

- Images and containers are different things.
- Port mapping is explicit.
- Container logs and `exec` are core debugging tools.
- Containers are disposable.

## Lab 2: Build Your Own Image

Path: `outputs/labs/lab-02-build-image`

### Goal

Build a small Flask web app into a custom image and run it.

### Files In This Lab

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `.dockerignore`

### Step 1: Move Into The Lab Directory

```bash
cd outputs/labs/lab-02-build-image
```

Explanation:

- Docker builds from a context directory.
- Everything in the current build context can be sent to the Docker daemon unless excluded by `.dockerignore`.

### Step 2: Build The Image

```bash
docker build -t compose-hands-flask:v1 .
```

Explanation:

- `-t` adds a name and tag to the built image.
- `.` means the current directory is the build context.
- Docker executes the `Dockerfile` step by step and creates image layers.

### Step 3: Run The Image

```bash
docker run --rm -p 5000:5000 -e MESSAGE="Built from my Dockerfile" compose-hands-flask:v1
```

Open `http://localhost:5000`.

Explanation:

- `--rm` removes the container automatically when it exits.
- `-e MESSAGE=...` injects an environment variable at runtime.
- The image is now your own artifact, not just a public image you pulled.

### Step 4: Inspect The Result

```bash
docker image ls compose-hands-flask
docker ps
```

Explanation:

- `docker image ls` shows your built image.
- `docker ps` confirms the container is running from that image.

### Step 5: Change The App And Rebuild

Edit `app.py`, change the default message, then rebuild:

```bash
docker build -t compose-hands-flask:v2 .
```

Explanation:

- Image builds are immutable snapshots.
- Changing source code does nothing to a running container until you rebuild or remount the code.

### Why `.dockerignore` Matters

The `.dockerignore` file keeps junk out of the build context.
That makes builds faster, smaller, and less error-prone.

## Lab 3: Use Compose For Local Development

Path: `outputs/labs/lab-03-compose-dev`

### Goal

Replace a long `docker run` command with a Compose file and use a bind mount for fast iteration.

### Files In This Lab

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `compose.yaml`
- `.dockerignore`

### Step 1: Move Into The Lab Directory

```bash
cd ../lab-03-compose-dev
```

If you are not currently in `lab-02-build-image`, use the full path:

```bash
cd outputs/labs/lab-03-compose-dev
```

### Step 2: Start The Stack

```bash
docker compose up --build
```

Explanation:

- `docker compose up` creates the project network, builds images if needed, and starts services.
- `--build` forces Compose to rebuild before starting.
- In this lab there is only one service, but the Compose workflow is the same for larger stacks.

Open `http://localhost:5000`.

### Step 3: Inspect Compose State

In another terminal:

```bash
docker compose ps
docker compose logs -f web
```

Explanation:

- `ps` shows the services in the current project.
- `logs -f` tails logs for one service.
- Compose scopes resources by project, which makes multi-container work easier to manage.

### Step 4: Edit The App Without Rebuilding

Change the message in `app.py` or in `compose.yaml`, then refresh the browser.

Explanation:

- This lab uses a bind mount, so the container sees your local files directly.
- That is good for development because you can iterate quickly.
- It is not how you should ship production images.

### Step 5: Stop The Stack

```bash
docker compose down
```

Explanation:

- `down` removes containers and the project network.
- It does not remove named volumes unless you add `-v`.

### What Compose Added Here

- Declarative configuration.
- Easier repeatability.
- Cleaner service lifecycle management.
- A stepping stone to multi-service applications.

## Lab 4: Build A Multi-Service Application With Compose

Path: `outputs/labs/lab-04-compose-multi-service`

### Goal

Run a Flask app and Redis together, connected by Compose networking, with a persistent Redis volume.

### Files In This Lab

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `compose.yaml`
- `.dockerignore`

### Step 1: Move Into The Lab Directory

```bash
cd ../lab-04-compose-multi-service
```

Or:

```bash
cd outputs/labs/lab-04-compose-multi-service
```

### Step 2: Start The Project

```bash
docker compose up --build
```

Open `http://localhost:5001`.
Refresh the page several times.

What you should see:

- A counter increasing on each request.
- The app reporting that it is talking to Redis.

Explanation:

- The `web` service connects to `redis` by service name, not by IP address.
- Compose creates a default network and registers service names on it.
- This is one of the biggest practical benefits of Compose.

### Step 3: Inspect The Redis Data

In another terminal:

```bash
docker compose exec redis redis-cli get hits
```

Explanation:

- `docker compose exec` is the Compose-aware version of `docker exec`.
- You are reading application state directly from the dependency container.

### Step 4: Test Persistence

Stop the stack:

```bash
docker compose down
```

Start it again:

```bash
docker compose up
```

Refresh the page.

Explanation:

- The hit counter should continue because Redis data is stored in a named volume.
- Containers are transient, but the volume survives.

Now reset everything completely:

```bash
docker compose down -v
```

Explanation:

- `-v` removes named volumes created by the project.
- This is the difference between deleting containers and deleting state.

### Step 5: View The Fully Rendered Compose Config

```bash
docker compose config
```

Explanation:

- This shows the resolved configuration after interpolation and defaults.
- It is useful when debugging larger Compose files.

### What You Learned

- Service discovery by service name.
- Multi-service orchestration.
- Persistent state with named volumes.
- The importance of cleanup choices.

## Lab 5: A More Production-Like Compose Stack

Path: `outputs/labs/lab-05-compose-productionish`

### Goal

Run a small stack with an app, Redis, and Nginx, using healthchecks, an env file, restart policies, and a debug profile.

### Files In This Lab

- `app.py`
- `requirements.txt`
- `Dockerfile`
- `compose.yaml`
- `.env.example`
- `nginx/default.conf`
- `.dockerignore`

### Step 1: Move Into The Lab Directory

```bash
cd ../lab-05-compose-productionish
```

Or:

```bash
cd outputs/labs/lab-05-compose-productionish
```

### Step 2: Review The Runtime Env File

This lab includes a ready-to-run `.env` plus a matching `.env.example` template.
If you want to reset the lab back to the default values, run:

```bash
cp .env.example .env
```

Explanation:

- `env_file` is a clean way to supply runtime configuration.
- It keeps environment-specific values out of the main Compose file.
- The example file is version-safe to commit, while the real `.env` is usually local.

### Step 3: Start The Stack In The Background

```bash
docker compose up --build -d
```

Open `http://localhost:8080`.

Explanation:

- `proxy` publishes port `8080`.
- Nginx forwards requests to the internal `web` service.
- `web` depends on a healthy Redis instance.

### Step 4: Inspect Health And Status

```bash
docker compose ps
docker compose logs -f proxy web redis
```

Explanation:

- `ps` should show the state of each service.
- Healthchecks make startup order and readiness more explicit.
- Logs across multiple services help you trace request flow.

### Step 5: Use The Optional Debug Profile

Start the debug service:

```bash
docker compose --profile debug up -d inspector
```

Run a network check from inside the Compose network:

```bash
docker compose exec inspector wget -qO- http://web:5000/health
```

Explanation:

- Profiles let you keep optional services out of the default startup path.
- This is useful for temporary tooling such as shells, seeders, or troubleshooting helpers.

### Step 6: Tear Down The Stack

```bash
docker compose down
```

If you want to remove persistent Redis data too:

```bash
docker compose down -v
```

### What This Lab Adds Beyond Basic Compose

- `env_file` for configuration.
- Healthchecks for dependency readiness.
- A reverse proxy service.
- Restart policies.
- An optional profile.
- A non-root application container.

## Troubleshooting Checklist

### Port Already In Use

Symptom:

- `Bind for 0.0.0.0:5000 failed`

Fix:

- Stop the process already using that port, or change the left side of the port mapping.

Example:

```yaml
ports:
  - "5050:5000"
```

### Container Exits Immediately

Symptom:

- The container starts and stops right away.

Fix:

- Read the logs.
- Confirm the startup command is correct.
- Check environment variables and file paths.

Useful commands:

```bash
docker logs <container-name>
docker compose logs <service-name>
```

### Code Changes Do Not Appear

Symptom:

- You edit files locally but the app output does not change.

Fix:

- For image-based labs, rebuild the image.
- For bind-mounted dev labs, confirm the volume is configured correctly.

### Data Keeps Coming Back

Symptom:

- You thought you deleted everything, but old data still exists.

Fix:

- Remember that `docker compose down` keeps named volumes.
- Use `docker compose down -v` when you want a full reset.

### Service Starts Before Dependency Is Ready

Symptom:

- App container starts, but cannot connect to Redis or another dependency yet.

Fix:

- Add a healthcheck to the dependency.
- Use `depends_on` with `condition: service_healthy` when your Compose implementation supports it.

## Good Habits To Keep

- Prefer `docker compose` over old `docker-compose`.
- Keep Dockerfiles small and deterministic.
- Use `.dockerignore`.
- Separate development-only behavior from production images.
- Tag images meaningfully.
- Use named volumes for real state.
- Use `docker compose config` when YAML behavior is confusing.
- Clean up old containers and images regularly.

## Suggested Next Experiments

After finishing the labs, try these:

1. Add PostgreSQL as another service and connect the Flask app to it.
2. Add an `.env` variable that changes the Flask app behavior by environment.
3. Add a second app replica and put Nginx in front of it.
4. Split the Compose file into a base file plus an override for development.
5. Add a CI job that builds the Docker image automatically.

## Quick Command Cheat Sheet

```bash
docker run -d --name demo -p 8080:80 nginx:alpine
docker ps
docker logs demo
docker exec -it demo sh
docker stop demo
docker rm demo

docker build -t myapp:v1 .
docker run --rm -p 5000:5000 myapp:v1

docker compose up --build
docker compose up -d
docker compose ps
docker compose logs -f
docker compose exec web sh
docker compose config
docker compose down
docker compose down -v
```

If you can explain why each command exists and when to use it, you have a solid beginner-to-intermediate Docker foundation.
