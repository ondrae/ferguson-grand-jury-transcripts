from xml.etree import ElementTree as xml
import re
# Open up the txt file


with open('files/sample.txt') as text:
  with open('files/sample.an', 'w') as out:

    # start building the Akoma Ntoso file
    akomaNtoso = xml.Element("akomaNtoso")
    debate = xml.SubElement(akomaNtoso, "debate")
    meta = xml.SubElement(debate, "meta")
    references = xml.SubElement(meta, "references")
    debateBody = xml.SubElement(debate, "debateBody")

    def get_speakers():
      ''' Find all the speakers '''
      for line in text:
        # Look for peoples names
        already_found = False
        r = re.search("(M[RS]\. [A-Z]+):", line)
        if r:
          showAs = r.group(1)

          # Check that the person isn't in yet.
          for child in references:
            if showAs == child.attrib["showAs"]:
              already_found = True
              break
          if already_found:
            continue

          id = showAs.lower().replace(". ","-")
          attr = {
            "href" : "/ontology/person/ferguson.sayit.mysociety.org/" + id,
            "showAs" : showAs
          }
          TLCPerson = xml.SubElement(references, "TLCPerson", attr)

    def get_speeches():
      ''' Pull all the speeches out '''
      text.seek(0)
      r = re.findall("M[RS]\. [A-Z]+: (.*?)", text.read(), re.S)
      print r

    def indent(elem, level=0):
      ''' pretty printing for xml '''
      i = "\n" + level*"  "
      if len(elem):
          if not elem.text or not elem.text.strip():
              elem.text = i + "  "
          if not elem.tail or not elem.tail.strip():
              elem.tail = i
          for elem in elem:
              indent(elem, level+1)
          if not elem.tail or not elem.tail.strip():
              elem.tail = i
      else:
          if level and (not elem.tail or not elem.tail.strip()):
              elem.tail = i

    get_speakers()
    get_speeches()

    indent(akomaNtoso)
    out.write(xml.tostring(akomaNtoso))

