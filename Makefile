#!make

VERSION := $(shell cat src/redis_redirect/version.py | cut -d= -f2 | sed 's/\"//g; s/ //')
export VERSION
unexport CONDA_PREFIX  # if conda is installed, it will mess with the virtual env

version:
	echo ${VERSION}

ver-bug:
	bash ./scripts/verup.sh bug

ver-feature:
	bash ./scripts/verup.sh feature

ver-release:
	bash ./scripts/verup.sh release

reqs:
	pre-commit autoupdate
	bash ./scripts/compile_requirements.sh
	pip install -r requirements.dev.txt
