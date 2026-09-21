# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name          = "jekyll-theme-nucky"
  spec.version       = "2026.09"
  spec.authors       = ["Miroslav Biňas"]
  spec.email         = ["miroslav.binas@tuke.sk"]

  spec.summary       = "Theme for KPI courses."
  spec.homepage      = "http://www.kpi.fei.tuke.sk"
  spec.license       = "MIT"

  spec.files         =  `find * -type f -print0`.split("\x0").select { |f| f.match(%r!^(assets|_layouts|_includes|_sass|LICENSE|README)!i) }

  spec.add_runtime_dependency "jekyll", "~> 4.3"

  spec.add_development_dependency "bundler", ">= 2.3"
  spec.add_development_dependency "rake", "~> 13.0"
end
