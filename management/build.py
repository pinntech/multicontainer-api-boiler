"""
Docker manage commands for all containers.

:copyright: (c) 2016 Pinn
:license: All rights reserved

"""

import click
import subprocess


@click.command()
@click.argument('args')
def build(args):
    """Subprocess python shell."""
    if 'nginx' in args:
        call = ['docker', 'build', '--force-rm']
        call.extend(['-t', 'nginx', 'dock/nginx'])
        click.echo('+\n++\n+++ Building nginx docker container...')
        subprocess.call(call)

    if 'rabbit' in args:
        call = ['docker', 'build', '--force-rm']
        call.extend(['-t', 'rabbit', 'dock/rabbit'])
        click.echo('+\n++\n+++ Building rabbit docker container...')
        subprocess.call(call)

    if 'worker' in args:
        call = ['docker', 'build', '--force-rm']
        call.extend(['-t', 'worker', 'dock/worker'])
        click.echo('+\n++\n+++ Building worker docker container...')
        subprocess.call(call)

    if 'base' in args:
        call = ['docker', 'build', '--force-rm']
        call.extend(['-t', 'multi_base', 'dock/base'])
        click.echo('+\n++\n+++ Building base docker container...')
        subprocess.call(call)

    if 'run' in args:
        call = ['docker', 'build', '--force-rm']
        call.extend(['-t', 'run', '-f', 'dock/run/Dockerfile', '.'])
        click.echo('+\n++\n+++ Building runner docker container...')
        subprocess.call(call)

if __name__ == '__main__':
    build()
