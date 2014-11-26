import slate

with open('files/sample.pdf') as f:
    with open('files/sample.txt', 'w') as out:
        doc = slate.PDF(f)
        for page in doc:
            out.write(page+"\n")
