from xml.etree import ElementTree as xml
import re, helpers

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
    self.full_text_details = []

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
      name = re.search("(M[RS]\.* [A-Z]+)", line["text"])
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

    def get_list_of_speeches():
      ''' build the first list of speeches '''
      
      # Look for a speakers name. Start recording the rest of that line
      # record all other lines until another name is found.
      speeches = []
      speech = {
        "speech" : []
      }

      for line in self.full_text:

        # clean up
        line["text"] = line["text"].replace("(at new indentation)", "")

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

        # elif narrative:
        #   speech = {
        #     "speaker" : "narrative",
        #     "speech" : [ {
        #       "text" : narrative.group(1), 
        #       "pos" : line["pos"]
        #     }]
        #   }
        #   print speech
        #   speeches.append(speech)

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

      return speeches

    def add_indented_q_speeches(speeches):
      ''' some q speeches are found by a large indent
          use the pos to find these and insert them
          return a list of speeches with no pos
      '''
      # different formats for different Q&A sections
      rebuilt_speeches = []
      for speech in speeches:
        if speech["speaker"] == "A":
          for paragraph in speech["speech"]:
            if paragraph["pos"]:
              # 300 is for big indents
              if int(paragraph["pos"][0:3]) > 300:
                new_speech = {
                  "speaker" : "Q",
                  "speech" : [ paragraph["text"] ]
                }
                rebuilt_speeches.append(new_speech)
              else:
                new_speech = {
                  "speaker" : speech["speaker"],
                  "speech" : [ ]
                }
                for paragraph in speech["speech"]:
                  new_speech["speech"].append(paragraph["text"])
                rebuilt_speeches.append(new_speech)
        else:
          new_speech = {
            "speaker" : speech["speaker"],
            "speech" : [ ]
          }
          for paragraph in speech["speech"]:
            new_speech["speech"].append(paragraph["text"])
          rebuilt_speeches.append(new_speech)

      return rebuilt_speeches


    def build_speeches(speeches):
      ''' build speech xml elements '''
      for speech in speeches:
        attr = {
          "by" : "#" + speech["speaker"].lower().replace(" ","-").replace(".","")
        }
        self.speech = xml.SubElement(self.debateSection, "speech", attr)
        self.add_paragraphs(self.speech, speech)

    speeches = get_list_of_speeches()
    speeches = add_indented_q_speeches(speeches)
    speeches = helpers.remove_dupes(speeches)
    build_speeches(speeches)


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
