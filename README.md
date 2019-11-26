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

