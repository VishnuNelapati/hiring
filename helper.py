import spacy
from spacy.matcher import Matcher
import docx2txt
import nltk

from io import StringIO
from io import BytesIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import os

def get_resume_from_file(resume_file):
    if resume_file.split('.')[-1] == 'pdf':
        text = extract_text_from_pdf_file(resume_file)
    elif resume_file.split('.')[-1] == 'docx':
        text = extract_text_from_docx(resume_file)
    else:
        text = "INVALID FILE"
        print(text)
    return text

def get_resumes_from_dir(dir):
    resumes = []
    for file in os.listdir(dir):
        try:
            resume_file = os.path.join(dir, file)
            text = get_resume_from_file(resume_file)

            if text=="INVALID FILE":
                continue 

        except:
            continue
        resumes.append(text)
    return resumes

def extract_text_from_docx(docx_path):
    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace('\t', ' ')
    return None

def extract_text_from_pdf(pdf_file):
    output_string = StringIO()
    parser = PDFParser(pdf_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    return output_string.getvalue()

def extract_text_from_pdf_file(pdf_file):
    with open(pdf_file, 'rb') as in_file:
        text = extract_text_from_pdf(in_file)
    return text

def extract_text_from_stream(pdf_stream):
    pdf_memory_file = BytesIO()
    pdf_memory_file.write(pdf_stream)
    text = extract_text_from_pdf(pdf_memory_file)
    return text


def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    nlp_text = nlp(resume_text)
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', [pattern])
    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        
    return span.text


def extract_skills(input_text, SKILLS_DB):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w.lower() for w in filtered_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(
        map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills database
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in SKILLS_DB:
            found_skills.add(ngram)

    return found_skills


def compare_similarity(text1, text2):
    nlp = spacy.load('en_core_web_md')
    doc = nlp(text1)
    doc2 = nlp(text2)
    return doc.similarity(doc2) > 0.5


def separate_sections(text, possible_headings):
    lines = text.split('\n')
    section_text = ''
    section_dict = {}

    previous_header = ''
    for line in lines:
        if line == '' or line == '•':
            continue

        if len(line.split()) <= 2:

            if previous_header != '':
                for possible_heading in possible_headings:
                    if compare_similarity(possible_heading, line):
                        section_dict[previous_header] = section_text
            previous_header = line.replace(':', '')
            section_text = ''

            continue

        section_text += line

    reads = []
    readable = {}

    for section in section_dict.values():
        read = ''
        for char in range(len(section)):
            if char + 1 < len(section):
                if section[char] == ' ' and section[char + 1] == ' ':
                    read += '\n'
                    continue
            elif char == ' ':
                break
            if section[char] == '' or section[char] == '\n':
                read += '\n'
            else:
                read += section[char]
        reads.append(read)

    for h, r in zip(section_dict.keys(), reads):
        readable[h] = r

    return readable
