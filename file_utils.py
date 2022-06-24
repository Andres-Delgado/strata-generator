from lxml import etree
from xml.etree import ElementTree
import pathlib
import requests
import zipfile

class FileUtils:
  @classmethod
  def get_data_path(cls) -> pathlib.Path:
    path = pathlib.Path.joinpath(pathlib.Path.cwd(), 'data')

    if not path.is_dir():
      path.mkdir(parents=True, exist_ok=True)

    return path

  @classmethod
  def extract_roster(cls, filename: str) -> ElementTree:
    ext = '.rosz'
    dataPath = cls.get_data_path()

    with zipfile.ZipFile(dataPath.joinpath(filename + ext), 'r') as file:
      file.extractall(path=dataPath)

    return etree.parse(dataPath.joinpath(filename + '.ros'))

  @staticmethod
  def download_save(url: str, filename: str):
    headers = {
      'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, ' +
        'like Gecko) Chrome/102.0.5005.125 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    with open(FileUtils.get_data_path().joinpath(filename), 'wb') as outfile:
      outfile.write(response.content)

  ############
  ############
  ############

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

    # from roster, get name for models/units/factions
    # find factionIDs from factions.csv with faction names
    # find datasheetIDs from datasheets.csv with model/unit names
    # find keywords from datasheets_keywords.csv with datasheetIDs

    cls.sync_stratagems_csv()
    cls.sync_factions_csv()
    cls.sync_datasheets_csv()
    cls.sync_datasheets_stratagems_csv()
