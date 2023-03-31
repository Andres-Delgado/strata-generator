from lxml import etree
from xml.etree import ElementTree
from typing import List
import pathlib
import requests
import zipfile
import pandas

class FileUtils:
  @classmethod
  def get_data_path(cls) -> pathlib.Path:
    path = pathlib.Path.joinpath(pathlib.Path.cwd(), 'data')
    if not path.is_dir():
      path.mkdir(parents=True, exist_ok=True)
    return path

  @classmethod
  def get_csv_path(cls) -> pathlib.Path:
    path = pathlib.Path.joinpath(cls.get_data_path(), 'csv')
    if not path.is_dir():
      path.mkdir(parents=True, exist_ok=True)
    return path

  @classmethod
  def get_rosters_path(cls) -> pathlib.Path:
    path = pathlib.Path.joinpath(cls.get_data_path(), 'rosters')
    if not path.is_dir():
      path.mkdir(parents=True, exist_ok=True)
    return path

  @classmethod
  def extract_roster(cls, filename: str) -> ElementTree:
    rostersPath = cls.get_rosters_path()
    filenameZipped = ''

    with zipfile.ZipFile(rostersPath.joinpath(filename), 'r') as file:
      filenameZipped = file.namelist()[0]
      file.extract(member=filenameZipped, path=rostersPath)

    return etree.parse(rostersPath.joinpath(filenameZipped))

  @classmethod
  def list_roster_files(cls) -> List[str]:
    dataPath = cls.get_data_path()
    return [path.stem for path in dataPath.iterdir() if path.is_file() and path.suffix == '.json']

  @staticmethod
  def download_save(url: str, filename: str):
    headers = {
      'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, ' +
        'like Gecko) Chrome/102.0.5005.125 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    with open(FileUtils.get_csv_path().joinpath(filename), 'wb') as outfile:
      outfile.write(response.content)

  ################
  # sync methods #
  ################

  @classmethod
  def sync_stratagems_csv(cls):
    url = 'https://wahapedia.ru/wh40k9ed/Stratagems.csv'
    cls.download_save(url, 'stratagems.csv')

  @classmethod
  def sync_factions_csv(cls):
    url = 'https://wahapedia.ru/wh40k9ed/Factions.csv'
    cls.download_save(url, 'factions.csv')

  @classmethod
  def sync_datasheets_csv(cls):
    url = 'https://wahapedia.ru/wh40k9ed/Datasheets.csv'
    cls.download_save(url, 'datasheets.csv')

  @classmethod
  def sync_datasheets_stratagems_csv(cls):
    url = 'http://wahapedia.ru/wh40k9ed/Datasheets_stratagems.csv'
    cls.download_save(url, 'datasheets_stratagems.csv')

  @classmethod
  def sync_csv_files(cls):
    # allCsvUrl = 'https://wahapedia.ru/wh40k9ed/Export%20Data%20Specs.xlsx'
    # keyswordsUrl = 'http://wahapedia.ru/wh40k9ed/Datasheets_keywords.csv'

    cls.sync_stratagems_csv()
    cls.sync_factions_csv()
    cls.sync_datasheets_csv()
    cls.sync_datasheets_stratagems_csv()

  ###################
  # load csv methods #
  ###################

  @classmethod
  def load_csv_to_dataframe(cls, filename: str) -> pandas.DataFrame:
    filePath = cls.get_csv_path().joinpath(filename)
    dataFrame: pandas.DataFrame = pandas.read_csv(filePath, delimiter='|', encoding='utf8')
    return dataFrame
