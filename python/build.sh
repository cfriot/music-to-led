#!/bin/bash
echo "cleaning old build files"
rm -Rf build; rm -Rf dist; find . | grep -E \"(__pycache__|.pyc|.pyo)\"| xargs rm -rf
echo "building new one"
pyinstaller --icon='resources/icon.icns' --onefile --windowed music2led.spec;
