"""
Deployment manage commands.

:copyright: (c) 2016 Pinn
:license: All rights reserved

"""

import glob
import click
import subprocess

version = 'latest'

SUCCESS = 0
ecr_url = 'ecr-repository-number.dkr.ecr.us-west-1.amazonaws.com/'
containers = {'runner', 'nginx', 'worker', 'rabbit'}
mapper = {'a': 'nginx:',
          'b': 'runner:',
          'c': 'worker:',
          'd': 'rabbit:'}


@click.command()
@click.option('--fake', default=False, is_flag=True)
def deploy(fake):
    """Subprocess python shell."""
    click.secho('\nChoose deployment step:')
    click.secho('a) Tag and push')
    click.secho('b) Deploy')
    click.secho('c) Tag, Push, Deploy')
    click.secho('d) Tasks')

    choice = click.prompt(click.style('default is b'),
                          type=click.Choice(['a', 'b', 'c']),
                          default='b',
                          show_default=False)

    if choice in ['a', 'c']:
        click.secho('\nChoose container to push:')
        click.secho('a) nginx')
        click.secho('b) runner')
        click.secho('c) worker')
        click.secho('d) rabbit')
        click.secho('e) ALL OF THE ABOVE')

        tag_and_push = click.prompt(click.style('Choose one'),
                                    type=click.Choice(['a', 'b', 'c', 'd', 'e']),
                                    show_default=False)
    if choice in ['b', 'c']:
        click.secho('\nSelect a deployment environment')
        click.secho('a) development')
        click.secho('b) multi')
        click.secho('c) production')

        ch = click.prompt(click.style('(default is a)'),
                          type=click.Choice(['a', 'b', 'c']),
                          default='a',
                          show_default=False)
        ch_dict = {'a': 'development',
                   'b': 'multi',
                   'c': 'production'}
        environment = ch_dict[ch]
        click.secho('\nAre you sure you want to deploy to ', nl=False)
        click.secho(environment, fg='yellow', nl=False)
        confirmed = click.confirm('')

    if choice == 'a':
        """Tag and Push"""
        tag(choice=tag_and_push)
        push(choice=tag_and_push, fake=fake)
        code = untag(choice=tag_and_push)

    if choice == 'b':
        """Deploy"""
        if confirmed:
            code = dep(environment, fake=fake)
        else:
            click.secho('Did not confirm deployment, make sure you are ready!', fg='white')
            code = 99

    if choice == 'c':
        """Tag, Push, Deploy"""
        tag(choice=tag_and_push)
        push(choice=tag_and_push, fake=fake)
        code = untag(choice=tag_and_push)
        if confirmed:
            code = dep(environment, fake=fake)
        else:
            click.secho('Did not confirm deployment, make sure you are ready!', fg='white')
            code = 99

    if choice == 'd':
        code = ecs()

    if code == SUCCESS:
        click.secho('Success deploy command', fg='green')
    else:
        click.secho('Failure deploy command', fg='red')


def tag(choice):
    """Tag for ECR."""
    click.secho('+\n++\n+++ Tagging Image for ECR...')
    if choice in mapper:
        tag = ecr_url + mapper[choice] + version
        image = 'multi_' + mapper[choice] + version
        call = ['docker', 'tag', image, tag]
        code = subprocess.call(call)
    else:
        for container in containers:
            tag = ecr_url + container + ':' + version
            image = 'multi_' + container + ':' + version
            call = ['docker', 'tag', image, tag]
            code = subprocess.call(call)
    if code == SUCCESS:
        click.secho('Sucess Tagging', fg='green')
    else:
        click.secho('Failure Tagging', fg='red')


def untag(choice):
    """Untag image for space."""
    click.secho('+\n++\n+++ Removing tagged image(s)...')
    if choice in mapper:
        tag = ecr_url + mapper[choice] + version
        call = ['docker', 'rmi', tag]
        code = subprocess.call(call)
    if choice == 'e':
        for container in containers:
            tag = ecr_url + container + ':' + version
            call = ['docker', 'rmi', tag]
            code = subprocess.call(call)
    if code == SUCCESS:
        click.secho('Cleaned up tagged images', fg='green')
    else:
        click.secho('Failed to clean up imnages', fg='red')
    return code


def push(choice, fake=False):
    """Push to ECR."""
    click.secho('+\n++\n+++ Pushing image to ECR...')
    call = ['aws', 'ecr', 'get-login', '--region', 'us-west-1']
    p = subprocess.Popen(call, stdout=subprocess.PIPE)
    out, err = p.communicate()
    call = out.split()
    # code = subprocess.call(call)
    code = SUCCESS
    if code == SUCCESS:
        if not fake:
            if choice in mapper:
                tag = ecr_url + mapper[choice] + version
                call = ['docker', 'push', tag]
                # subprocess.call(call)
            if choice == 'e':
                for container in containers:
                    tag = ecr_url + container + ':' + version
                    call = ['docker', 'push', tag]
                    # code = subprocess.call(call)
        click.secho('Success pushing to ECR', fg='green')
        return code
    click.secho('Failed to push to ECR', fg='red')


def ecs():
    """ECS management."""
    # Old ecs commands
    # Deploy handles service and task management via EB so these are just for reference
    click.secho('+\n++\n+++ Deploying tasks and services to ECS...')
    # Using ecs-cli
    call = ['ecs-cli', 'compose', '--file', 'dock/ecs-compose.yml']
    call.extend(['--project-name', 'multi', 'service', 'up'])
    # Using aws ecs
    call = [' aws', 'ecs', 'register-task-definition']
    call.extend(['--cli-input-json', 'file://dock/tasks.json'])
    # code = subprocess.call(call)
    code = SUCCESS
    if code == SUCCESS:
        click.secho('Successful task deployment', fg='green')
        return code
    click.secho('Unsuccessful task deployment', fg='red')


def dep(environment, fake=False):
    """Deploy to EB."""
    click.secho('+\n++\n+++ Zipping and deploying to EB...')
    click.secho('\n> Switching elastic beanstalk', fg='white')
    eb_env = 'multi-' + environment
    call = ['eb', 'use', eb_env]
    # subprocess.call(call)
    call = ['zip', 'deploy.zip', 'Dockerrun.aws.json']
    call.extend(glob.glob('.ebextensions/*'))
    code = subprocess.call(call)
    call = ['rm', 'deploy.zip']
    if code == SUCCESS:
        # if not fake:
            # code = subprocess.call(['eb', 'deploy'])
        click.secho('Success EB Deployment', fg='green')
        subprocess.call(call)
        return code
    click.secho('Failure EB Deployment', fg='red')
    return subprocess.call(call)

if __name__ == '__main__':
    deploy()
