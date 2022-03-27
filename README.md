# verigram

Research project from generating spectral diagrams to visualize misinformations of Twitter.

### Installation:

Install requirements:

- jupyter notebook
- requests
- pandas
- numpy
- matplotlib
- networkx
- nxviz
- python-louvain
- py3plex
- kuramoto
- seaborn
- sklearn
- scipy
- numba
- july
- moment
- miditime

### OS Requirements

- Microsoft C++ 14.0 (For graph build tools on Windows)

### Usage

you can place the csv export files from hoaxy of the `raw_data` directory.

```sh
cd /raw_data
```

### Aggregate Data

You can then proceed to aggregate data by running `correlate-data.py`

```sh
# You need python 3.x to run this.
python3 correlate-data.py
```

### Running the Paper Implementation

You can run the research paper implementation using vscode and opening **Paper Impelementation.ipynb** or opening it in Jupyter notebook
