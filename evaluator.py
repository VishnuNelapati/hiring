from helper import *
import os
from scorer import *

rejected_resumes = get_resumes_from_dir("Resumes/Indeed-Rejected")
offered_resumes = get_resumes_from_dir("Resumes/Notion-Everyone")

correct = 0
total = 0

for resume in rejected_resumes:
    if score_resume(resume, 13)==False:
        correct+=1
    total+=1


for resume in offered_resumes:
    if score_resume(resume, 13)==True:
        correct+=1
    total+=1

accuracy = correct/total
print(accuracy)