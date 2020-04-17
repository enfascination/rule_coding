### `compare.py`:
#### Installation
Package needed: `numpy`, `pandas`, `xlrd`
#### Usage
input file: `rules_data_codifying.xlsx`
output file: `compare.csv`

### `break_compounds.py`:
#### Installation
Package needed: `nltk`, `openpyxl`
also, must run: 
```python
nltk.download('punkt')
```

#### Usage
```shell
python break_compounds.py <codifying>.xlsx <codifying>_decompounded.xlsx
```

## Updates
  11/25 update -- statistical summary: summary.py  output: summary.csv 
added positon agreement measure to compare.py

# TODO
*  Caitlyn found that certain cbullet characters or tab charactrs were creeping through and throwing off the excel formatting.
*  When rule headers in reddit are added, they are missing community, oine id, and other info
*  move domain column over, closer to codes
