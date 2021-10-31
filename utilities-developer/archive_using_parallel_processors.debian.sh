#!/bin/bash
sudo apt-get install pigz pbzip2
cd /bin && mv gzip{,.000} && mv bzip2{,.000} && ln -s `which pigz` gzip && ln -s `which pbzip2` bzip2
# <OldCoder> they will not be faster for decompress of old tarballs
# <OldCoder> only for compress of new ones and decompress of new ones
