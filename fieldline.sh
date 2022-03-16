:;# Activates virtual environment, starts buffer, and runs fieldline client

:<<BATCH
  :;@echo off
  :; # ########## WINDOWS SECTION #########################

  echo Windows not yet supported.
        
  :; # ########## WINDOWS SECTION ENDS ####################
  :; # ####################################################
  exit /b
BATCH

if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ] || [ "$(uname)" == "Darwin" ]; then
## Linux and Mac section
  # virtual environment
  . venv/bin/activate

  # ft buffer
  ./buffer/linux/buffer &> /dev/null &
  BUFFER_PID=$!
  echo Fieldtrip Buffer running with pid ${BUFFER_PID}

  # Fieldline
  python3 mne_fieldline.py

  # cleanup when we're done
  kill -9 ${BUFFER_PID}
fi
exit 0
