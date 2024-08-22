# this requires EDirect, so please install that.
# EDirect is a Pubmed CLI tool.

import sys, shutil, os, ast
from pathlib import Path
import pandas as pd

from config import config as project_config
import glob

sys.path.insert(1, os.path.dirname(shutil.which('xtract')))  # this finds the path to edirects xtract executable
import edirect as e


def get_pubmeddata(mindate=int(project_config.year_start), maxdate=int(project_config.year_end)):
    mindate = int(project_config.year_start)
    maxdate = int(project_config.year_end)
    Path(f'data/obsgyn/pmids').mkdir(parents=True, exist_ok=True)

    query_files = glob.glob(f'queries/obsgyn/pmids/*.json')
    queries = pd.DataFrame({
        'long': pd.Series(dtype='str'),
        'short': pd.Series(dtype='str'),
        'type': pd.Series(dtype='str'),
        'query': pd.Series(dtype='str'),
    })
    for queryfile in query_files:
        with open(queryfile, 'r') as f:
            my_dict = ast.literal_eval(f.read())
        queries = pd.concat([queries, pd.DataFrame.from_dict(my_dict)], ignore_index=True)
    queries['query'] = queries['query'].str.replace('"|“|”', '\\"')  # fix the quotes
    queries.drop_duplicates(subset='short', inplace=True)

    for index, row in queries.iterrows():
        for my_year in range(mindate, maxdate + 1):
            pipeline = (
                f'esearch -db pubmed -query "({row['query']}) AND ({my_year}[PDAT])"',
                f'efetch -format uid'
            )
            results = e.pipeline(pipeline)

            with open(Path(f'data/obsgyn/pmids/{row["short"]}_{my_year}.txt'), 'w') as f:
                f.write(results)


def clean_pubmeddata():
    """ This is obviously a stub """
    print('Cleaning PubMed data')
