#!/usr/bin/env ruby
# Renders a Liquid template with variables passed as JSON on stdin:
#   {"template": "...", "vars": {...}}
# Prints the rendered result to stdout. Used by tasks.py so the epub/pdf
# preprocessing can use Liquid (already a jekyll dependency) instead of
# Jinja2, without adding a second Python templating dependency.

require 'liquid'
require 'json'

input = JSON.parse($stdin.read)
template = Liquid::Template.parse(input['template'])
print template.render(input['vars'])
