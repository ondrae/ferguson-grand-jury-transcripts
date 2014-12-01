from xml.etree import ElementTree as xml
import re, helpers, copy

class Volume():
  ''' each volume gets its own Akoma Ntoso file '''
  
  def __init__(self):
    ''' get the full text for that volume '''
    self.akoma_ntoso = xml.Element("akomaNtoso")
    self.debate = xml.SubElement(self.akoma_ntoso, "debate")
    self.meta = xml.SubElement(self.debate, "meta")
    self.references = xml.SubElement(self.meta, "references")
    self.debateBody = xml.SubElement(self.debate, "debateBody")
    self.full_text = []

  def debateSection(self, heading):
    ''' properly label the section '''
    self.debateSection = xml.SubElement(self.debateBody, "debateSection")
    self.heading = xml.SubElement(self.debateSection, "heading")
    self.heading.text = heading

  def remove_cover_pages(self):
    ''' id and remove cover pages '''
    # Every coverpage ends with this phone number
    for i, line in enumerate(self.full_text):
      if "(314) 615-2600" in line["text"]:
        end_of_cover = i
        break
    # Include the line with the number and the newline after it
    end_of_cover = end_of_cover + 2
    new_text_wo_cover_page = []
    # once we've counted down to it, start copying lines
    for line in self.full_text:
      if not end_of_cover:
        new_text_wo_cover_page.append(line)
      else:
        end_of_cover = end_of_cover - 1
    self.full_text = new_text_wo_cover_page

  def get_speakers(self):
    ''' Find all the speakers '''
    print "Getting speakers"
    for line in self.full_text:
     
      # Look for peoples names
      already_found = False
      name = re.search("(M[RS]\.* [A-Z]+):", line["text"])
      qna = re.search("([QA]) ", line["text"])
      if name:
        showAs = name.group(1)
      if qna:
        showAs = qna.group(1)

      # Check that the person isn't in yet.
      if name or qna:
        for child in self.references:
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
        self.TLCPerson = xml.SubElement(self.references, "TLCPerson", attr)

  def get_speeches(self):
    ''' Find all the sections and speeches '''
    print "Getting speeches"

    # Look for a speakers name. Start recording the rest of that line
    # record all other lines until another name is found.
    speeches = []
    speech = {
      "speech" : []
    }
    for line in self.full_text:

        # clean up
        line["text"] = line["text"].replace("(at new indentation)", "")
        line["text"] = line["text"].strip()

        # Look for speakers names
        name = re.search("(M[RS]\.* [A-Z]+):(.*)", line["text"])

        # Look for Q&A
        qna = re.match("([AQ]) (.*)", line["text"])

        if name:
          speech = {
            "speaker" : name.group(1),
            "speech" : [{
              "text" : name.group(2),
              "pos" : line["pos"]
            }]
          }
          speeches.append(speech)

        elif qna:
          speech = {
            "speaker" : qna.group(1),
            "speech" : [{
              "text" : qna.group(2),
              "pos" : line["pos"]
            }]
          }
          speeches.append(speech)

        else:
          # Add line to current speech
          speech['speech'].append(line)

    self.speeches = speeches


  def fix_indented_qna_speeches(self):
    ''' some q speeches are found by a large indent
        use the pos to find these
    '''
    for i, speech in enumerate(self.speeches):
      where_to_insert = False
      if speech["speaker"] == "A":
        for paragraph in speech["speech"]:
          if where_to_insert:
              self.speeches[where_to_insert]["speech"].append(paragraph)
          if paragraph["pos"]:
            # 300 is for big indents
            if int(paragraph["pos"][0:3]) > 300:
              where_to_insert = i + 1 # Insert after this
              new_speech = {
                "speaker" : "Q",
                "speech" : [ paragraph ]
              }
              self.speeches.insert(where_to_insert, new_speech)
            
      if where_to_insert:
        # remove the fixed line from the answer
        speech_copy = copy.copy(self.speeches[i]["speech"])
        for paragraph in self.speeches[i]["speech"]:
          if paragraph in self.speeches[i+1]["speech"]:
            speech_copy.remove(paragraph)
        self.speeches[i]["speech"] = speech_copy

  def remove_pos(self):
    ''' only needed pos for the qna formatting'''
    for speech in self.speeches:
      text = []
      for paragraph in speech["speech"]:
        text.append(paragraph["text"])
      speech["speech"] = text

  def build_speeches(self):
    ''' build speech xml elements '''
    for speech in self.speeches:
      attr = {
        "by" : "#" + speech["speaker"].lower().replace(" ","-").replace(".","")
      }
      self.speech = xml.SubElement(self.debateSection, "speech", attr)
      self.add_paragraphs(self.speech, speech)

  def add_paragraphs(self, elem, speech):
    ''' build paragraphs '''
    speech["speech"] = " ".join(speech["speech"])
    speech["speech"] = speech["speech"].split("--++ new paragraph!")
    for paragraph in speech["speech"]:
        paragraph = re.sub("\n","",paragraph) # get rid of leading newlines
        paragraph = paragraph.strip()
        if paragraph:
          p = xml.SubElement(elem, "p")
          p.text = paragraph

  def indent(self):
    helpers.indent(self.akoma_ntoso)
