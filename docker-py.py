import os
import argparse
from docker import Client


# Parser to get args input from CLI

parser = argparse.ArgumentParser()

parser.add_argument("--image", "-i", help="Your docker image name", type=str)
parser.add_argument("--name", "-n", help="Name of the Container", type=str)
parser.add_argument("--entrypoint", "-e",
                    help="Your Entrypoint File '.sh'", type=str)
parser.add_argument("--working_dir", "-w", help="Working Directory", type=str)
parser.add_argument("--volumes", "-v", help="Volume list", type=list)
parser.add_argument(
    "--docker_host", help='''tcp://ip-addr for the host where your docker daemon is running,
    other then host of your local system''')
parser.add_argument("--path", "-p",
                    help='''Path to the directory,
                    where your Dockerfile is located''')
parser.add_argument("--tag", "-t", help="Tag for the image")
parser.add_argument("--dockerfile", "-df", help="Dockerfile")
parser.add_argument("--container_limits", "-c",
                    help='''JSON for container resources:
                    memory, memswap, cpushares, cpusetcpus''')

args = parser.parse_args()

print (args.image)
print(args.image, args.name, args.entrypoint, args.working_dir, args.volumes)


# Cli is a Docker Client
# base_url is where the Docker daemon is running
# for the Docker running on the same host, use the default

cli = Client(base_url='unix://var/run/docker.sock')


# Working Directory where the codebase is

if args.working_dir is None:
    wd = os.getcwd()
else:
    wd = args.working_dir


def build():
    pass


def run(info):

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
    print (response)


if __name__ == '__main__':
    run()
