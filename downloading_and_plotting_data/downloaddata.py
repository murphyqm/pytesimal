#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script download data files from BGS data archive."""
import requests

source_urls = [
    "http://webservices.bgs.ac.uk/accessions/download/"
    "138605?fileName=constant_properties.dat",
    "http://webservices.bgs.ac.uk/accessions/download/"
    "138605?fileName=variable_properties.dat",
]

for url in source_urls:
    filename = url.rsplit("=", 1)[1]
    print("Downloading", filename)
    r = requests.get(url, allow_redirects=True)
    fh = open(filename, "wb")
    fh.write(r.content)
    fh.close()
