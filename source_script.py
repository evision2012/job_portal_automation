import os
import pandas as pd
import PyPDF2
import re
from rapidfuzz import process

import json

from mylib import city_by_states, is_same

all_cities = [x for val in city_by_states.values() for x in val]



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







college_keywords = [
    "University", "College", "Institute", "Academy",
    "Technology", "Polytechnic", "Faculty" ,"Academy"
]

def has_college_keyword(segment):
    segment_lower = segment.lower()
    for kw in college_keywords:
        kw_lower = kw.lower()
        if re.search(rf'\b{re.escape(kw_lower)}\b', segment_lower):
            return True
    return False

def clean_segment(segment):
    # Remove trailing punctuation and irrelevant words
    segment = segment.strip().rstrip(".,;")
    # Remove small connecting words at the start (e.g., "and", "in", "for")
    segment = re.sub(r'^(and|in|for|at|of)\s+', '', segment, flags=re.IGNORECASE)
    return segment

def extract_college(text):
    text = text.replace('\r', ' ').replace('\t', ' ').strip()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Step 1: Prioritize lines with education-related keywords (case-insensitive)
    education_keywords = ["education", "degree", "bachelor", "mba", "college", "diploma", "ssc", "hsc"]
    prioritized_lines = []
    other_lines = []
    for line in lines:
        line_lower = line.lower()
        if any(kw in line_lower for kw in education_keywords):
            prioritized_lines.append(line)
        else:
            other_lines.append(line)
    
    # Step 2: Split segments using pipes, commas, hyphens, etc.
    for line in prioritized_lines + other_lines:
        # Split by |, commas, hyphens, slashes
        segments = re.split(r'[|,/–-]', line)
        for segment in reversed(segments):
            cleaned_segment = clean_segment(segment)
            if has_college_keyword(cleaned_segment):
                words = cleaned_segment.split()
                if len(words) >= 2 and not words[0].lower() in {"and", "in", "for"}:
                    return cleaned_segment
    
    # Step 3: Fallback for multiple keywords in a line
    for line in prioritized_lines + other_lines:
        cleaned_line = clean_segment(line)
        count = 0
        for kw in college_keywords:
            if re.search(rf'\b{re.escape(kw.lower())}\b', cleaned_line.lower()):
                count += 1
                if count >= 2:
                    return cleaned_line
    
    # Step 4: Check for single keyword with sufficient length
    for line in prioritized_lines + other_lines:
        cleaned_line = clean_segment(line)
        if has_college_keyword(cleaned_line) and len(cleaned_line.split()) >= 3:
            return cleaned_line
    
    return "NO_COLLEGE"





def extract_graduation_year(text):
    # Normalize text
    text = text.replace('\r', '\n')
    
    # Define patterns to locate education section headers
    education_headers = [
        "education", "educational background", "academic qualifications", 
        "education details", "academic profile", "qualifications"
    ]
    
    # Define common section endings to stop at
    section_enders = [
        "experience", "skills", "projects", "certifications", "work experience",
        "internship", "profile", "personal", "achievements", "summary"
    ]

    # Split text into lines
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]

    # Find education section start
    edu_start = -1
    for idx, line in enumerate(lines):
        if any(header in line.lower() for header in education_headers):
            edu_start = idx
            break
    
    if edu_start == -1:
        return "NO_YEAR"
    
    # Scan from education section until next major section
    edu_lines = []
    for idx in range(edu_start + 1, len(lines)):
        line_lower = lines[idx].lower()
        if any(ender in line_lower for ender in section_enders):
            break
        edu_lines.append(lines[idx])

    # Combine education lines into one text block
    edu_text = " ".join(edu_lines)

    # Find all 4-digit years in the text
    years = re.findall(r'\b(20[1-2][0-9])\b', edu_text)

    # Filter only years in 2015–2025 range
    valid_years = [year for year in years if 2015 <= int(year) <= 2025]

    # Exclude 10th/12th lines
    filtered_years = []
    for line in edu_lines:
        if any(x in line.lower() for x in ["10", "x", "ssc", "cbse", "hsc", "12", "xii"]):
            continue
        found_years = re.findall(r'\b(20[1-2][0-9])\b', line)
        for y in found_years:
            if 2015 <= int(y) <= 2025:
                filtered_years.append(y)

    # Choose the last matching year assuming UG is mentioned after 10th/12th
    if filtered_years:
        return max(filtered_years)  # latest year

    # Fallback to any valid year found
    if valid_years:
        return max(valid_years)

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
    "File Name": filename,
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
