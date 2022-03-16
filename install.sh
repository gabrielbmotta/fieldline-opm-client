:;# Creates a python virtual environemnt and installs dependecies.

:<<BATCH
  :;@echo off
  :; # ########## WINDOWS SECTION #########################

  echo Windows not yet supported.

  :; # ########## WINDOWS SECTION ENDS ####################
  :; # ####################################################
  exit /b
BATCH

if [[ "$(expr substr `uname -s` 1 5)" == "Linux" || "$(uname)" == "Darwin" ]]; then
## Linux and Mac section
  python3 -m venv venv
  . venv/bin/activate
  pip install fieldline_api-0.3.0-py3-none-any.whl
fi
exit 0