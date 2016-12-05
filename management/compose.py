"""
Docker-compose management commands.

:copyright: (c) 2016 Pinn
:license: All rights reserved

"""

import click
import subprocess


@click.command()
@click.option('--ecs', is_flag=True)
@click.option('--volumes', is_flag=True)
@click.option('--images', is_flag=True)
def clean(ecs, volumes, images):
    """Subprocess python shell."""
    click.secho('+\n++\n+++ Shutting down docker-compose...', fg='white')
    call = ['docker-compose', '-f', 'dock/docker-compose.yml', '-p', 'multi']
    call.append('down')
    subprocess.call(call)
    # Remove images created from docker-compose up
    click.secho('+\n++\n+++ Removing images from project*...', fg='white')
    if ecs or images:
        call = ['docker', 'rmi']
        if ecs:
            call.append('ecr-repository-number.dkr.ecr.us-west-1.amazonaws.com/runner')
            call.append('ecr-repository-number.dkr.ecr.us-west-1.amazonaws.com/worker')
            call.append('ecr-repository-number.dkr.ecr.us-west-1.amazonaws.com/nginx')
            call.append('ecr-repository-number.dkr.ecr.us-west-1.amazonaws.com/rabbit')
        if images:
            call.extend(['multi_nginx', 'multi_runner', 'multi_worker', 'multi_rabbit'])
        subprocess.call(call)
    if volumes:
        p = subprocess.Popen(['docker', 'volume', 'ls', '-q', '-f', 'dangling=true'],
                             stdout=subprocess.PIPE)
        out, err = p.communicate()
        call = ['docker', 'volume', 'rm']
        call.extend(out.split())
        subprocess.call(call)

choices = ['build', 'bundle', 'config', 'create', 'down', 'events', 'exec', 'help', 'kill', 'logs']
choices.extend(['pause', 'post', 'ps', 'pull', 'push', 'restart', 'rm', 'run', 'scale', 'start'])
choices.extend(['stop', 'unpause', 'up', 'version'])


@click.command()
@click.option('--build', is_flag=True)
@click.option('--detach', is_flag=True)
@click.option('--recreate', is_flag=True)
@click.option('--ecs', is_flag=True)
@click.argument('args')
def compose(args, build, recreate, detach, ecs):
    """Subprocess python shell."""
    if ecs:
        call = ['docker-compose', '-f', 'dock/ecs-compose.yml', '-p', 'multi']
    else:
        call = ['docker-compose', '-f', 'dock/docker-compose.yml', '-p', 'multi']
    if args in choices:
        click.secho('docker-compose {}'.format(args))
        call.append(args)
        if detach:
            call.append('-d')
        if build:
            call.append('--build')
        if recreate:
            call.append('--force-recreate')
    else:
        click.secho('\nCompose command is not available see:\n')
        call.append('--help')
    subprocess.call(call)

if __name__ == '__main__':
    compose()
