# Demo Order
1. Try a DevContainer Sample
2. CFBD Demo
3. Build a DevContainer from Scratch
4. Use a pre-built template
5. Look at a more complex example
6. CodeSpaces!

---

## CFBD Demo
1. This looks interesting: https://blog.collegefootballdata.com/introduction-to-cfb-analytics/
2. From the Remote menu (lower-left), choose `Open folder in container`
     - Choose the `cfbd` folder
     - Use the `Anaconda (Python 3)` image
3. Open the Jupyter notebook and run the first cell
4. Failed due to the `cfbd` package not being installed.
     - run `pip install cfbd`
5. If we were to rebuild the container, the package would no longer be installed 
6. Add it to the `Dockerfile` (it could also be done via the `postCreateCommand` in `devcontainer.json`)
```docker
RUN pip install cfbd
```
```json
"postCreateCommand": "pip install cfbd"
```
7. Keep running - should fail now due to authentication
8. Need to introduce an environment variable
`devcontainer.json`
```json
  "containerEnv": {
    "CFBD_API_KEY": "${localEnv:CFBD_API_KEY}"
  },
```
9. Rebuild container again
10. Should be able to run through completely now


---

## Walk-through for DevContainer from scratch
1. Create folder and open in code
2. Add folder: `.devcontainer`
3. Add files:
    - Dockerfile
    - devcontainer.json

`Dockerfile`:
```docker
FROM mcr.microsoft.com/dotnet/sdk:7.0
```
`devcontainer.json`
```json
{
  "name": "Demo",
  "build": {
    "dockerfile": "Dockerfile"
  }
}
```

4. Re-open folder in container
5. Open terminal

```
dotnet new web -n demo -o .
```

6. Add c# extension(s). Note: at this point, if the container is recreated, the extension s will be missing again
7. Add the extension(s) to the `devcontainer.json` file
8. Add compile and debug assets (via command pallette) and Run!
9. Add some settings to the `devcontainer.json` file:

```json
"settings": {
    "workbench.colorTheme": "Default Light+",
    "editor.fontSize": 24,
    "workbench.colorCustomizations": {
        "activityBar.activeBackground": "#c88a20",
        "activityBar.background": "#c88a20",
        "activityBar.foreground": "#15202b",
        "activityBar.inactiveForeground": "#15202b99",
        "activityBarBadge.background": "#126e4c",
        "activityBarBadge.foreground": "#e7e7e7",
        "commandCenter.border": "#e7e7e799",
        "sash.hoverBorder": "#c88a20",
        "statusBar.background": "#9c6c19",
        "statusBar.foreground": "#e7e7e7",
        "statusBarItem.hoverBackground": "#c88a20",
        "statusBarItem.remoteBackground": "#9c6c19",
        "statusBarItem.remoteForeground": "#e7e7e7",
        "titleBar.activeBackground": "#9c6c19",
        "titleBar.activeForeground": "#e7e7e7",
        "titleBar.inactiveBackground": "#9c6c1999",
        "titleBar.inactiveForeground": "#e7e7e799"
    }
}
```

10. Add a post-create command:
```json
"postStartCommand": "dotnet restore"
```
11. Add `zsh` to the container (in `Dockerfile`)

```docker
RUN apt-get update \
&& apt-get install -y zsh \
&& sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
```

12. Add configure the container to use it (in `devcontainer.json` settings):

```json
"terminal.integrated.defaultProfile.linux": "zsh",
```

13. We can pre-build images to speed things up

```shell
devcontainer build --workspace-folder ./ --image-name dev-container-demo
docker tag dev-container-demo localhost:9000/dev-container-demo:1
docker push localhost:9000/dev-container-demo:1
```

14. Then we can use that pre-made image in our `devcontainer.json` file instead:

```json
{
    "image": "localhost:9000/dev-container-demo:1"
}
```

15. Microsoft has some nice pre-made images for us to use. Let's use those:
```json
{
    "image": "mcr.microsoft.com/devcontainers/dotnet:0-7.0"
}
```

16.  Add some other services and convert to using `docker-compose.yml`:
```yml
version: "3.8"

services:
   app:
      image: mcr.microsoft.com/devcontainers/dotnet:0-7.0
      volumes:
         - ..:/workspace:cached
      command: sleep infinity
      network_mode: service:db
      depends_on:
         - db
         - rabbitmq

   db:
      image: postgres
      restart: unless-stopped
      ports:
         - "5432"
      environment:
         POSTGRES_PASSWORD: demo
         POSTGRES_USER: demo
         POSTGRES_DB: demo

   rabbitmq:
      image: rabbitmq:3-management
      ports:
         - "5672"
         - "15672"
      environment:
         - RABBITMQ_DEFAULT_USER=demo
         - RABBITMQ_DEFAULT_PASS=demo
      restart: unless-stopped
```

17. Update `devcontainer.json` to use the `docker-compose.yml` configuration:
```json
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
```

18. Rebuild the container
19. See the RabbitMQ Admin site running: [http://localhost:15672/](http://localhost:15672/)
