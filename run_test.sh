#!/usr/bin/env bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PYTHONPATH="$PYTHONPATH:$SCRIPTPATH:$SCRIPTPATH/src" python -m coverage run -m unittest -v && coverage report