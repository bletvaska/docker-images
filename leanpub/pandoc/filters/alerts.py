#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create alerts from blockquote, if the syntax of first line is

> [alert] alert title
"""

from panflute import Str, Space, Div, Header, Span, BlockQuote
import panflute as pf


mapping = {
    '[comment]': {
        'classes': ['alert', 'alert-primary', 'theme-alert-info'],
        'icon-classes': ['fas', 'fa-info-circle'],
        'title': 'Poznámka',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-info-circle-fill" viewBox="0 0 16 16">\
  <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>\
</svg>',
        'box-name': 'infobox',
        'box-color': 'cyan'
    },

    '[warning]': {
        'classes': ['alert', 'alert-danger', 'theme-alert-danger'],
        'icon-classes': ['fas', 'fa-exclamation-circle'],
        'title': 'Upozornenie',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle-fill" viewBox="0 0 16 16">\
  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>\
</svg>',
        'box-name': 'warningbox',
        'box-color': 'red'
    },

    '[lecturer]': {
        'classes': ['alert', 'alert-warning', 'theme-alert-lecturer'],
        'icon-classes': ['fas', 'fa-paperclip'],
        'title': 'Poznámky pre učiteľa',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-paperclip" viewBox="0 0 16 16">\
  <path d="M4.5 3a2.5 2.5 0 0 1 5 0v9a1.5 1.5 0 0 1-3 0V5a.5.5 0 0 1 1 0v7a.5.5 0 0 0 1 0V3a1.5 1.5 0 1 0-3 0v9a2.5 2.5 0 0 0 5 0V5a.5.5 0 0 1 1 0v7a3.5 3.5 0 1 1-7 0V3z"/>\
</svg>',
        'box-name': 'lecturerbox',
        'box-color': ''
    },

    '[solution]': {
        'classes': ['alert', 'alert-secondary', 'theme-alert-solution'],
        'icon-classes': ['fas', 'fa-tools'],
        'title': 'Riešenie',
        'icon': '',
        'box-name': 'solutionbox',
        'box-color': ''
    }
}

def to_html(elem, code):

    # prepare stuff
    title = mapping[code]['title']
    content = pf.convert_text(elem.content[1:], input_format='panflute', output_format='html')
    classes = ' '.join(mapping[code]['classes'])
    icon_classes = ' '.join(mapping[code]['icon-classes'])

    # populate template
    alert = f"""
    <div class="{classes}" role="alert">
        <p class="alert-heading">
             <span class="{icon_classes}"></span> {title}
        </p>
        <p>{content}</p>
    </div>
    """

    # render
    return pf.convert_text(alert, input_format='html')



def to_latex(elem, code):
    # prepare stuff
    title = mapping[code]['title']
    content = pf.convert_text(elem.content[1:], input_format='panflute', output_format='latex')
    box = mapping[code]['box-name']
    color = mapping[code]['box-color']


    # populate template
    return [
        pf.RawBlock(f'\\begin{{{box}}}', format='latex'),
        pf.RawBlock(f'\\noindent\\textcolor{{{color}!75!black}}{{\\textbf{{{title}}}}}', format='latex'),
        pf.RawBlock('\\smallskip'),
        pf.RawBlock(f'\\noindent {content}', format='latex'),
        pf.RawBlock(f'\\end{{{box}}}', format='latex'),
    ]

    # alert = f"""
    # \\begin{{infobox}}
    # \\textbf{{{title}:}} {content}
    # \\end{{infobox}}
    # """

    # # render
    # return pf.convert_text(alert, input_format='latex')


def to_epub(elem, code):
    # prepare stuff
    title = mapping[code]['title']
    content = pf.convert_text(elem.content[1:],
                              input_format='panflute',
                              output_format='html')
    classes = ' '.join(mapping[code]['classes'])
    # icon = mapping[code]['icon']

    # populate template
    alert = f"""
    <div class="{classes}" role="alert">
        <p class="alert-heading">{title}</p>
        <p>{content}</p>
    </div>
    """

    # render
    return pf.convert_text(alert, input_format='html')


def action(elem, doc):
    if isinstance(elem, BlockQuote):
        try:
            code = elem.content[0].content[0].text

            if code in ('[comment]', '[warning]', '[lecturer]', '[solution]'):
                if doc.format in ('html', 'html5'):
                    return to_html(elem, code)
                elif doc.format == 'epub':
                    return to_epub(elem, code)
                elif doc.format == 'latex':
                    return to_latex(elem, code)
        except :
            return elem



def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
