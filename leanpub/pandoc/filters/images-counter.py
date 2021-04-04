#!/usr/bin/env python3

import panflute as pf


counter = 1

# def eprint(*args, **kwargs):
#     with open('/tmp/out', 'a') as f:
#         print(*args, file=f, **kwargs)


def action(elem, doc):
    if isinstance(elem, pf.Image) and doc.format == 'html':
        global counter

        strong = pf.Strong(pf.Str(f'Obr. {counter}: '))
        elem.content.insert(0, strong)
        counter += 1

        elem.classes.append('img-responsive')


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
