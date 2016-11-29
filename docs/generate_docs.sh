#!/usr/bin/env bash
make latexpdf
mv _build/latex/G4SETechnicalDocumentation.pdf .
rm -rf _build/
