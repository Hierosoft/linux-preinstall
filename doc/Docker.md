# Docker

## Setup a docker image

## Setup Docker

See docker.debian.sh in linux-preinstall
- also tested with Devuan 4 Chimera

`sudo docker run hello-world`

says:

> Unable to find image 'hello-world:latest' locally
> latest: Pulling from library/hello-world
> 2db29710123e: Pull complete
> Digest: sha256:80f31da1ac7b312ba29d65080fddf797dd76acfb870e677f390d5acba9741b17
> Status: Downloaded newer image for hello-world:latest
>
> Hello from Docker!
> This message shows that your installation appears to be working correctly.
>
> To generate this message, Docker took the following steps:
>  1. The Docker client contacted the Docker daemon.
>  2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
>     (amd64)
>  3. The Docker daemon created a new container from that image which runs the
>     executable that produces the output you are currently reading.
>  4. The Docker daemon streamed that output to the Docker client, which sent it
>     to your terminal.
>
> To try something more ambitious, you can run an Ubuntu container with:
>  $ docker run -it ubuntu bash
>
> Share images, automate workflows, and more with a free Docker ID:
>  https://hub.docker.com/
>
> For more examples and ideas, visit:
>  https://docs.docker.com/get-started/


## Storage
The overlay filesystem uses no storage in and of itself.

[Docker 'overlay' takes too much size - how to debug?](https://stackoverflow.com/questions/70802197/docker-overlay-takes-too-much-size-how-to-debug):
> running df -h I get
> `overlay          79G   70G  5.8G  93% /var/lib/docker/overlay2/a7bcb73019b20505a640593453aee3578647e027ccf90a607ad1806a9b25edd4/merged`
> Any idea how I can check why it takes so much space?

-TheUnreal Jan 21 at 13:38 on

> An overlay filesystem, like a bind mount, doesn't use any disk space itself. What's reported is the disk space of the underlying filesystem. In this case, if you run `df /var/lib/docker` you'll see the same disk space allocated to that underlying filesystem, and you can review what is used on that mount.
>
> If the issue is docker, then `docker system prune` would be a first
> step. If that doesn't help and you see significant usage from the
> /var/lib/docker folder you want to clean, see
> [this answer](https://stackoverflow.com/a/46672068/596285) for
> additional suggestions.

-BMitch answered Jan 21 at 17:17 <https://stackoverflow.com/a/70805169/4541104> [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

The URL above redirects to [Is it safe to clean
docker/overlay2/](https://stackoverflow.com/questions/46672001/is-it-safe-to-clean-docker-overlay2/46672068#46672068)'s
answer at <https://stackoverflow.com/a/46672068/4541104>
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) BMitch:
> . . .

```
$ docker system prune --help

Usage:  docker system prune [OPTIONS]

Remove unused data

Options:
  -a, --all             Remove all unused images not just dangling ones
      --filter filter   Provide filter values (e.g. 'label=<key>=<value>')
  -f, --force           Do not prompt for confirmation
      --volumes         Prune volumes
```
> What a prune will never delete includes:
>
> - running containers (list them with `docker ps`)
> - logs on those containers (see [this post](https://stackoverflow.com/a/42510314/596285) for details on limiting the size of logs)
> - filesystem changes made by those containers (visible with `docker diff`)
> . . .

-BMitch answered Oct 10, 2017 at 16:57 edited Jan 3 at 19:28

> thanks for your reply, sir. But there is another folder under /docker, called /volumes, I would assume this is where they keep the volumes. So I'm still confused what is exactly in the /docker/overlay2 folder. –

-qichao_he Oct 10, 2017 at 23:08

> The overlay2 folder should contain the filesystem layers needed for your images and containers. You're free to ignore this advice, but please don't ask me for advice on how to recover a failed system after you break it, particularly since I gave you a supported way to cleanup your filesystem.

-BMitch Oct 10, 2017

> I found this worked best for me:
> `docker image prune --all`
> By default Docker will not remove named images, even if they are unused. This command will remove unused images.
>
> Note each layer in an image is a folder inside the /usr/lib/docker/overlay2/ folder.

-Sarke [answered Jul 10, 2019 at 6:27](https://stackoverflow.com/a/56964541/4541104) [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

> I had this issue... It was the log that was huge. Logs are here :
> `/var/lib/docker/containers/<container id>/<container id>-json.log`
> You can manage this in the run command line or in the compose file. See there : [Configure logging drivers](https://docs.docker.com/config/containers/logging/configure/)
>
> I personally added these 3 lines to my docker-compose.yml file :
```
my_container:
  logging:
    options:
      max-size: 10m
```

-Tristan answered [Apr 9, 2019 at 7:42](https://stackoverflow.com/a/55587497/4541104) edited Apr 10, 2019 at 8:14 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)



> also had problems with rapidly growing `overlay2`
>
> `/var/lib/docker/overlay2` - is a folder where docker store writable layers for your container. `docker system prune -a` - may work only if container is stopped and removed.
>
> in my i was able to figure out what consumes space by going into `overlay2` and investigating.
>
> that folder contains other hash named folders. each of those has several folders including `diff` folder.
>
> `diff` folder - contains actual difference written by a container with exact folder structure as your container (at least it was in my case - ubuntu 18...)
>
> **so i've used `du -hsc /var/lib/docker/overlay2/LONGHASHHHHHHH/diff/tmp` to figure out that `/tmp` inside of my container is the folder which gets polluted**.
>
> so as a workaround i've used `-v /tmp/container-data/tmp:/tmp` parameter for `docker run` command to map inner `/tmp` folder to host and setup a cron on host to cleanup that folder.
>
> cron task was simple:
>
> -   `sudo nano /etc/crontab`
> -   `*/30 * * * * root rm -rf /tmp/container-data/tmp/*`
> -   `save and exit`
>
> NOTE: `overlay2` is system docker folder, and they may change it structure anytime. Everything above is based on what i saw in there. Had to go in docker folder structure only because system was completely out of space and even wouldn't allow me to ssh into docker container.

-user2932688 [answered Jun 29, 2019 at 13:40](https://stackoverflow.com/a/56817997/4541104) [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

