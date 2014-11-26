import slate
import re

with open('files/Ferguson Grand Jury Testimony.pdf') as f:
    with open('files/output.txt', 'w') as out:
        doc = slate.PDF(f)

        # Skip first five pages
        skip = 4
        for page in doc:
            if skip:
                skip -= 1
                continue

            # Clean up some text that persists later on
            # if we don't get rid of it here first
            # page = page.replace("Gore Perry Reporting and Video FAX", "")
            page = re.sub("Page \d+", "", page)

            # Split on digits, leaving the line numbers in so that
            # we can easily trim off everything before and after
            lines = re.split("(\d+)", page)
            
            # We won't include anything before line 1
            # or after line 25
            beginning = False
            end = False
            lined_page = []
            for line in lines:
                if line == "1":
                    beginning = True
                if beginning:
                    lined_page.append(line)
                if end:
                    break
                if line == "25":
                    end = True

            # Now dump the line numbers and just keep the text
            text_page = []
            for index, line_text in enumerate(lined_page):
                if index % 2 != 0:
                    text_page.append(line_text)

            page = "".join(text_page)

            # Stitch the text back a little cleaner
            page = re.sub("\.  ", ".\n", page)
            page = page.replace("   ", " ")
            page = page.replace("  ", " ")

            # Cover page
            # page = page.replace("--- Fax: () - Email: schedule@goreperry.com Internet: < <www .goreperry.com > > ", "")

            out.write(page+"\n")
