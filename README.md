# strata-generator
A simple tool for Warhammer: 40k to generate relevant strategems from a battlescribe roster list

## run
```sh ./run.sh```

## Notes
make sure to not edit roster filename

## TODO
- extract model/unit/faction IDs from roster
  - model/unit ID: datasheets.csv
  - keywords: datasheets_keywords.csv
  - factions: factions.csv

- find linking IDs in csv files
- make utility to download/save all relevant files
- parse through files using linking IDs

## Z Practice
make everything modular
- implement menu for different actions
  - resync all files
  - get strategems for "filename"
  - sync & get stratagems
