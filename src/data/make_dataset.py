# -*- coding: utf-8 -*-
from pathlib import Path
import json
import requests


def download_covid_case(output_filepath=None):
    url = 'https://opendata.arcgis.com/datasets/b9f0d3856802413dacd4e0c4523e7a5f_0.geojson'
    raw_covid_case = requests.get(url).json()
    with open(f"{output_filepath}/case_count.json", 'w') as file:
        file.write(json.dumps(raw_covid_case))


def main(output_filepath=None):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """

    download_covid_case(output_filepath=output_filepath)


if __name__ == '__main__':
    # project directory path
    project_dir = Path(__file__).resolve().parents[2]

    main(output_filepath=f'{project_dir}/data/raw')
