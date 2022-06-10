import pathlib
import zipfile
from lxml import etree
from xml.etree.ElementTree import ElementTree

def get_path() -> pathlib.PurePath:
  data_path = pathlib.PurePath.joinpath(pathlib.Path.cwd(), 'data')
  return data_path

def extract_and_get_file(filename: str = '2k Undivided') -> ElementTree:
  dataPath = get_path()
  with zipfile.ZipFile(dataPath.joinpath(filename), 'r') as file:
    file.extractall(path=dataPath)

  return etree.parse(dataPath.joinpath(filename + '.ros'))

if __name__ == '__main__':
  # get filename from arguments

  fileTree = extract_and_get_file()
