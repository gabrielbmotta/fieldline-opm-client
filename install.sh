:;# This script performs generates and copies the necesary library dependencies for running qt-projects both for
:;# dynamic and for staic builds.
:;#
:;# This file is part of the MNE-CPP project. For more information visit: https://mne-cpp.github.io/
:;#
:;# This script is based on an open-source cross-platform script template.
:;# For more information you can visit: https://github.com/juangpc/multiplatform_bash_cmd
:;#

:<<BATCH
    :;@echo off
    :; # ########## WINDOWS SECTION #########################

    echo Windows not yet supported.

    :; # ########## WINDOWS SECTION ENDS ####################
    :; # ####################################################
    exit /b
BATCH

if [ "$(expr substr $(uname -s) 1 5)" == "Linux"  || "$(uname)" == "Darwin" ]; then

    # ######################################################
    # ############## LINUX SECTION #########################

    PYTHON_VERSION="$(python3 --version)"
    if [[ ${PYTHON_VERSION} = "Python 3."* ]]
        then
        PYTHON_OK=true
        echo Python 3 version meets minimum requirements
        else
        PYTHON_OK=false
        echo Python 3 version does not meet minimum requirements
    fi

    if [[ "${PYTHON_OK}" = true ]]
        then
        # Setup environment
        python3.8 -m venv venv
        . venv/bin/activate
        pip install -r requirements-api.txt
        pip install fieldline_api-0.0.13-py3-none-any.whl
    fi

    # ############## LINUX SECTION ENDS ####################
    # ######################################################

fi

exit 0