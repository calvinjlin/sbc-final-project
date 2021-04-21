# -*- coding: utf-8 -*-
import logging
from pathlib import Path
# from dotenv import find_dotenv, load_dotenv
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
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    download_covid_case(output_filepath=output_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main(output_filepath=f'{project_dir}/data/raw')
