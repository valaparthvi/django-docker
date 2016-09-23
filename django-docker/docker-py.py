import os
from docker import Client

#base_url is where the docker daemon is running
#currently for the same host system
cli = Client(base_url='unix://var/run/docker.sock')

#project wording directory
wd  = os.getcwd()

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
  print container
  response = cli.start(container=container.get('Id'))
  
if __name__ == '__main__':
  run()
  
