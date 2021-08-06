import logging
import os
import re
from sys import exit
from pathlib import Path

import frontmatter
from invoke import task
from invoke.tasks import call
from dotenv import load_dotenv
import requests
from rich.console import Console
from pydantic import BaseSettings
from jinja2 import Environment, FileSystemLoader, Template
import yaml


class DictObj:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Page(DictObj):
    pass


class Site(DictObj):
    pass


class Settings(BaseSettings):
    port = 4000
    host = '0.0.0.0'
    course: str = None
    deploy_token: str = None
    lecturer_folder: str = None
    log_level: str = 'INFO'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
logging.basicConfig(level=settings.log_level)

# load site settings
file = open('_config.yml')
config = yaml.load(file, Loader=yaml.Loader)
site = Site(**config)



# load env variables
load_dotenv('.env')

console = Console()

# jinja2 setup
j2_env = Environment(
  loader=FileSystemLoader(
    '/pandoc/j2_templates'),
  autoescape=False
)



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

    with console.status('[bold green] Cleaning...') as status:
        cmd = 'bundle exec jekyll clean'
        ctx.run(cmd, shell='/bin/sh')
        ctx.run(f'rm -rf {settings.course}.zip')


@task
def serve(ctx, lecturer=False, destination='_site'):
    """
    Runs jekyll serve
    """

    # prepare
    _configs = ['_config.yml']
    _destination = Path(destination)
    _base_url = None if settings.course is None else f"/{settings.course}"

    # prepare lecturer stuff
    if lecturer is True:
        _configs.append('_config_lecturer.yml')
        _base_url = f'/{settings.lecturer_folder}' if _base_url is None else f"{_base_url}/{settings.lecturer_folder}"
        _destination = _destination / settings.lecturer_folder

    # prepare command
    cmd = [
        'bundle exec jekyll serve',
        '--incremental',
        f'--host {settings.host}',
        f'--port {settings.port}',
        '--drafts',
        f'--destination {_destination}',
        f'--config={",".join(_configs)}'
    ]

    if _base_url is not None:
        cmd.append(f'--baseurl {_base_url}')

    # serve
    with console.status('[bold green] Serving the content...') as status:
        ctx.run(' '.join(cmd), shell='/bin/sh')


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


def _preprocess_labs(ctx, path):
    """
    Preprocess single labs file.
    """
    print(f'Preprocessing lab {path} ...')

    # get chapter document
    doc = frontmatter.load(path)

    if 'layout' in doc and doc['layout'] == 'labs':
        # remove {% if site.lecturer %} blocks
        regex = re.compile(
            r'\{%\s+if\s+site\.lecturer\s+%\}([^\{]*)\{%\s+endif\s+%\}',
            re.MULTILINE|re.DOTALL
            )
        doc.content = regex.sub('', doc.content)

    # render template
    if 'epub' in doc and doc['epub']['type'] == 'foreword':
        template = j2_env.get_template('epub-page.html')
        return template.render(meta = doc.metadata, content = doc.content)

    elif 'layout' in doc and doc['layout'] == 'labs':
        # process doc.content as template first
        tpl = Template(doc.content, comment_start_string='<!--', comment_end_string='-->')
        content = tpl.render(page = Page(**doc.metadata), site = site)

        # render document with template
        template = j2_env.get_template('epub-lab.html')
        return template.render(meta = doc.metadata, content = content)

    elif 'type' in doc and doc['type'] == 'imprint':
        template = j2_env.get_template('epub-imprint.html')
        return template.render()

    else:
        return doc.content


def _preprocess_lecture(ctx, path):
    """
    Preprocess single lecture file.
    """
    print(f'Preprocessing lecture {path} ...')

    # get chapter document
    doc = frontmatter.load(path)

    if 'layout' in doc and doc['layout'] == 'lecture':

        # filter stuff in chapter content
        # remove all the links to slides [slide](url)
        regex = re.compile(r'\(\[slide\]\([^)]*\)\)[^\S\r\n]*')
        doc.content = regex.sub('', doc.content)

        # remove first three characters (the list items and spaces)
        regex = re.compile(r'^(\* |  )', re.MULTILINE|re.DOTALL)
        doc.content = regex.sub('', doc.content)

        # remove {% include %}
        regex = re.compile(r'{%\s+include\s+.*\s+%}', re.MULTILINE)
        doc.content = regex.sub('', doc.content)

        # remove {% if site.lecturer %} blocks
        regex = re.compile(r'\{%\s+if\s+site\.lecturer\s+%\}([^\{]*)\{%\s+endif\s+%\}',
                re.MULTILINE|re.DOTALL)
        doc.content = regex.sub('', doc.content)

    # render template
    if 'epub' in doc and doc['epub']['type'] == 'foreword':
        template = j2_env.get_template('epub-page.html')
        return template.render(meta = doc.metadata, content = doc.content)

    elif 'layout' in doc and doc['layout'] == 'lecture':
        # process doc.content as template first
        tpl = Template(doc.content, comment_start_string='<!--', comment_end_string='-->')
        content = tpl.render(page = Page(**doc.metadata), site = site)

        # render document with template
        template = j2_env.get_template('epub-lecture.html')
        return template.render(meta = doc.metadata, content = content)

    elif 'type' in doc and doc['type'] == 'imprint':
        template = j2_env.get_template('epub-imprint.html')
        return template.render()

    else:
        return doc.content


@task
def epub(ctx, _lectures=True, _year='2021'):
    """
    Builds epub.
    """

    # prepare content type
    content_type = 'lectures' if _lectures else 'labs'

    # load metadata
    path = Path(_year)
    file = open(path / f'metadata-{content_type}.yaml')
    metadata = yaml.load(file, Loader=yaml.Loader)
    output = 'download/ebook.epub'

    # preprocess sources
    with console.status('[bold green] Preprocessing sources...') as status:
        for source in metadata['sources']:
            with open(path / f'_{source}', 'w') as f:
                if content_type == 'lectures':
                    f.write(_preprocess_lecture(ctx, path / source))
                else:
                    f.write(_preprocess_labs(ctx, path / source))

    # prepare pandoc default params
    cmd = [
        'pandoc',
        f'--defaults /pandoc/defaults/epub-{content_type}.yaml',
        f'-o {output}'
    ]

    # append sources
    for source in metadata['sources']:
        cmd.append(f'_{source}')

    # build epub
    with ctx.cd(_year):
        with console.status('[bold green] Building epub...') as status:
            ctx.run(' '.join(cmd), shell='/bin/sh')

            # cleanup
            for source in metadata['sources']:
                ctx.run(f'rm _{source}')

    # print destination file
    logging.info(f'Book was written to {output}.')


@task
def pdf(ctx, _lectures=True, _year='2021'):
    """
    Builds PDF document.
    """

    # prepare content type
    content_type = 'lectures' if _lectures else 'labs'

    # load metadata
    path = Path(_year)
    file = open(path / f'metadata-{content_type}.yaml')
    metadata = yaml.load(file, Loader=yaml.Loader)
    output = 'lectures.tex'

    # preprocess sources
    with console.status('[bold green] Preprocessing sources...') as status:
        for source in metadata['sources']:
            with open(path / f'_{source}', 'w') as f:
                if content_type == 'lectures':
                    f.write(_preprocess_lecture(ctx, path / source))
                else:
                    f.write(_preprocess_labs(ctx, path / source))


    # prepare pandoc default params
    cmd = [
        'pandoc',
        f'--defaults /pandoc/defaults/pdf-{content_type}.yaml',
        f'-o {output}'
    ]

    # append sources
    for source in metadata['sources']:
        cmd.append(f'_{source}')

    # build pdf
    with ctx.cd(_year):
        with console.status('[bold green] Building PDF...') as status:
            ctx.run(' '.join(cmd), shell='/bin/sh')

            # cleanup
            for source in metadata['sources']:
                ctx.run(f'rm _{source}')

    # print destination file
    logging.info(f'Book was written to {output}.')


# TODO treba inac vyriesit - rovno z entrypointu
@task
def shell(ctx):
    """
    Runs shell in the courseware (current) directory.
    """
    ctx.run('/bin/bash')
