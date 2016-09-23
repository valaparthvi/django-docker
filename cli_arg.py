import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--image", "-i", help="Your docker image name", type=str)

parser.add_argument("--name", "-n", help="enter name", type=str)

parser.add_argument("--entrypoint", "-e",
                    help="Your Entrypoint File", type=str)

parser.add_argument("--working_dir", "-w", help="Working Directory", type=str)

parser.add_argument("--volumes", "-v", help="Volume list", type=list)

args = parser.parse_args()

print(args.image, args.name, args.entrypoint, args.working_dir, args.volumes)
