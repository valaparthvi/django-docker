import os
import argparse
from docker import Client
from io import BytesIO
from logs import *

# Parser to get args input from CLI
parser = argparse.ArgumentParser()

# args flags to get inputs
parser.add_argument("--mode", "-m", help="Mode for Docker build/run")
parser.add_argument("--image_name", "-i",
                    help="Your docker image name", type=str)
parser.add_argument("--name", "-n", help="Name of the Container", type=str)
parser.add_argument("--entrypoint", "-e",
                    help="Your Entrypoint File '.sh'", type=str)
parser.add_argument("--working_dir", "-w", help="Working Directory", type=str)
parser.add_argument("--volumes", "-v", help="Volume list", type=list)
parser.add_argument("--docker_host",
                    help='''tcp://ip-addr for the host where your docker daemon is running,
    other then host of your local system''')
parser.add_argument("--path", "-p",
                    help='''Path to the directory,
                    where your Dockerfile is located''')
parser.add_argument("--tag", "-t", help="Tag for the image")
parser.add_argument("--dockerfile", "-df", help="Dockerfile")
parser.add_argument("--container_limits", "-c",
                    help='''JSON for container resources:
                    memory, memswap, cpushares, cpusetcpus''')
parser.add_argument("--port", help="port to expose", type=int)
args = parser.parse_args()

print (args.image_name)
print(args.image_name, args.name, args.entrypoint,
      args.working_dir, args.volumes)


# Cli is a Docker Client
# base_url is where the Docker daemon is running
# for the Docker running on the same host, use the default
if args.docker_host is not None:
    cli = args.docker_host
else:
    cli = Client(base_url='unix://var/run/docker.sock')


# Working Directory where the codebase is
if args.working_dir is None:
    wd = os.getcwd()
else:
    wd = args.working_dir

if args.image_name is None:
    args.image_name = 'django'

if args.tag is None:
    args.tag = 'latest'

maintainer = os.uname().nodename

# Build function for Docker Build


def build(args):
    # 1 Make a Dockerfile from the args given,
    # 2 open in the file obj f
    # 3 cli.build with given params
    # return the image id
    try:
        if args.dockerfile is None:
            Dockerfile = '''FROM %s:%s
            MAINTAINER %s
            ENV DOCKYARD_SRC=%s
            ENV DOCKYARD_SRVHOME=/srv
            ENV DOCKYARD_SRVPROJ=/srv/%s
            RUN apt-get update && apt-get -y upgrade
            RUN apt-get install -y python3 python3-pip
            WORKDIR $DOCKYARD_SRVHOME
            RUN mkdir media static logs
            VOLUME %s
            COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ
            RUN pip3 install -r $DOCKYARD_SRVPROJ/requirements.txt
            EXPOSE %d
            WORKDIR $DOCKAYRD_SRVPROJ
            COPY %s
            ENTRYPOINT[%s]''' % (args.image_name, args.tag, maintainer,
                                 wd, wd, args.volumes, args.port,
                                 args.entrypoint, args.entrypoint)
            f = BytesIO(Dockerfile.encode('utf-8'))
        else:
            f = args.dockerfile

        response = [line for line in cli.build(
            rm=True, tag=args.tag, fileobj=f)]

        # check if image was successfully build
        if b"Successfully build" in response[len(response) - 1]:
            return response

        f.close()

    except Exception as e:
        logger.exception("%s", str(e))

# Run function for Docker Run


def run(args):

    container = cli.create_container(
        image='django',
        command='/bin/sleep 1000',
        name='Demo-Django-Docker',
        entrypoint=[''],
        working_dir=wd,
        volumes=['']
    )

    print (container)
    response = cli.start(container=container.get('Id'))
    return response


if __name__ == '__main__':
    # pseudo code
    if args.mode == 'run' or 'r':
        run(args)

    elif args.mode == 'build' or 'b':
        build(args)

    elif args.mode == 'build+run' or 'b+r':
        build(args)
        run(args)
    else:
        print("Enter mode.")
