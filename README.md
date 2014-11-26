ferguson-grand-jury-transcripts
===============================

Converting the Ferguson Grand Jury transcripts into something more readable. We want to display them on the [SayIt](http://sayit.mysociety.org/) service by [MySociety](https://www.mysociety.org/). Court transcripts [look very nice](http://leveson.sayit.mysociety.org/hearing-14-may-2012/lord-augustine-odonnell) on  SayIt.

### Raw Transcripts
http://graphics8.nytimes.com/newsgraphics/2014/11/24/ferguson-assets/grand-jury-testimony.pdf

### OCR Transcripts
https://www.dropbox.com/s/67unqhdrb8jhgr0/Ferguson%20Grand%20Jury%20Testimony.pdf?dl=0

### Sample Files
First ten pages of the OCR transcript are at `files/sample.pdf`

### Required Libraries
I started with pdfminer, but it attempts to maintain the layout of the PDF. We don't want that. Doing much better with [Slate](https://pypi.python.org/pypi/slate). It apparently depends on an old version of pdfminer though, so I had to install it like `sudo pip install --upgrade --ignore-installed slate==0.3 pdfminer==20110515` which I found [here](https://github.com/timClicks/slate/issues/5#issuecomment-53450633).

### Transform Scripts
Starting at `convert.py`

### Final Transcripts - ToDo
http://ferguson.sayit.mysociety.org/


## Conversion Steps
1. Download the OCR transcripts
2. Choose a PDF to text converter - I'm starting with pdfminer
3. Convert the text to XML
4. Convert the XML to [Akoma Ntoso](http://sayit.mysociety.org/about/developers#an)
5. Format all the people involved and sections of the transcript.
6. Upload to SayIt
7. Promote to the media

### Twitter Discussion
https://twitter.com/steiny/status/537297171255943168