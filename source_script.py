import os
import pandas as pd
import PyPDF2
import re
import rapidfuzz import process
import json

from mylib import city_by_states, is_same

all_cities = [x for val in city_by_states.values() for x in val]
all_cities = [x for x in all_cities if len(x)>3]



# Define stub functions to be implemented later

def extract_name(text):
    return "NO_NAME"



def extract_email(text):
    return "NO_EMAIL"



def extract_phone(text):
    return "NO_PHONE"



def extract_city(text):
    return "NO_CITY"



def extract_experience(text):
    return "NO_EXPERIENCE"



def extract_degree(text):
    return "NO_DEGREE"



def extract_stream(text):
    return "NO_STREAM"



#  Load college list from JSON file
with open('D:\Vs - code\Job_Portal_Automation\Job_Portal_Automation\Data_Files\college.json', 'r', encoding='utf-8') as f:
    known_colleges = json.load(f)

#  Fuzzy matching function
def match_with_known_colleges(candidate):
    if not candidate or candidate == "NO_COLLEGE":
        return "NO_COLLEGE"
    match = process.extractOne(candidate, known_colleges, score_cutoff=80)
    if match:
        return match[0]
    return candidate

#  Main function to extract college name from resume text
def extract_college(text):
    text = text.replace('\r', ' ').replace('\t', ' ')
    lines = text.split('\n')

    # Find EDUCATION/ACADEMICS section
    edu_lines = []
    found = False
    for line in lines:
        if re.search(r'EDUCATION|ACADEMICS', line, re.IGNORECASE):
            found = True
            continue
        if found:
            if re.search(r'EXPERIENCE|PROJECT|SKILL|CERTIFICATE|CERTIFICATION|INTERNSHIP|LANGUAGE|DECLARATION', line, re.IGNORECASE):
                break
            edu_lines.append(line)

    if not edu_lines:
        return "NO_COLLEGE"

    education_section = ' '.join(edu_lines)

    # 1. Try full college names
    college_pattern = r"\b((?:[A-Z][A-Za-z&,\s.'-]{2,}\s){0,3}(University|College|Institute|Academy|Technology)(?:\s+of\s+[A-Z][A-Za-z]{2,})?)\b"
    for match in re.finditer(college_pattern, education_section, flags=re.IGNORECASE):
        return match_with_known_colleges(match.group(1).strip())

    # 2. Try abbreviations (JNTUA, RGPV, etc.)
    abbrev_pattern = r"(?:(?:from|at)\s+)?((?:[A-Z]\s*){2,}(?:[A-Za-z\s]{0,20}))"
    for match in re.finditer(abbrev_pattern, education_section):
        abbrev = match.group(1).strip()
        abbrev_clean = ' '.join(abbrev.split())
        if 2 <= len(abbrev_clean.replace(" ", "")) <= 15:
            return match_with_known_colleges(abbrev_clean)

    return "NO_COLLEGE"



def extract_graduation_year(text):
    return "NO_YEAR"



def extract_pdf_text(file_path):
    """Extracts and returns all text from a PDF file."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
    return text



def process_resumes(folder_path="Resumes", excel_path="report_students.xlsx"):
    # Ensure resume folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Load existing data or create new DataFrame
    if os.path.exists(excel_path):
        output_df = pd.read_excel(excel_path)
    else:
        columns = [
            "Name", "Email ID", "Phone Number", "Current Location",
            "Total Experience", "Under Graduation degree",
            "UG Specialization", "UG University/institute Name", "UG Graduation year"
        ]
        output_df = pd.DataFrame(columns=columns)

    # Process PDF files one by one
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing: {file_path}")
            text = extract_pdf_text(file_path)

            # Prepare new row from extracted data
            new_row = pd.DataFrame([{
                "Name": extract_name(text),
                "Email ID": extract_email(text),
                "Phone Number": extract_phone(text),
                "Current Location": extract_city(text),
                "Total Experience": extract_experience(text),
                "Under Graduation degree": extract_degree(text),
                "UG Specialization": extract_stream(text),
                "UG University/institute Name": extract_college(text),
                "UG Graduation year": extract_graduation_year(text)
            }])

            # Append new row to the existing DataFrame
            output_df = pd.concat([output_df, new_row], ignore_index=True)

            # Save to Excel immediately
            output_df.to_excel(excel_path, index=False)
            print(f"Data appended for file: {filename}")



# Run the function
if __name__ == "__main__":
    process_resumes()




