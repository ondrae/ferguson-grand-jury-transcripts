import re
from xml.etree import ElementTree as xml
from volume import Volume

def get_line_details(line):
  ''' get line details '''
  match = re.match("\((\d+\.\d+,\d+\.\d+)\) (.*)", line)
  if match:
    line_details = {
      "pos" : match.group(1),
      "text" : match.group(2)
    }
  else:
    line_details = { "pos" : "" , "text" : line}
  return line_details

def split_on_volume():
  ''' split text into volume objects '''
  with open('files/pdfminer/output/ferguson_grand_jury_testimony.txt') as file:
    volumes = []
    recording = False

    text = file.readlines()
    for line in text:
      line_details = get_line_details(line)

      # split on volumes, where VOLUME [IVX]+ is the only text
      match = re.match("(VOLUME [IVX]+)", line_details["text"])
      if match:
        volume = Volume()
        volume.debateSection(match.group(1))
        volumes.append(volume)
        recording = True

      # get the rest of the text too
      if recording:
        volume.full_text.append(line_details)

  return volumes

if __name__ == "__main__":
  volumes = split_on_volume()
  
  for volume in volumes:
    volume.remove_cover_pages()
    volume.get_speakers()
    volume.get_speeches()
    volume.fix_indented_qna_speeches()
    volume.remove_pos()
    volume.build_speeches()
    volume.indent()

  # Tests
  for volume in volumes:
    match = re.match("(VOLUME [IVX]+)", volume.heading.text)
    assert match

  # printout files
  for volume in volumes:
    with open("files/akoma_ntoso/"+volume.heading.text+".xml", "w") as out:
      xml_string = xml.tostring(volume.akoma_ntoso)
      out.writelines(xml_string)
