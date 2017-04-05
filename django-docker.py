
'''
django-docker is a small utility to generate the 'docker-compose.yml',
Docker Images of each component in your application stack;
nginx, django, db or more if you want to add any.
Simply run this in CLI with python3 django-docker.py
'''
import collections
import os
import readline
import sys
import subprocess
import yaml

readline.set_completer_delims('\t\n;')
readline.parse_and_bind("tab: complete")

print('\n---------------------------------\n')
print('Enter the project directory details below,\n')

web_dir = input('Enter \'absolute\' path to django/flask directory : ')
if not os.path.isdir(web_dir):
    sys.exit('Enter the correct details of the django/flask directory!')

nginx_dir = {'yes': True, 'no': None}[
    str(input('have a nginx directory? (yes/no) : '))]
if nginx_dir:
    nginx_dir = input('Enter \'absolute\' path to the nginx directory : ')

db_dir = {'yes': True, 'no': None}[
    str(input('have a db directory? (yes/no) : '))]
if db_dir:
    db_dir = input('Enter \'absolute\' path to the db directory : ')


dir_config = {'web_dir': web_dir,
              'nginx_dir': nginx_dir,
              'db_dir': db_dir}

for config in dir_config.items():
    if config[1] is not None:
        if os.path.exists(config[1] + 'Dockerfile'):
            try:
                f = open(config[1] + 'Dockerfile')
                print('\nFor ', config[0],
                      'we\'ve found the below configurations\n')
                for item in [item.split('\n') for item in f.readlines()]:
                    print(item[0])
                print('\n')
            except IOError:
                print('Could not open the file Dockerfile for ', config[0])
                continue
        else:
            print('\nNo Dockerfile found for ', config[0])
            choice = {'yes': True, 'no': False}[str(input(
                '''\nWant to create one for it?
                (for Dockerfile reference https://goo.gl/R1tmsw)
                (yes or no) : '''))]
            if choice:
                subprocess.check_call(['nano', config[1] + 'Dockerfile'])

if {'yes': True, 'no': False}[str(input(
        'Create docker-compose.yml? (yes or no) :'))]:
    yml_config = collections.OrderedDict()

    print('\nSetting compose version=3...\n')
    yml_config['version'] = '3'

    print('Setting services for each component...\n')
    yml_config['services'] = {}

    for item in dir_config.items():
        if item[1] is not None:
            yml_config['services'][item[0]] = {}
            yml_config['services'][item[0]][
                'build'] = './' + item[1].split('/')[-1]
            yml_config['services'][item[0]]['command'] = input(
                'Enter the command for ' + item[0] + ' : ')
            yml_config['services'][item[0]]['volumes'] = input(
                'Enter the volumes config : ')
            yml_config['services'][item[0]]['ports'] = input(
                'Enter the list of ports combination : ')

    yml_file = open('docker-compose.yaml', 'w')
    yml_file.write(yaml.dump(yml_config, default_flow_style=False))
    print('\n_______Wrote the Docker-Compose.yaml______\n')
