ferguson-grand-jury-transcripts
===============================

We are converting the 5000 page Ferguson Grand Jury transcript PDF into [something more readable](http://ferguson.sayit.mysociety.org/). We're using the [SayIt](http://sayit.mysociety.org/) service by [MySociety](https://www.mysociety.org/). 

### Tasks
- [x] OCR the transcripts
- [x] Use `pdf2txt.py` to convert PDF to XML
- [x] Use `parse_transcript_xml.py` to convert XML to formatted txt
- [x] Use `converted_text_to_akoma_ntoso.py` script to convert the new formatted text to [Akoma Ntoso](http://sayit.mysociety.org/about/developers#an)
- [x] Upload to SayIt
- [ ] Promote to media and activists

### Conversion
The Ferguson Grand Just testimony PDF is 5000 pages long. It was transcribed over 100 days by different people, so the formatting is all over the place. There is also a lot of redacted content. We've done the best we can to get these transcripts up and live. Done is better than perfect. Compare anything that looks weird to the official released PDF.

### Raw Transcripts
http://graphics8.nytimes.com/newsgraphics/2014/11/24/ferguson-assets/grand-jury-testimony.pdf

### OCR Transcripts
https://www.dropbox.com/s/67unqhdrb8jhgr0/Ferguson%20Grand%20Jury%20Testimony.pdf?dl=0

### Document Cloud
St. Louis Public Radio has [run all the eveidence](http://apps.stlpublicradio.org/ferguson-project/evidence.html) through a service called [Document Cloud](http://www.documentcloud.org/documents/1370490-grand-jury-volume-1.html) which does all kinds of useful stuff. They have [an API](http://www.documentcloud.org/api/documents/1370490-grand-jury-volume-1.json) links for all the [converted text](https://s3.amazonaws.com/s3.documentcloud.org/documents/1370490/grand-jury-volume-1.txt) or text [broken out by page](http://www.documentcloud.org/documents/1370490/pages/grand-jury-volume-1-p1.txt).

### Final Transcripts
http://ferguson.sayit.mysociety.org/

### Twitter Discussion
https://twitter.com/steiny/status/537297171255943168
