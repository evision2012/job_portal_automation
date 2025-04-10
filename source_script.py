import os
import pandas as pd
import PyPDF2
import re
from rapidfuzz import process

import json

from mylib import city_by_states, is_same

all_cities = [x for val in city_by_states.values() for x in val]
all_cities = [x for x in all_cities if len(x)>3]



# Define stub functions to be implemented later



max_lines=20
def extract_name(text):
    FALSE_POSITIVES = {
        "career objective", "carrier objective", "curriculum vitae",
        "resume", "cv", "personal details", "profile", "objective",
        "softskills", "skillset", "summary", "contact", "job objective",
        "projects", "address", "cybersecurity", "analyst", "security",
        "soft", "skills", "experience", "education", "sysap", "technology",
        "vpn", "mobile", "email", "phone", "gmail", "yahoo", "outlook", 
        "linkedin", "no", "no.","p","professional","Digital","Forensics","work"
    }

    # Extract first `max_lines` lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    lines = lines[:max_lines]

    clean_lines = []
    for line in lines:
        # Remove mobile numbers
        line = re.sub(r'\+?\d{1,3}[-\s]?\d{10}', '', line)  
        line = re.sub(r'\d{3}[-\s]?\d{3}[-\s]?\d{4}', '', line)  

        # Remove false positives
        words = line.split()
        filtered_words = [word for word in words if word.lower().rstrip('.') not in FALSE_POSITIVES]
        cleaned_line = " ".join(filtered_words)

        if cleaned_line:
            clean_lines.append(cleaned_line)

    #print("Filtered Lines:", clean_lines)  # Debugging output

    # Regex patterns to extract names
    name_patterns = [
        r'^[A-Z][a-z]+\s+[A-Z]\.?\s+[A-Z][a-z]+$',  # "Rahul K Yadav"
        r'^[A-Z][a-z]+\s+[A-Z][a-z]+$',             # "Rahul Yadav"
        r'^[A-Z][a-z]+,\s*[A-Z][a-z]+$',            # "Yadav, Rahul"
        r'^[A-Z]+\s+[A-Z]+\s+[A-Z]+$',              # ALL CAPS "RAHUL KUMAR YADAV"
        r'^[A-Z][a-z]+(?: [A-Z][a-z]+)+$',          # "First Last"
        r'^[A-Z]\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # "J. Doe"
        r'^[A-Z]{2,}(?:\s+[A-Z]{2,})+$',            # "SHUBHAM KUMAR"
        r'(?i)^\s*Name\s*[:\-]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*$',
        r'^[A-Z]+(?:\s+[A-Z]+)*\.?$',
        r'^[A-Z][a-z]+\s+[A-Z][a-z]+\s+[a-z]$',
        r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z]){1,3}$',
        r'^[A-Z]{2,}(?:\s+[A-Z]{2,})*(?:\s+[A-Z]){1,}$',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)$',
        r'^[A-Z][a-z]+(?:\s+[A-Z]){2}$',
        r'^[A-Z]{2,}\s+[A-Z]{2,}$',
        r'^[A-Z]{2,}\s+[A-Z]{2,}\s+[a-z]+$', #RAHUL KUMAR Yadav
    ]

    # 1. Check for direct name matches
    for line in clean_lines:
      for pattern in name_patterns:
        match = re.fullmatch(pattern, line)
        if match:
            return match.group(1) if match.groups() else match.group(0)
        
        # Fallback to search if not full match
        match = re.search(pattern, line)
        if match:
            return match.group(1) if match.groups() else match.group(0)
    
    # 2. Check consecutive uppercase words
    for i in range(len(clean_lines) - 1):
        line1 = clean_lines[i]
        line2 = clean_lines[i + 1]
        if (
            re.fullmatch(r'^[A-Z][a-z]+\s+[A-Z][a-z]+$', line1) and
            re.fullmatch(r'^[A-Z][a-z]+$', line2)
        ):
            return f"{line1} {line2}"
        
    # PascalCase (e.g., Rahul Yadav)
    for i in range(len(clean_lines) - 1):
       if (
        re.fullmatch(r'^[A-Z][a-z]+$', clean_lines[i]) and
        re.fullmatch(r'^[A-Z][a-z]+$', clean_lines[i + 1])
    ):
        return f"{clean_lines[i]} {clean_lines[i + 1]}"
    
    # Check for two consecutive ALL CAPS lines (e.g., ANIRUDH + JOSHI)
    for i in range(len(clean_lines) - 1):
      if (
        re.fullmatch(r'^[A-Z]{2,}$', clean_lines[i]) and
        re.fullmatch(r'^[A-Z]{2,}$', clean_lines[i + 1])
    ):
        return f"{clean_lines[i]} {clean_lines[i + 1]}"

    for line in clean_lines:
        match = re.search(r'\b([A-Z]{2,})\s+([A-Z]{2,})\b', line)
        if match:
            return f"{match.group(1)} {match.group(2)}"

    return "NO_NAME"



def extract_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, text, re.IGNORECASE)
    return match.group() if match else "NO_EMAII"
    #return "NO_EMAIL"



def extract_phone(text):
    phone_patterns = [
        r"\+?91?\d{10,12}",
        r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{1,4}\)?[\s-]?)?\d{3,5}[\s-]?\d{3,5}[\s-]?\d{3,5}",
        r"\+?\d{1,3}[\s-]?\d{3,5}[\s-]?\d{3,5}[\s-]?\d{3,5}",  # Handles country codes (+63, +91)
        r"\+91[\s-]?\d{5}[\s-]?\d{5}",  # +91 with spaces or hyphens
        r"\d{10}",                        # 10-digit standard mobile number 
        r"\d{5}[\s-]?\d{5}",            # Numbers like 98765 43210
        r"\+91\s*\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}",  # +91 (807) 438-5280 or +91 807-438-5280
        r"\b\d{2,5}[\s-]?\d{2,5}[\s-]?\d{1,5}\b",    #7559 8498 34  
        r'(\d\s?){10,12}',  # for 1 2 3 4 5 6 7 8 3 4
        r'(\+91[\-\s]?)?[6-9]\d{9}',
        r'\+?\d{1,3}[\s\-]?\d{2,5}[\s\-]?\d{2,5}[\s\-]?\d{2,5}',
        r'\+?\d{1,3}[\s\-]?\d{2,5}[\s\-]?\d{2,5}[\s\-]?\d{2,5}',  
        r'(\d[\s\n]?){10,12}'  # for 1 in first line and 2 in second line

    ]

    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            phone_number = match.group(0)
            phone_number = re.sub(r"[^\d]", "", phone_number)  # Remove non-numeric characters
            #phone_number = re.sub(r"^91", "", phone_number)     # Remove country code if present
            if len(phone_number) > 10 and phone_number.startswith("91"):
                phone_number = phone_number[-10:]
            
            if len(phone_number) == 10:
                return phone_number
    return "NO_PHONE"



def extract_city(text):
    for city in all_cities:
        if city.lower() in text.lower():
            return city
    return "NO_CITY"



def extract_experience(text):      #Anand
    return "NO_EXPERIENCE"



def load_degrees():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Current file directory
    file_path = os.path.join(base_dir, "Data_Files", "degree.json")

    with open(file_path, "r", encoding="utf-8") as file:
        degrees = json.load(file)
    
 
    return {deg for deg in degrees if re.search(   r'\b('
        r'(B\.?\s?(Tech|Sc|E|Com|BA|Voc|CA|Pharma|Arch|BBA|BCA|BMS|BHM|BPT|Computer Application))'
        r'|(Bachelor of (Technology|Engineering|Science|Commerce|Arts|Computer Application|Business Administration))'
        r'|(M\.?\s?(Tech|Sc|Com|CA|BA|MBA))'
        r'|(Master of (Technology|Science|Commerce|Arts|Business Administration|Computer Application))'
        r')(\s+in\s+[A-Za-z &]+)?\b', deg, re.IGNORECASE)}

degree_list = load_degrees()

def extract_degree(text):
    text = text.strip().replace(',', '').replace('–', '-')
    for degree in degree_list:
        pattern = re.escape(degree)
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return degree
    return "NO_DEGREE"




def extract_stream(text):    #Ashutosh
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

def extract_graduation_year(text):        #ankit
    
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
