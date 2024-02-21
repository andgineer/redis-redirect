#!/usr/bin/env bash
#
# "Set-ups or/and activates development environment"
#

VENV_FOLDER="venv"
PYTHON="python3.11"  # sync with python-version: '3.11' in .github/workflows/static.yml

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

if ! (return 0 2>/dev/null) ; then
    # If return is used in the top-level scope of a non-sourced script,
    # an error message is emitted, and the exit code is set to 1
    echo
    echo -e $RED"This script should be sourced like"$NC
    echo "    . ./activate.sh"
    echo
    exit 1
fi

# virtual env
unset CONDA_PREFIX
if [[ ! -d ${VENV_FOLDER} ]] ; then
    echo -e $CYAN"Creating virtual environment for python in ${VENV_FOLDER}"$NC
    if uv venv ${VENV_FOLDER} --python=${PYTHON}; then
      START_TIME=$(date +%s)

      . ${VENV_FOLDER}/bin/activate
      uv pip install --upgrade pip
      uv pip install -r requirements.dev.txt
      uv pip install -e .

      END_TIME=$(date +%s)
      echo "Environment created in $((END_TIME - $START_TIME)) seconds"
    else
      echo -e $RED"Error to create virtual env. Do you have Astral's UV installed ( https://pypi.org/project/uv/ )?"$NC
      return 1
    fi
else
    echo -e $CYAN"Activating virtual environment ..."$NC
    . ${VENV_FOLDER}/bin/activate
fi
