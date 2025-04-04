import os
import pandas as pd
import PyPDF2
import re

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

    print("Filtered Lines:", clean_lines)  # Debugging output

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



def extract_college(text):
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




