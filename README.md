# CNTO Owlbot

## What is Owlbot

Owlbot is CNTO's omnipresent assistant. It is currently implemented as a TeamSpeak user for populating our `stats` pages, and on Discord for automated member pings before our operations begin. R&D has plans to expand the Discord presence to enable staff members to carry out their tasks directly from our Discord, but this is a WIP. Currently, this repository contains the Discord features of the bot.

## Owlbot features

 - Welcome new users joining the Discord server. Upon starting the Docker image, Owlbot connects to the Guild passed as argument and waits for new users to join the guild; whenever a new joiner is detected, Owlbot sends a welcome message pinging the new joiner and providing useful links and references.
 - Arma3 operation notification. An optional `operation-notification` command can be passed to `owlbot.py`, in this case Owlbot sends a fire-and-forget type notification to a preset channel pinging community members to remind them to join an upcoming Arma3 operation. The command can be invoked on the host machine (i.e. from outside the Docker container) through `docker exec` or `docker compose exec` to leverage cron jobs.

## Running Owlbot

Owlbot is available as [a Docker image](https://hub.docker.com/repository/docker/cntoarma/owlbot/general), published on CNTO's DockerHub registry. The `cntoarma/owlbot:dev` image is reserved for development builds, for production use the latest tag available based on SemVer (we are working on creating the `cntoarma/owlbot:latest` tag).

You should run Owlbot through `docker compose`, find an example configuration in the `docker-compose.yml` file.

If you are a CNTO Staff member and looking for how R&D deployed this bot, refer to the Forum wiki pages.

### Passing Discord authentication token to Owlbot

Owlbot reads the Discord authentication token from a local file (`/run/secrets/discord_secret`). If using `docker compose`, leverage [the `secrets` section](https://docs.docker.com/compose/use-secrets/). If you are not using docker compose, you will need to [set up the secret](https://docs.docker.com/engine/swarm/secrets/#about-secrets) yourself.

### Required parameters

Separate from the Discord token, a few configuration parameters are required and Owlbot reads them from environment variables. Find an example configuration (suitable for CNTO production environment) in the `config` file. Using docker compose, we pass parameters with the `env_file` command; if you don't use docker compose you will need to pass them one by one upon starting the container.

```
NOTIFICATION_CHANNEL_ID     # Discord channel where members are pinged before operations begin
WELCOME_CHANNEL_ID          # Discord channel where newjoiners are linked to for reading rules and regulations
GUILD_ID                    # Id of the Discord guild (aka Discord server)
INTERVIEWER_ROLE_ID         # Role id of interviewing team, used to ping relevant staff whenever a new user joins
```

The ids listed above can be found on the Discord server by right clicking on the relevant item (i.e. channel, role). To get the "Copy ID" option, make sure you enable Discord Developer mode on your client.

## Contributing

There is not git workflow set in stone, we try to keep things as simple as possible. If you want to contribute to Owlbot: create a new branch from `main`, push your changes to the repository in a feature branch (naming should be along the lines of `feature/a_relevant_name`), open a Pull Request and request a review.
We try to keep Issues updated with a list of tasks, but no guarantees.

### Setting up a local development environment

The use of `virtualenv` or `conda` is recommended to run a Python virtual environment. When working on a new feature or making moderate-to-heavy changes on the codebase, you might want to test the code locally before containerising the application. This requires a local setup of the Discord auth token and environment variables.

 - To pass the Discord auth token: we have a testing Discord server, ask R&D Manager for the token. Create a file the Owlbot can read (i.e. `/run/secrets/discord_token`) on your filesystem containing the token.
 - To pass the environment variables: there are preconfigured options in the `config` and `config.cnto-test-server` files, to export their values to your environment you can run the following:
    ```bash
    set -o allexport
    source CONFIGURATION_FILE
    set +o allexport
    ```

### Building Docker images

If developing locally, you'll want to make sure the changes in the application don't break the Docker image so build the image with the `experimental` tag and update `docker-compose.yml` to use said image. Do not push the image tagged as `experimental` to DockerHub.

This GitHub repository is configured with workflows that automatically build, tag and push the Docker image to CNTO DockerHub registry. The workflows are enabled on the `main` and `dev` branches (workflow specification are contained in the `.github/workflows` directory of this repository). Whenever a new commit is pushed to either branches, workflows are available to start although they require manual approval from the R&D team to proceed.

If you are releasing a new version of Owlbot, make sure to change the tag in `.github/workflows/stable-image-build.yml` (we are working on automating tag release using git tags).