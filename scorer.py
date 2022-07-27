import os
from rake_nltk import Rake
from helper import *
from ahocorapy.keywordtree import KeywordTree

nltk.download('punkt')
nltk.download('stopwords')

SKILLS_DB = {}

skills_kwtree = KeywordTree(case_insensitive=True)

needed_languages = ["python"]
general_skills = ["machine learning", "data science", "ai", "computer vision", "natural language processing", "NLP", "computer science", "artificial intelligence"]
libraries = ["matplotlib", "seaborn", "pytorch", "sklearn", "pandas", "numpy", "tensorflow", "nltk"]

possible_headings = ['Skills', 'Experience', 'Education', 'Languages', 'Libraries', 'General Skills', 'Courses', 'Courses Taken', 'Projects',
                     'Employment', 'Career', 'Summary']

for language in needed_languages:
    lower_language = language.lower()
    SKILLS_DB[lower_language] = 1.5
    skills_kwtree.add(lower_language)

for skill in general_skills:
    lower_skill = skill.lower()
    SKILLS_DB[lower_skill] = 0.8
    skills_kwtree.add(lower_skill)

for library in libraries:
    lower_library = library.lower()
    SKILLS_DB[lower_library] = 0.5
    skills_kwtree.add(lower_library)

skills_kwtree.finalize()

colleges_file = open("top_colleges.txt", "r")
college_kwtree = KeywordTree(case_insensitive=False)

colleges = colleges_file.read().split("\n")
for college in colleges:
    college_kwtree.add(college)

college_kwtree.finalize()

def main_nlp(text):
    r = Rake(include_repeated_phrases=False, min_length=1, max_length=3)
    r.extract_keywords_from_text(text)

    words_ranks = [keyword for keyword in r.get_ranked_phrases_with_scores() if keyword[0] >= 9]
    return words_ranks

def score_resume(text, threshold):

    score = 0

    is_in_university = college_kwtree.search(text)

    if is_in_university!=None:
        score+=0.5

    skills = skills_kwtree.search_all(text)
    if skills==None:
        return False

    for skill in skills:
        score += SKILLS_DB[skill[0].lower()]

    # evaluate resume
    if score >= threshold:
        return True
    else:
        return False