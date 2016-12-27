#!/bin/bash

# Install specific version of Firefox known to work well with the selenium version above
wget https://ftp.mozilla.org/pub/firefox/releases/45.0.1/linux-x86_64/en-US/firefox-45.0.1.tar.bz2
tar jxf firefox*.tar.bz2
rm -rf firefox-bin
mv firefox firefox-bin
rm firefox*.tar.bz2
