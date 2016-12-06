#!/usr/bin/env bash

echo ":::"
if [[ ${EUID} -eq 0 ]]; then
    echo "::: You are root."
else
    echo "::: Script called with non-root privileges. geopyter_magic places"
    echo "::: files in /usr/local/share/jupyter/nbextensions/ and requires"
    echo "::: elevated rights. Please check the contents of the script for any"
    echo "::: concerns with this requirement."
    echo ":::"
    echo "::: Detecting the presence of the sudo utility to continue install..."

    if [ -x "$(command -v sudo)" ]; then
        echo "::: sudo utility located."
    else
        echo ":::"
        echo "::: Elevated privileges are required to install geopyter_magis."
        echo "::: Please run this script as root."
        exit 1
    fi
fi

TARGET_PIP="$(which pip)"
TARGET_JUPYTER="$(which jupyter)"
echo "::: Installing geopyter_magic..."
sudo -H $TARGET_PIP install . || true
echo "::: Installing geopyter into Jupyter NBExtensions..."
sudo $TARGET_JUPYTER nbextension install geopyter_magic/geopyter.js || true
echo "::: Enabling geopyter in Jupyter..."
sudo $TARGET_JUPYTER nbextension enable geopyter || true
echo "::: Registering geopyter_magic with Jupyter..."
sudo $TARGET_JUPYTER serverextension enable --py geopyter_magic || true
exit $?