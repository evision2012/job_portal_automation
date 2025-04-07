import os
import pandas as pd
import PyPDF2

from mylib import city_by_states, is_same

all_cities = [x for val in city_by_states.values() for x in val]
all_cities = [x for x in all_cities if len(x)>3]



# Define stub functions to be implemented later

def extract_name(text):
    return "NO_NAME"



def extract_email(text):
    return "NO_EMAIL"



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




