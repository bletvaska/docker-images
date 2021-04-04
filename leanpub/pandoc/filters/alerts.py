#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create alerts from blockquote, if the syntax of first line is

> [alert] alert title
"""

from panflute import Str, Space, Div, Header, Span, BlockQuote
import panflute as pf

def eprint(*args, **kwargs):
    with open('/tmp/out', 'a') as f:
        print(*args, file=f, **kwargs)


mapping = {
    '[comment]': {
        'classes': ['alert', 'alert-primary', 'theme-alert-info'],
        'icon-classes': ['fas', 'fa-info-circle'],
        'title': 'Poznámka'
    },
    '[warning]': {
        'classes': ['alert', 'alert-danger', 'theme-alert-danger'],
        'icon-classes': ['fas', 'fa-exclamation-circle'],
        'title': 'Upozornenie'
    },
    '[lecturer]': {
        'classes': ['alert', 'alert-warning', 'theme-alert-lecturer'],
        'icon-classes': ['fas', 'fa-paperclip'],
        'title': 'Poznámky pre učiteľa'
    },
    '[solution]': {
        'classes': ['alert', 'alert-secondary', 'theme-alert-solution'],
        'icon-classes': ['fas', 'fa-tools'],
        'title': 'Riešenie'
    }
}


def to_html(elem, code):
    div = Div(classes=mapping[code]['classes'])

    # prepare content
    # icon
    icon = Span(classes=mapping[code]['icon-classes'], attributes={'aria-hidden': 'true'})

    # title
    title = [icon, Space]
    if len(elem.content[0].content[1:]) == 0:
        title.append(Str(mapping[code]['title']))
    else:
        title.append(Str(elem.content[0].content[1:]))
    header = Header(*title, level=4, classes=['alert-heading'])

    # title = pf.Strong()
    # title.content = elem.content[0].content[1:]

    # if len(title.content) == 0:
        # title.content.append(pf.Str(' ' + mapping[code]['title']))

    # para = pf.Para(icon, title)

    # div.content.extend(icon)
    div.content.append(header)
    div.content.extend(elem.content[1:])

    return div


def action(elem, doc):
    if isinstance(elem, BlockQuote):  # and doc.format == 'html':
        code = elem.content[0].content[0].text

        if code in ('[comment]', '[warning]', '[lecturer]', '[solution]'):
            if doc.format in ('html', 'html5'):
                return to_html(elem, code)


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
