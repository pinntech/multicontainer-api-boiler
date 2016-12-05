*Boiler plate api with docker managed containers that communicate and are elastic beanstalk ready.*

Further Explanations: http://www.timchi.co/single-post/2016/11/10/Docker-izing-Production-Quality-APIs

## Table of Contents

- [Multi](#multi)
    * [Initial](#initial)
    * [Management](#management)

## Initial
Make sure necessary packages are installed via virtual environment

```
 - git clone https://github.com/pinnrepo/multicontainer-api-boiler.git
 - virtualenv -p python2.7 .venv
 - . .venv/bin/activate
 - pip install -r requirements.txt
```

```
Begin by building your base image, this is used by the runner image in order to contain
necessary modules so that building doesn't always go through the download process.

./manage build base

Than you can use compose however you like, suggested

./manage compose up --build

For a faked deploy process run, no subprocesses are called so nothing really happens 
other than taggin of images to fake repositories.

./manage deploy

To clean, 

./manage clean --ecs --volumes --images
```

## Management

Management commands are available for convenience, here's the basic rundown

```shell
Usage: ./manage [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.
```

| Command                   | Description                                                                   |
| ------------------------- | ----------------------------------------------------------------------------- |
| `build`                   | Build docker images with name of image from docker-compose file.              |
|                           | https://docs.docker.com/engine/reference/commandline/build/                   |
| `compose`                 | Docker-compose commands to manage docker runners.                             |
|                           | https://docs.docker.com/compose/reference/                                    |
| `clean`                   | Clean all docker images (local or ecr) with flags.                            |
| `deploy`                  | Deploy the application live after source is validated.                        |

## License

Pinn Technologies, Inc. All rights reserved
