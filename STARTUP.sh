#!/bin/bash
training="$1"

$if [ "$training" ]; then {
    python ./src/code/training.py
}
fi

streamlit run ./src/page.py
