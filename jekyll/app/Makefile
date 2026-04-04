JEKYLL := bundle exec jekyll

GREEN  := \033[0;32m
YELLOW := \033[0;33m
RESET  := \033[0m

.PHONY: all help new install update build serve clean shell

all: install serve  ## Install dependencies and serve the site

help:  ## Show this help
	@printf "Usage: make $(YELLOW)<target>$(RESET)\n\n"
	@printf "Targets:\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-10s$(RESET) %s\n", $$1, $$2}'

new:  ## Create a new Jekyll project in the current directory
	@[ ! -f _config.yml ] || { printf "$(YELLOW)Project already exists in this directory.$(RESET)\n"; exit 1; }
	[ -f Gemfile ] || cp /app/Gemfile Gemfile
	bundle install
	$(JEKYLL) new . --force --skip-bundle

install:  ## Install gem dependencies
	[ -f Gemfile ] || cp /app/Gemfile Gemfile
	bundle install

update:  ## Update gem dependencies
	bundle update

build:  ## Build the static site
	$(JEKYLL) build --incremental

serve:  ## Serve the site locally at http://localhost:5000
	$(JEKYLL) serve --host 0.0.0.0 --port 5000 --watch --incremental

clean:  ## Remove generated files, installed gems and lock file
	rm -rf _site/ .jekyll-cache/ vendor/ Gemfile.lock

shell:  ## Open an interactive shell
	sh
