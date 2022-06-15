import pathlib
import zipfile
from lxml import etree
from xml.etree.ElementTree import ElementTree

def get_path() -> pathlib.PurePath:
  data_path = pathlib.PurePath.joinpath(pathlib.Path.cwd(), 'data')
  return data_path

def extract_and_get_file(filename: str = '2k_Undivided.rosz') -> ElementTree:
  filename = '2k_Undivided'
  # filename = 'Test_Custodes'
  ext = '.rosz'

  dataPath = get_path()
  with zipfile.ZipFile(dataPath.joinpath(filename + ext), 'r') as file:
    file.extractall(path=dataPath)

  return etree.parse(dataPath.joinpath(filename + '.ros'))

if __name__ == '__main__':
  # get filename from arguments

  fileTree = extract_and_get_file()
  root = fileTree.getroot()

  keywords: list[str] = []
  for item in root:

    if item.tag == '{http://www.battlescribe.net/schema/rosterSchema}forces':
      for force in item:
        for selections in force:

          if selections.tag == '{http://www.battlescribe.net/schema/rosterSchema}selections':
            for selection in selections:

              if selection.get('type') == 'model' or selection.get('type') == 'unit':
                for categories in selection:

                  if categories.tag == '{http://www.battlescribe.net/schema/rosterSchema}categories':
                    for category in categories:
                      keywords.append(category.get('name'))

  keywordSet = list(set(keywords))
  print(*keywordSet, sep='\n')
