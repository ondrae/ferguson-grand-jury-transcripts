from operator import itemgetter
import re
import sys
import xml.etree.cElementTree as ET

def fix_ocr_errors_in_line(line_in):
	fixed = line_in
	# fix Urn = Um
	fixed = re.sub(r'\b([Uu])rn\b', r'\1m', fixed)
	# fix rna' am = ma'am
	fixed = re.sub('rna\' am', 'ma\'am', fixed)
	# fix IS = 's
	fixed = re.sub(r'\bIS\b', 'is', fixed)
	# fix 1s = is and 1n = in
	fixed = re.sub(r'\b1s\b', r'is', fixed)
	fixed = re.sub(r'\b1n\b', r'in', fixed)

	# fix other i = 1 variations
	fixed = re.sub('1ng', 'ing', fixed)
	fixed = re.sub('r1e', 'rie', fixed)
	fixed = re.sub('p1e', 'pie', fixed)
	fixed = re.sub('r1m', 'rim', fixed)
	fixed = re.sub('r1o', 'rio', fixed)
	fixed = re.sub('g1v', 'giv', fixed)
	fixed = re.sub('exam1n', 'examin', fixed)
	fixed = re.sub('aga1n', 'again', fixed)
	fixed = re.sub('excess1ve', 'excessive', fixed)
	fixed = re.sub('1gnore', 'ignore', fixed)
	fixed = re.sub('1mage', 'image', fixed)	
	fixed = re.sub('1ssue', 'issue', fixed)
	fixed = re.sub('magaz1ne', 'magazine', fixed)
	fixed = re.sub('mus1c', 'music', fixed)
	fixed = re.sub('n1ne', 'nine', fixed)
	fixed = re.sub('occas1on', 'occasion', fixed)
	fixed = re.sub('op1n1on', 'opinion', fixed)
	fixed = re.sub('se1ze', 'seize', fixed)
	fixed = re.sub('s1gn', 'sign', fixed)
	fixed = re.sub('s1nce', 'since', fixed)
	fixed = re.sub('s1r', 'sir', fixed)
	fixed = re.sub('s1x', 'six', fixed)
	fixed = re.sub('s1ze', 'size', fixed)
	fixed = re.sub('superv1sor', 'supervisor', fixed)
	fixed = re.sub('v1ce', 'vice', fixed)

	# fix some one-offs
	fixed = re.sub('Sox-rays', 'So x-rays', fixed)
	fixed = re.sub('pun ked', 'punked', fixed)
	fixed = re.sub(ur' \u2022', '', fixed)

	return fixed

def parseXML(xml_in):
	'''
	parse the document XML
	'''

	# if two fragments of text are within LINE_TOLERANCE of each other they're on the same line
	LINE_TOLERANCE = 4
	# if two fragments of text are within INDENT_TOLERANCE of each other they're at the same level of indentation
	INDENT_TOLERANCE = 40
	# list of cover page numbers
	COVER_PAGES = [1,83,277,489,670,956,1226,1441,1675,1781,1923,2121,2376,2634,2744,2975,3139,3394,3580,3850,4054,4279,4388,4654]
	# page bounding box
	FORMAT_PAGE = {'from_page': 1, 'to_page': 4799, 'left': 0.0, 'top': 792.0, 'right': 614.0, 'bottom': 0.0}
	# dicts of format ranges and associated bounding boxes
	FORMAT_RANGES = [
		{'from_page': 1, 'to_page': 2743, 'left': 160.0, 'top': 712.0, 'right': 586.0, 'bottom': 84.0},
		{'from_page': 2744, 'to_page': 4653, 'left': 125.0, 'top': 712.0, 'right': 555.0, 'bottom': 77.0},
		{'from_page': 4654, 'to_page': 4799, 'left': 118.0, 'top': 753.0, 'right': 588.0, 'bottom': 40.0}
	]
	# if true, capture all text, including that outside the focus areas
	CAPTURE_ALL_TEXT = False
	# :NOTE: set page offset to 500 when parsing sample.xml
	PAGE_OFFSET = 0

	# get the page elements
	tree = ET.ElementTree(file=xml_in)
	pages = tree.getroot()

	if pages.tag != "pages":
		sys.exit("ERROR: pages.tag is %s instead of pages!" % pages.tag)

	# all the document lines
	all_lines = []
	# step through the pages
	for page in pages:
		# get all the textline elements
		textlines = page.findall("./textbox/textline")
		#print "found %s textlines" % len(textlines)

		# is this a cover page?
		is_cover_page = int(page.attrib["id"]) + PAGE_OFFSET in COVER_PAGES
		focus_bbox = FORMAT_PAGE
		# get the bounding box for the transcript area of the page
		if not is_cover_page:
			for page_format in FORMAT_RANGES:
				if page_format['from_page'] <= int(page.attrib["id"]) + PAGE_OFFSET <= page_format['to_page']:
					focus_bbox = page_format


		# step through the textlines
		lines = []
		for textline in textlines:
			# get the boundaries of the textline [left,bottom,right,top]
			line_bounds = [float(s) for s in textline.attrib["bbox"].split(',')]
			#print "line_bounds: %s" % line_bounds
			# is this line inside the focus area?
			is_in_focus = line_bounds[3] < focus_bbox['top'] and line_bounds[3] > focus_bbox['bottom']

			# get all the characters in this textline
			chars = list(textline)
			#print "found %s characters in this line." % len(chars)

			# combine all the characters into a single string
			line_text = ""
			line_left = line_bounds[2]
			for char in chars:
				try:
					char_left = float(char.attrib["bbox"].split(',')[0])
					# if the line's inside the focus box, respect the left bounds
					if is_in_focus:
						if char_left > focus_bbox['left']:
							line_text = line_text + char.text
							line_left = min(char_left, line_left)

					# otherwise, just add the character
					elif CAPTURE_ALL_TEXT:
						line_text = line_text + char.text
						line_left = min(char_left, line_left)

				# skip empty <text> elements
				except KeyError:
					pass

			# strip edge & multiple spaces
			line_text = re.sub(' +', ' ', line_text.strip())
			# fix OCR errors
			line_text = fix_ocr_errors_in_line(line_text)
			# ignore page numbers
			if not CAPTURE_ALL_TEXT:
				if re.match('Page', line_text):
					line_text = ""

			# if line text survived, save a description of the line
			if line_text != "":
				line = {'left': line_left, 'top': line_bounds[3], 'text': line_text}
				lines.append(line)

		#print "page %s has %s lines" % (page.attrib["id"], len(lines))

		# sort the lines by top position (reverse because measures in PDF/XML are from the bottom of the document)
		lines.sort(key=itemgetter('top'), reverse=True)

		# consolidate lines that have the same top (within tolerance)
		consolidated_lines = []
		line_collection = []
		line_top = lines[0]['top']
		for line in lines:
			if abs(line['top'] - line_top) < LINE_TOLERANCE:
				line_collection.append(line)

			else:
				# assure that text segments appear in the correct order
				line_collection.sort(key=itemgetter('left'))
				consolidated_lines.append(line_collection)

				# reset
				line_collection = [line]
				line_top = line['top']

		# add the last line collection to the consolidated lines
		line_collection.sort(key=itemgetter('left'))
		consolidated_lines.append(line_collection)

		# merge each line's text
		for line_segments in consolidated_lines:
			merged_line = dict(line_segments[0])
			merged_line['text'] = " ".join([segment['text'] for segment in line_segments])
			all_lines.append(merged_line)

	# now clean and categorize the text
	last_line_left = 0.0
	last_paragraph_left = 0.0
	for line in all_lines:
		# check for a name
		name_match = re.search(r'(M[RS]\. [A-Z]+):', line['text'])

		# check for Q/A (will give false positive for lines of text starting with 'A ...' that aren't answers)
		qa_match = re.match(r'[QA] ', line['text'])

		# check for an open parens
		parens_match = re.match(r'\(', line['text'])

		# get the diffs for the position of this line
		line_diff = line['left'] - last_line_left
		paragraph_diff = line['left'] - last_paragraph_left
		# check for a significant change in the indentation
		indent_change = abs(line_diff) > INDENT_TOLERANCE

		if name_match or qa_match or parens_match or (indent_change and line['left'] > last_line_left):
			message = "--++ new paragraph!"
			if abs(paragraph_diff) > INDENT_TOLERANCE:
				message = message + " (at new indentation)"

			print message
			last_paragraph_left = line['left']

		last_line_left = line['left']

		print "(%s,%s) %s" % (line['left'], line['top'], line['text'].encode('utf-8'))



if __name__ == "__main__":
	# :NOTE: if parsing sample.xml, set PAGE_OFFSET above to 500
	parseXML("files/ferguson_grand_jury_testimony.xml")
