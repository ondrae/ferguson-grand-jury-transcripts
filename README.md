ferguson-grand-jury-transcripts
===============================

Converting the Ferguson Grand Jury transcripts into something more readable. We want to display them on the [SayIt](http://sayit.mysociety.org/) service by [MySociety](https://www.mysociety.org/). Court transcripts [look very nice](http://leveson.sayit.mysociety.org/hearing-14-may-2012/lord-augustine-odonnell) on  SayIt.

### Raw Transcripts
http://graphics8.nytimes.com/newsgraphics/2014/11/24/ferguson-assets/grand-jury-testimony.pdf

### OCR Transcripts
https://www.dropbox.com/s/67unqhdrb8jhgr0/Ferguson%20Grand%20Jury%20Testimony.pdf?dl=0

### Converted to text
https://docs.google.com/uc?id=0ByV6qGuufDXDZGdtVl90aU1YV0E&export=download
The original PDF has three slightly different formats and we produced a different text file for each format. There's also one single file that has the entire contents of the document.

Two sets of files included; one with page numbers (extracted from the document) and one without. The page numbers might be useful if we need to refer back to the original document for any reason, and they're easy to skip when parsing if not.

The page numbers for the last set of pages (4654-4799) are in a different format than the others; they're all prefixed with 'GorePerry Reporting & Video...'


### Final Transcripts - Work in progress
http://ferguson.sayit.mysociety.org/


## Conversion Steps
1. Download the OCR transcripts
2. Choose a PDF to text converter
3. Convert the text to [Akoma Ntoso](http://sayit.mysociety.org/about/developers#an)
4. Format all the people involved and sections of the transcript.
5. Upload to SayIt
6. Promote to the media

### Twitter Discussion
https://twitter.com/steiny/status/537297171255943168

### Initial attempts
I started with pdfminer, but it attempts to maintain the layout of the PDF. We don't want that. Doing much better with [Slate](https://pypi.python.org/pypi/slate). It apparently depends on an old version of pdfminer though, so I had to install it like `sudo pip install --upgrade --ignore-installed slate==0.3 pdfminer==20110515` which I found [here](https://github.com/timClicks/slate/issues/5#issuecomment-53450633).

We ended up using a different tool though.
