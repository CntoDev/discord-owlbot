# CNTO Owlbot

## What is the Owlbot

Owlbot is CNTO's omnipresent assistant. It is currently implemented as a TeamSpeak user for populating our `stats` pages, and on Discord for automated member pings before our operations begin. R&D has plans to expand the Discord presence to enable staff members to carry out their tasks directly from our Discord, but this is a WIP.

## Installation guide

Owlbot is available as [a Docker image](https://hub.docker.com/repository/docker/cntoarma/owlbot/general), published on CNTO's DockerHub registry.

### 1. Create a Discord application from the Discord Developer Portal

You can follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) to create a bot application. CNTO has two versions of the Owlbot managed by R&D: OWL and OWL Dev. The key takeaway from this step is to obtain the bot's secret, used to authenticate the bot against Discord's API.

### 2. Gather the required parameters

Within CNTO, the Owlbot is deployed on the `Tools Server`. It requires a few parameters as described in the `.env.template` file, namely:

```language=config
OWLBOT_SECRET=<OWLBOT_SECRET>               # The bot's secret obtained on the Discord Developer Portal
OP_START_CHANNEL_ID=<OP_START_CHANNEL_ID>   # The ID of the channel where operations reminders will be posted
```

These parameters can be passed to Owlbot in two different ways:

1. As system environment variables, for example `export OWLBOT_SECRET=1234`
2. As `.env` file in the same directory as the `.env.template`

Owlbot will try to load from a `.env` file, falling back to system variables. If both are present, system variables are used.

**Note** if you use the Owlbot Docker image from our public registry, the `.env` file is not yet created by the build process so you need to rely on environment variables. The `.env` file mechanism is supported for local development environments. We do not plan on adding `.env` file support for staging / production environments.

### 3. Run the Docker image

Launch a container based on the Owlbot Docker image, for example:

```bash
docker run -d -e OWLBOT_SECRET=<YOUR_SECRET_HERE> -e OP_START_CHANNEL_ID=<YOUR_CHANNEL_ID_HERE> cntoarma/owlbot:[stable|dev]
```

If you still want to use a `.env` you can avoid passing environment variables to the run command, for example:

```bash
docker run -d --env-file .env cntoarma/owlbot:[stable|dev]
```

**Note** using `docker-compose` is preferred in production environments as it can also handle container restarts, ensuring the Owlbot is operational all the time. 

#### Update the crontab file

By default, the Owlbot will send join reminders 10 minutes before our events start (19:35 CET / CEST). This is configured in the `crontab.txt` file that gets installed inside the Owlbot container upon build. If you need to change the 