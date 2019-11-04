#!/bin/bash

cd python-app
python -m inputs.midiInput --list
python -m inputs.audioInput --list
python -m outputs.serialOutput --list
