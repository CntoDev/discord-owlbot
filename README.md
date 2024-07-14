# CNTO Owlbot

## What is the Owlbot

Owlbot is CNTO's omnipresent assistant. It is currently implemented as a TeamSpeak user for populating our `stats` pages, and on Discord for automated member pings before our operations begin. R&D has plans to expand the Discord presence to enable staff members to carry out their tasks directly from our Discord, but this is a WIP.

## Installation guide

Owlbot is available as [a Docker image](https://hub.docker.com/repository/docker/cntoarma/owlbot/general), published on CNTO's DockerHub registry. Two versions are currently maintained: `dev` for development environments and `latest` for production environments.

### 1. Create a Discord application from the Discord Developer Portal

You can follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) to create a bot application. CNTO has two versions of the Owlbot managed by R&D: OWL and OWL Dev. The key takeaway from this step is to obtain the bot's secret, used to authenticate the bot against Discord's API.

### 2. Gather the required parameters

Within CNTO, the Owlbot is deployed on the `Tools Server`. It requires two parameters to run.

 1. Discord channel id to post event reminders, this makes use of `.env` file (find a template in the `.env.template` file)
 2. Discord bot token to authenticate, this is passed using [docker-compose secrets](https://docs.docker.com/compose/use-secrets/). A plain text file named `discord-token.txt` should be placed in the same directory as `docker-compose.yml`, reference `discord-token.txt.template` for an example.

The `.env` parameters can be passed to Owlbot in two different ways:


1. As system environment variables, for example `export OWLBOT_SECRET=1234`
2. As `.env` file in the same directory as the `.env.template`

Owlbot will try to load from a `.env` file, falling back to system variables. If both are present, system variables are used.

**Note** if you use the Owlbot Docker image from our public registry, the `.env` file is not yet created by the build process so you need to rely on environment variables. The `.env` file mechanism is supported for local development environments. We do not plan on adding `.env` file support for staging / production environments.

### 3. Run the Docker image

Start the container through `docker-compose` to ensure proper parameters and secrets loading.

```bash
docker-compose up -d
```

Is the only command you need to get Owlbot up and running.

### Updating the crontab file

By default, the Owlbot will send join reminders 10 minutes before our events start (19:35 CET / CEST). This is configured in the `crontab.txt` file that gets installed inside the Owlbot container upon image build. Changing the `crontab.txt` file content and restarting the container or `docker-compose` execution will have no impact on the actual cron entry installed.

If you need to change the cron entry for debugging purposes without triggering an image rebuild, get access to a shell within the container (only `/bin/sh` since it's based on an `alpine` image) and edit the crontab manually, for example with `crontab -e`.