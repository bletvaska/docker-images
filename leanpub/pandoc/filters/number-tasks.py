#!/usr/bin/env python3

import panflute as pf

step = 0
task = 0


def action(elem, doc):
    global task
    global step

    # FIXME treba vyriesit cislovanie pre epub - header 1 nuluje step
    if isinstance(elem, pf.Header) and doc.format in ('html', 'epub'):

        if 'step' in elem.classes:
            step += 1
            task = 1
        elif 'task' in elem.classes:
            elem.content.append(pf.Space)
            elem.content.append(pf.Str(f'{step}.{task}'))
            task += 1


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == '__main__':
    main()
