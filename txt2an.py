from xml.etree import ElementTree as xml
import re, helpers, StringIO

with open('files/VOLUME III.txt') as text:
  with open('files/VOLUME III.an', 'w') as out:

    # start building the Akoma Ntoso file
    akomaNtoso = xml.Element("akomaNtoso")
    debate = xml.SubElement(akomaNtoso, "debate")
    meta = xml.SubElement(debate, "meta")
    references = xml.SubElement(meta, "references")
    debateBody = xml.SubElement(debate, "debateBody")

    def get_speakers():
      ''' Find all the speakers '''
      print "Getting speakers"

      for line in text:
        # Look for peoples names
        already_found = False
        name = re.search("([A-Z]{2,}\.* [A-Z]{4,})", line)
        qna = re.search("([QA]) ", line)
        if name:
          showAs = name.group(1)
        if qna:
          showAs = qna.group(1)

        if name or qna:

          # Check that the person isn't in yet.
          for child in references:
            if showAs == child.attrib["showAs"]:
              already_found = True
              break
          if already_found:
            continue

          id = showAs.lower().replace(".","").replace(" ","-")
          attr = {
            "href" : "/ontology/person/ferguson.sayit.mysociety.org/" + id,
            "id" : id,
            "showAs" : showAs
          }
          TLCPerson = xml.SubElement(references, "TLCPerson", attr)


    def get_speeches():
      ''' Find all the sections and speeches '''
      print "Getting speeches"
      text.seek(0)

      # Look for a speakers name. Start recording the rest of that line
      # record all other lines until another name is found.
      speeches = []
      speech = {
        "speech" : []
      }

      for line in text:

        # Look for VOLUME to create sections
        volume = re.search("(VOLUME [A-Z]+)", line)
        # Look for speakers names
        name = re.search("([A-Z]{2,}\.* [A-Z]{4,}):(.*)", line)
        # Look for narrative
        narrative = re.search("\((.*)\)", line)
        # Look for Q&A
        qna = re.match("([AQ]) (.*)", line)

        if volume:
          section = xml.SubElement(debateBody, "debateSection")
          heading = xml.SubElement(section, "heading")
          heading.text = volume.group(1)

        elif name:
          speech = {
            "speaker" : name.group(1),
            "speech" : [name.group(2)]
          }
          speeches.append(speech)

        elif narrative:
          speech = {
            "speaker" : "narrative",
            "speech" : [narrative.group(1)]
          }
          speeches.append(speech)

        elif qna:
          speech = {
            "speaker" : qna.group(1),
            "speech" : [qna.group(2)]
          }
          speeches.append(speech)

        else:
          # Add line to current speech
          speech['speech'].append(line)

      # Loop through speeches and build xml
      for speech in speeches:

        # clean up speech
        speech["speech"] = " ".join(speech["speech"])
        speech["speech"] = speech["speech"].replace("\n", "\\n")

        # <narrative>
        if speech["speaker"] == "narrative":
          narrative = xml.SubElement(section, "narrative")
          narrative.text = speech["speech"]

        # <speech by="#mr-mcculloch">
        else:
          attr = {
            "by" : "#" + speech["speaker"].lower().replace(" ","-").replace(".","")
          }
          speech_elem = xml.SubElement(section, "speech", attr)
          p = xml.SubElement(speech_elem, "p")
          p.text = speech["speech"]

    def get_questioner():
      questioner = False
      text.seek(0)
      for line in text:
        match = re.search("BY (M[RS]+\.* [A-Z]+):", line)
        if match:
          questioner = "#" + match.group(1).lower().replace(" ","-").replace(".","")
      return questioner

    get_speakers()
    get_speeches()
    
    # Clean up Akoma Ntoso
    helpers.indent(akomaNtoso)
    xml_string = xml.tostring(akomaNtoso)
    xml_io = StringIO.StringIO(xml_string)
    
    # Confused why I need to 
    questioner = get_questioner()
    for line in xml_io:
      if questioner:
        line = line.replace("#q", questioner)
        line = line.replace("\\n","")

        out.write(line)
      
