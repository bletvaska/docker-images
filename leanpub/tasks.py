import json
import logging
import os
import re
import subprocess
from pathlib import Path

import frontmatter
from invoke import task
from rich.console import Console
import yaml


logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))

LIQUID_TEMPLATES_DIR = Path('/app/pandoc/liquid_templates')


def render_liquid(template_str, **variables):
    """
    Renders a Liquid template by shelling out to Ruby (liquid is already a
    jekyll dependency), so preprocessing doesn't need a second Python
    templating library alongside it.
    """
    payload = json.dumps({'template': template_str, 'vars': variables}, default=str)
    result = subprocess.run(
        ['ruby', '/app/liquid_render.rb'],
        input=payload,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def render_template(name, **variables):
    template_str = (LIQUID_TEMPLATES_DIR / name).read_text()
    return render_liquid(template_str, **variables)


# load site settings
file = open('_config.yml')
site = yaml.load(file, Loader=yaml.Loader)

console = Console()


def _preprocess_labs(ctx, path, format='html'):
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
        return render_template('epub-page.liquid', meta=doc.metadata, content=doc.content)

    elif 'layout' in doc and doc['layout'] == 'labs':
        # process doc.content as a template first, so authors can reference
        # {{ page.xxx }} / {{ site.xxx }} inline in their markdown
        content = render_liquid(doc.content, page=doc.metadata, site=site)

        # render document with template
        return render_template('epub-lab.liquid', meta=doc.metadata, content=content)

    elif 'type' in doc and doc['type'] == 'imprint':
        return (LIQUID_TEMPLATES_DIR / 'epub-imprint.liquid').read_text()

    else:
        return doc.content


def _preprocess_lecture(ctx, path, format='html', replacements=None):
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

    # replacements
    if replacements is not None:
        for key in replacements:
            doc.content = doc.content.replace(key, replacements[key])

    # render template
    if 'epub' in doc and doc['epub']['type'] == 'foreword':
        return render_template('epub-page.liquid', meta=doc.metadata, content=doc.content)

    elif 'layout' in doc and doc['layout'] == 'lecture':
        # process doc.content as a template first, so authors can reference
        # {{ page.xxx }} / {{ site.xxx }} inline in their markdown
        content = render_liquid(doc.content, page=doc.metadata, site=site)

        # render document with template
        template_name = 'pdf-lecture.liquid' if format == 'pdf' else 'epub-lecture.liquid'
        return render_template(template_name, meta=doc.metadata, content=content)

    elif 'type' in doc and doc['type'] == 'imprint':
        return (LIQUID_TEMPLATES_DIR / 'epub-imprint.liquid').read_text()

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
    output = f'download/smart.lectures.{_year}.epub'

    # preprocess sources
    # with console.status('[bold green] Preprocessing sources...') as status:
    print('>> preprocessing sources...')
    for source in metadata['sources']['epub']:
        with open(path / f'_{source}', 'w') as f:
            if content_type == 'lectures':
                f.write(_preprocess_lecture(ctx, path / source, 'html'))
            else:
                f.write(_preprocess_labs(ctx, path / source))

    # prepare pandoc default params
    cmd = [
        'pandoc',
        f'--defaults epub-{content_type}',
        f'-o {output}'
    ]

    # append sources
    for source in metadata['sources']['epub']:
        cmd.append(f'_{source}')

    # build epub
    print('>> building epub...')
    print(' '.join(cmd))
    with ctx.cd(_year):
        # with console.status('[bold green] Building epub...') as status:
            ctx.run(' '.join(cmd), shell='/bin/sh')

            # cleanup
            for source in metadata['sources']['epub']:
                ctx.run(f'rm _{source}')

    # print destination file
    logging.info(f'Book was written to {_year}/{output}.')


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
        for source in metadata['sources']['pdf']:
            with open(path / f'_{source}', 'w') as f:
                if content_type == 'lectures':
                    content = _preprocess_lecture(ctx, path / source, 'pdf', metadata['replacements']['pdf'])
                    f.write(content)
                else:
                    f.write(_preprocess_labs(ctx, path / source))

    # prepare pandoc default params
    cmd = [
        'pandoc',
        f'--defaults pdf-{content_type}',
        f'-o {output}',
        # '--include-after-body appendix.01.md',
        # '--include-after-body appendix.02.md',
    ]

    # append sources
    for source in metadata['sources']['pdf']:
        cmd.append(f'_{source}')

    # build pdf
    with ctx.cd(_year):
        with console.status('[bold green] Building PDF...') as status:
            ctx.run(' '.join(cmd), shell='/bin/sh')

            # cleanup
            for source in metadata['sources']['pdf']:
                ctx.run(f'rm _{source}')

    # print destination file
    logging.info(f'Book was written to {output}.')
