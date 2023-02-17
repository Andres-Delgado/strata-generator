import pandas
import re

from file_utils import FileUtils

class Exporter:
  @classmethod
  def to_txt(cls, data: pandas.DataFrame):
    dataPath = FileUtils.get_data_path()

    f = open(dataPath.joinpath('roster.txt'), 'w')
    for _, strategem in data.iterrows():
      f.write('{name} - {cp_cost}CP\n'.format(name = strategem['name'], cp_cost=strategem['cp_cost']))
      f.write(strategem['type'] + '\n')
      f.write(cls.remove_tags(strategem['description']) + '\n')
      f.write(strategem['legend'] + '\n\n')

    f.close()

  @classmethod
  def remove_tags(cls, dirtyStr: str) -> str:
    return re.sub('<[^>]+>', '', dirtyStr)

  # TODO: replace &lt; &gt;