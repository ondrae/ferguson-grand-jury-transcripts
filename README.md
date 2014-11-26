ferguson-grand-jury-transcripts
===============================

Converting the Ferguson Grand Jury transcripts into something more readable. We want to display them on the [SayIt](http://sayit.mysociety.org/) service by [MySociety](https://www.mysociety.org/). Court transcripts [look very nice](http://leveson.sayit.mysociety.org/hearing-14-may-2012/lord-augustine-odonnell) on  SayIt.

### Tasks
- [x] Download the OCR transcripts
- [x] Convert the PDF to a clean text file
- [ ] Write script to convert the text to [Akoma Ntoso](http://sayit.mysociety.org/about/developers#an)
- [ ] Upload to SayIt
- [ ] Promote to media and activists

### Raw Transcripts
http://graphics8.nytimes.com/newsgraphics/2014/11/24/ferguson-assets/grand-jury-testimony.pdf

### OCR Transcripts
https://www.dropbox.com/s/67unqhdrb8jhgr0/Ferguson%20Grand%20Jury%20Testimony.pdf?dl=0

### Document Cloud
St. Louis Public Radio has [run all the eveidence](http://apps.stlpublicradio.org/ferguson-project/evidence.html) through a service called [Document Cloud](http://www.documentcloud.org/documents/1370490-grand-jury-volume-1.html) which does all kinds of useful stuff. They have [an API](http://www.documentcloud.org/api/documents/1370490-grand-jury-volume-1.json) links for all the [converted text](https://s3.amazonaws.com/s3.documentcloud.org/documents/1370490/grand-jury-volume-1.txt) or text [broken out by page](http://www.documentcloud.org/documents/1370490/pages/grand-jury-volume-1-p1.txt).

### Converted to text
https://docs.google.com/uc?id=0ByV6qGuufDXDZGdtVl90aU1YV0E&export=download

The original PDF has three slightly different formats and we produced a different text file for each format. There's also one single file that has the entire contents of the document.

Two sets of files are included; one with page numbers (extracted from the document) and one without. The page numbers might be useful for parsing or if we need to refer back to the original document, and they're easy to skip if not.

The page numbers for the last set of pages (4654-4799) are in a different format than the others; they're all at the bottom of the page instead of the top, and prefixed with 'GorePerry Reporting & Video...'

The text was extracted from the OCR Transcripts using [Cogniview PDF2XL](https://www.cogniview.com/pdf-to-excel).

### Sample Files
10 sample pages of the PDF are at `files/sample.pdf`
The same 10 pages of converted text are at `files/sample.txt`

### Final Transcripts - Work in progress
http://ferguson.sayit.mysociety.org/

### Twitter Discussion
https://twitter.com/steiny/status/537297171255943168

### Initial attempts
I started with pdfminer, but it attempts to maintain the layout of the PDF. We don't want that. Doing much better with [Slate](https://pypi.python.org/pypi/slate). It apparently depends on an old version of pdfminer though, so I had to install it like `sudo pip install --upgrade --ignore-installed slate==0.3 pdfminer==20110515` which I found [here](https://github.com/timClicks/slate/issues/5#issuecomment-53450633).
