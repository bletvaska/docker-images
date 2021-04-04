import os
from sys import exit
from pathlib import Path

from invoke import task
from invoke.tasks import call
from dotenv import load_dotenv
import requests
from rich.console import Console

# load env variables
load_dotenv('.env')

console = Console()


# https://stackoverflow.com/a/1855118/1671256
# def zipdir(path, ziph):
    # # ziph is zipfile handle
    # for root, dirs, files in os.walk(path):
        # for file in files:
            # ziph.write(os.path.join(root, file),
                       # os.path.relpath(os.path.join(root, file),
                                       # os.path.join(path, '..')))


@task
def build(ctx, destination='_site', lecturer=False):
    """
    Build your site.
    """

    # prepare 
    configs = ['_config.yml']
    _destination = Path(destination)

    # prepare lecturer's settings
    if lecturer is True:
        configs.append('_config_lecturer.yml')
        _destination = _destination / os.getenv('LECTURER_FOLDER')

    # TODO na co je tu incremental, ked bude deploy? a rovnako drafts?
    # prepare command
    cmd = ( 
            'bundle exec jekyll build '
            '--incremental '
            '--drafts '
            f'--destination {_destination} '
            f'--config={",".join(configs)}'
          )

    # build
    with console.status('[bold green] Building...') as status:
        ctx.run(cmd, shell='/bin/sh')


@task 
def clean(ctx):
    """
    Clean the site (removes site output and metadata file) without building.
    """

    course = os.getenv('COURSE')

    with console.status('[bold green] Cleaning...') as status:
        cmd = 'bundle exec jekyll clean'
        ctx.run(cmd, shell='/bin/sh')
        ctx.run(f'rm -rf {course}.zip')


@task
def serve(ctx, lecturer=False, destination='_site'):
    """
    Runs jekyll serve
    """

    # prepare
    _configs = ['_config.yml']
    _destination = Path(destination)
    _base_url = f"/{os.getenv('COURSE')}"

    # prepare lecturer stuff
    if lecturer is True:
        _configs.append('_config_lecturer.yml')
        _base_url = f"{_base_url}/{os.getenv('LECTURER_FOLDER')}"
        _destination = _destination / os.getenv('LECTURER_FOLDER')

    # prepare command
    cmd = ( 
            'bundle exec jekyll serve '
            '--incremental '
            '--host 0.0.0.0 '
            '--drafts '
            f'--destination {_destination} '
            f'--baseurl {_base_url} '
            f'--config={",".join(_configs)}'
          )

    with console.status('[bold green] Serving the content...') as status:
        ctx.run(cmd, shell='/bin/sh')


@task(pre=[
    clean, 
    call(build, destination='_public'), 
    call(build, destination=f'_public', lecturer=True)
    ])
def deploy(ctx, destination='_public'):
    """
    Deploys course to the web.
    """

    token = os.getenv('DEPLOY_TOKEN')
    course = os.getenv('COURSE')

    with console.status('[bold green] Packaging...') as status:
        # zip
        # from pathlib import Path

        with ctx.cd(destination):
            ctx.run(f'zip -r ../{course}.zip .')

    # HTTP POST
    with console.status('[bold green] Uploading...') as status:
        response = requests.post(f'https://kurzy.kpi.fei.tuke.sk/uploads/{course}',
            headers={
                'Authorization': f'Token {token}'
            },
            files={
                'package': open(f'{course}.zip', 'rb')
            }
        )

        # check result
        if response.status_code != 200:
            print(f'Error: {response.status_code}')
            print(response.text)
            exit(1)

    # cleanup
    with console.status('[bold green] Cleanup...') as status:
        ctx.run(f'rm -rf {course}.zip {destination}')


@task
def test(ctx):
    print('testing...')
