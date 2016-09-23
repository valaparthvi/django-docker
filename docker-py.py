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

args = parser.parse_args()

print (args.image)
print(args.image, args.name, args.entrypoint, args.working_dir, args.volumes)


# Cli is a Docker Client
# base_url is where the Docker daemon is running
# for the Docker running on the same host, use the default

cli = Client(base_url='unix://var/run/docker.sock')


# Working Directory where the codebase is

if args.working_dir is None:
    args.working_dir = os.getcwd()


def build():
    pass


def run(args):

    # Create container from the given arg inputs
    container = cli.create_container(
        image=args.image,
        # command=args.command,
        name=args.name,
        entrypoint=args.entrypoint,
        working_dir=args.working_dir,
        volumes=args.volumes
    )
    print (container)

    container_id = container['id']

    response = cli.start(container=container.get(container_id))
    print (response)


if __name__ == '__main__':
    run(args)
