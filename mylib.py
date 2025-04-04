from Levenshtein import distance as levenshtein_distance

def is_same(input_word, correct_word, threshold = 2):
    """
    Check if input_word has minor spelling mistakes compared to correct_word.
    Ignores case sensitivity and allows for small errors.

    Args:
        input_word (str): Word to be checked.
        correct_word (str): The correct reference word.
        threshold (int): Maximum allowed edit distance to consider words similar.

    Returns:
        bool: True if input_word is nearly the same as correct_word, False otherwise.
    """
    # Convert both words to lowercase to make comparison case insensitive
    input_word = str(input_word).lower()
    correct_word = str(correct_word).lower()
    
    # Calculate the Levenshtein distance
    distance = levenshtein_distance(input_word, correct_word)
    
    # Return True if the distance is within the allowed threshold
    return distance <= threshold


# Example usage
#print(is_same("hello", "Hello"))  # True (case difference)
#print(is_same("helllo", "hello"))  # True (1 letter extra)
#print(is_same("helo", "hello"))    # True (1 letter missing)
#print(is_same("hllo", "hello"))    # True (1 letter replaced)
#print(is_same("heallo", "hello"))  # False (too many differences)




# Cities by States



city_by_states = {
    "Andhra Pradesh": [
        "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool",
        "Tirupati", "Rajahmundry", "Kakinada", "Kadapa", "Anantapur",
        "Eluru", "Ongole", "Machilipatnam", "Chittoor", "Hindupur",
        "Bhimavaram", "Tadepalligudem", "Proddatur", "Adoni", "Amalapuram",
        "Madanapalle", "Dharmavaram", "Markapur", "Nandyal", "Srikakulam",
        "Rajampet", "Peddapuram", "Rayachoti", "Bapatla",
        "Nellore", "Palnadu", "Kovur", "Tadipatri", "Punganur", "Chilakaluripet",
        "Sattenapalli", "Bobbili", "Peddapalli", "Anakapalle", "Addanki",
        "Chintapalli", "Peddagummadiv", "Brahmanapalli", "Tuni", "Tanuku",
        "Vinukonda", "Amadalavalasa", "Srikalahasti", "Mummidivaram",
    ],
    "Arunachal Pradesh": [
        "Itanagar", "Tawang", "Ziro", "Pasighat", "Roing",
        "Tezu", "Bomdila", "Naharlagun", "Changlang", "Seppa",
        "Yingkiong", "Namsai", "Hawai", "Aalo", "Raga", "Tali", 
        "Joram", "Dirang", "Nirjuli", "Sangdupota", "Koloriang",
    ],
    "Assam": [
        "Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon",
        "Tinsukia", "Tezpur", "Bongaigaon", "North Lakhimpur",
        "Karimganj", "Goalpara", "Dhubri", "Haflong", "Sibsagar",
        "Sonari", "Nalbari", "Jorhat", "Barpeta", "Hojai", "Bajali",
        "Dibrugarh", "Dhemaji", "Morigaon", "Golaghat", "Kamrup", "Barpeta",
        "Mangaldoi", "Bilasipara", "Lakhimpur", "Charaideo", "Majuli",
        "Moran", "Darrang", "Hailakandi", "Haflong", "Tihu", "Bongaigaon",
    ],
    "Bihar": [
        "Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia",
        "Darbhanga", "Begusarai", "Ara", "Katihar", "Munger",
        "Chhapra", "Saharsa", "Samastipur", "Bettiah", "Siwan",
        "Motihari", "Kishanganj", "Nalanda", "Buxar", "Nawada",
        "Lakhisarai", "Khagaria", "Sheikhpura", "Jamui", "Jahanabad",
        "Supaul", "Vaishali", "Rohtas", "Aurangabad", "Banka",
        "Bhabhua", "Chapra", "Buxar", "Chhapra", "Dehri", "Rajgir",
        "Patna City", "Phulwari Sharif", "Bihar Sharif",
    ],
    "Chhattisgarh": [
        "Raipur", "Bhilai", "Bilaspur", "Korba", "Durg",
        "Rajnandgaon", "Jagdalpur", "Ambikapur", "Raigarh", "Mahasamund",
        "Kanker", "Dhamtari", "Dalli-Rajhara", "Champa", "Janjgir",
        "Bemetara", "Kondagaon", "Balod", "Raipur City", "Bijapur",
        "Narayanpur", "Balodabazar", "Mungeli", "Surguja", "Jashpur", "Kabirdham",
        "Surajpur", "Korba District", "Sarguja", "Dongargarh", "Kawardha", 
    ],
    "Goa": [
        "Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda",
        "Bicholim", "Curchorem", "Sanguem", "Valpoi", "Quepem",
        "Canacona", "Sanquelim", "Cortalim", "Assagao", "Aldona",
        "Baga", "Calangute", "Candolim", "Anjuna", "Colva", "Benaulim",
        "Varca", "Majorda", "Navelim", "Raia", "Mormugao", "Verem",
        "Ribandar", "Sirsaim", "Taleigao", "Porvorim", "Assagao",
    ],
    "Gujarat": [
        "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar",
        "Jamnagar", "Junagadh", "Gandhinagar", "Anand", "Nadiad",
        "Morbi", "Porbandar", "Navsari", "Bharuch", "Patan",
        "Godhra", "Mehsana", "Vapi", "Valsad", "Himmatnagar",
        "Dahod", "Bhuj", "Veraval", "Wankaner", "Gandhinagar",
        "Surendranagar", "Unjha", "Rajpipla", "Visnagar", "Palanpur",
        "Modasa", "Kalol", "Viramgam", "Borsad", "Kheda", "Kadi", 
        "Dholka", "Mansa", "Chhota Udepur", "Dahej", "Udhna", "Ankleshwar", 
        "Navsari", "Tapi", "Daman", "Diu",
    ],
    "Haryana": [
        "Gurgaon", "Faridabad", "Panipat", "Ambala", "Karnal",
        "Sonipat", "Rohtak", "Hisar", "Yamunanagar", "Panchkula",
        "Bhiwani", "Bahadurgarh", "Sirsa", "Jind", "Kaithal",
        "Palwal", "Fatehabad", "Mahendragarh", "Rewari", "Narnaul",
        "Barwala", "Ratia", "Hansi", "Tosham", "Bawani Khera", 
        "Pinjore", "Shahbad", "Nuh", "Samalkha", "Rohat",
    ],
    "Himachal Pradesh": [
        "Shimla", "Manali", "Dharamshala", "Mandi", "Kullu",
        "Chamba", "Solan", "Bilaspur", "Hamirpur", "Una",
        "Palampur", "Nahan", "Paonta Sahib", "Keylong", "Sundernagar",
        "Kangra", "Narkanda", "Kullu", "Bhuntar", "Arki", "Reckong Peo",
        "Jubbal", "Chintpurni", "Tissa", "Nagrota Surian", "Ghumarwin",
    ],
    "Jharkhand": [
        "Ranchi", "Jamshedpur", "Dhanbad", "Bokaro Steel City",
        "Hazaribagh", "Deoghar", "Giridih", "Ramgarh", "Phusro",
        "Chakradharpur", "Gumla", "Lohardaga", "Chaibasa", "Seraikela",
        "Dumka", "Godda", "Pakur", "Koderma", "Simdega", "Latehar",
        "Khunti", "Sahibganj", "Palamu", "Chatra", "Bermo", "Jamtara",
        "Ramgarh", "Madhupur", "Barkagaon", "Mandar", "Tundi", "Tata Nagar",
    ],
    "Karnataka": [
        "Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Belagavi",
        "Davanagere", "Ballari", "Shivamogga", "Tumakuru", "Udupi",
        "Mandya", "Chikkamagaluru", "Hassan", "Bijapur", "Bidar",
        "Gadag", "Chitradurga", "Raichur", "Karwar", "Hospet",
        "Kolar", "Bagalkot", "Gulbarga", "Hubli", "Vijayapura", "Hampi",
        "Sirsi", "Yadgir", "Bhadravati", "Sagar", "Channarayapatna", 
        "Chikkaballapur", "Haveri", "Ramanagara", "Humnabad", "Puttur", 
        "Karwar", "Karkala", "Alur", "Mudigere", "Kunigal", "Kadur",
    ],
    "Kerala": [
        "Thiruvananthapuram", "Kochi", "Kozhikode", "Kannur", "Kottayam",
        "Alappuzha", "Palakkad", "Thrissur", "Malappuram", "Muvattupuzha",
        "Vypin", "Varkala", "Pathanamthitta", "Ernakulam", "Punalur",
        "Kasaragod", "Payyanur", "Neyyattinkara", "Kalpetta", "Perumbavoor",
        "Thalassery", "Manjeri", "Kasargod", "Kollam", "Anchal", "Aluva",
        "Muvattupuzha", "Kanhangad", "Pattambi", "Perinthalmanna", "Sreekariyam",
        "Azhikkal", "Chalakudy", "Edappal", "Kollam", "Ponnani", "Edathala",
        "Cochin", "Irinjalakuda", "Kunnamkulam", "Changanassery", "Chirakkal",
    ],
    "Madhya Pradesh": [
        "Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain",
        "Sagar", "Ratlam", "Rewa", "Satna", "Dewas",
        "Chhindwara", "Murwara", "Vidisha", "Shivpuri", "Neemuch",
        "Khandwa", "Balaghat", "Mandla", "Damoh", "Betul", "Hoshangabad",
        "Shahdol", "Burhanpur", "Tikamgarh", "Panna", "Seoni", "Raisen",
        "Katni", "Alirajpur", "Anuppur", "Ashoknagar", "Mandsaur", "Rajgarh",
        "Narsinghpur", "Chhatarpur", "Shivpuri", "Datia", "Chhindwara", 
        "Bhilai", "Guna", "Pichhore", "Chhattarpur", "Dhar", "Jhabua",
    ],
    "Maharashtra": [
        "Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", 
        "Solapur", "Kolhapur", "Amravati", "Sangli", "Latur", "Akola", 
        "Jalgaon", "Nanded", "Ratnagiri", "Chandrapur", "Dhule", 
        "Malegaon", "Ichalkaranji", "Jalna", "Ambarnath", "Badlapur", 
        "Panvel", "Ulhasnagar", "Kalyan", "Dombivli", "Vasai", 
        "Virar", "Satara", "Beed", "Alibag", "Baramati", "Shirdi", 
        "Pandharpur", "Chiplun", "Osmanabad", "Gondia", "Hingoli", 
        "Washim", "Yavatmal", "Karad", "Mahabaleshwar", "Palghar", 
        "Talegaon", "Lonavala", "Vita", "Malkapur", "Dahanu", "Manmad", 
        "Uran", "Sinnar", "Akluj", "Khamgaon", "Wai", "Pusad", 
        "Shrirampur", "Sangamner", "Pathardi", "Digras", "Barshi", 
        "Buldhana", "Kinwat", "Nandurbar", "Tumsar", "Gadchiroli", 
        "Vijayapura", "Achalpur", "Murtijapur", "Rajgurunagar", 
        "Parli", "Ambajogai", "Chandrapur", "Nagpur", "Bhandara", 
        "Wardha", "Navi Mumbai", "Aurangabad",
    ],
    "Manipur": [
        "Imphal", "Bishnupur", "Thoubal", "Churachandpur", "Kakching",
        "Jiribam", "Senapati", "Tamenglong", "Ukhrul", "Noney", 
        "Chandel", "Kangpokpi", "Moirang", "Lamlai", "Tengnoupal",
    ],
    "Meghalaya": [
        "Shillong", "Tura", "Nongpoh", "Cherrapunji", "Jowai", 
        "Mawkyrwat", "Bojan", "Nartiang", "Mairang", "Baghmara", 
        "Williamnagar", "Resubelpara", "Nongstoin", "Pynursla", 
        "Khasi Hills", "Garo Hills", "Ri Bhoi", "East Khasi Hills",
    ],
    "Mizoram": [
        "Aizawl", "Lunglei", "Serchhip", "Champhai", "Kolasib", 
        "Mamit", "Saiha", "Lawngtlai", "Hnahthial", "Kolasib", 
        "Khawzawl", "Vairengte", "Zohmun", "Tlabung", "Darlawn", 
        "Ngopa", "Thenzawl", "Bungkawn", "Siaha",
    ],
    "Nagaland": [
        "Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha", 
        "Mon", "Phek", "Zunheboto", "Kiphire", "Longleng", 
        "Tseminyu", "Chümoukedima", "Peren", "Jalukie", 
        "Lotha", "Kohima Town", "Dimapur Town",
    ],
    "Odisha": [
        "Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur",
        "Puri", "Balasore", "Baripada", "Bhadrak", "Angul",
        "Dhenkanal", "Jagatsinghpur", "Jeypore", "Khordha", "Nayagarh",
        "Balangir", "Bargarh", "Kendrapara", "Koraput", "Malkangiri",
        "Sundargarh", "Nimapara", "Khariar", "Rayagada", "Pattamundai",
        "Boudh", "Deogarh", "Ganjam", "Kendujhar", "Mayurbhanj",
    ],
    "Punjab": [
        "Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala",
        "Bathinda", "Hoshiarpur", "Mohali", "Pathankot", "Ferozepur",
        "Moga", "Rupnagar", "Kapurthala", "Faridkot", "Mansa", 
        "Sri Muktsar Sahib", "Tarn Taran", "Fatehgarh Sahib", "Nawanshahr",
        "Zira", "Phagwara", "Sultanpur Lodhi", "Malerkotla", 
        "Samrala", "Ajnala", "Dera Baba Nanak", "Moga", "Rampura Phul",
    ],
    "Rajasthan": [
        "Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer",
        "Bikaner", "Alwar", "Bharatpur", "Sikar", "Jaisalmer",
        "Pali", "Churu", "Sawai Madhopur", "Nagaur", "Barmer",
        "Tonk", "Banswara", "Dungarpur", "Jhunjhunu", "Sri Ganganagar",
        "Hanumangarh", "Jhalawar", "Karauli", "Ratangarh", "Chittorgarh",
        "Rajsamand", "Kishangarh", "Beawar", "Mandawa", "Shahpura", 
        "Merta City", "Pali", "Sirohi", "Kota", "Bhilwara", 
    ],
    "Sikkim": [
        "Gangtok", "Namchi", "Geyzing", "Mangan", "Rangpo",
        "Singtam", "Jorethang", "Rabong", "Sichey", "Tadong",
    ],
    "Tamil Nadu": [
        "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem",
        "Vellore", "Tiruppur", "Thoothukudi", "Dindigul", "Kanchipuram",
        "Tirunelveli", "Karur", "Erode", "Vikramshila", "Pollachi",
        "Puducherry", "Nagercoil", "Ramanathapuram", "Tanjore", "Kumbakonam",
        "Virudhunagar", "Dharmapuri", "Perambalur", "Sivakasi", "Namakkal",
        "Cuddalore", "Arakkonam", "Nagapattinam", "Vellore", "Chidambaram",
        "Tiruvallur", "Hosur", "Bargur", "Chengalpattu", "Ranipet", 
    ],
    "Telangana": [
        "Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Ramagundam",
        "Khammam", "Mahbubnagar", "Mancherial", "Adilabad", "Miryalaguda",
        "Siddipet", "Jagtial", "Suryapet", "Nirmal", "Peddapalli",
        "Bhadrachalam", "Bhainsa", "Kothagudem", "Jagitial", "Wanaparthy",
        "Jangaon", "Nagarkurnool", "Medak", "Vikarabad", "Peddapalli",
    ],
    "Tripura": [
        "Agartala", "Udaipur", "Kailashahar", "Dharmanagar", "Khowai",
        "Sabroom", "Belonia", "Bishalgarh", "Jirania", "Melaghar",
        "Sonamura", "Amarpur", "Madhupur", "Gakulpur", "Bagma",
    ],
    "Uttar Pradesh": [
        "Lucknow", "Kanpur", "Varanasi", "Agra", "Meerut",
        "Allahabad", "Bareilly", "Ghaziabad", "Moradabad", "Aligarh",
        "Firozabad", "Mathura", "Shahjahanpur", "Rampur", "Saharanpur",
        "Muzaffarnagar", "Bijnor", "Jaunpur", "Raebareli", "Azamgarh",
        "Prayagraj", "Etawah", "Hapur", "Gorakhpur", "Sitapur",
        "Deoria", "Budaun", "Ballia", "Hardoi", "Amroha",
        "Basti", "Kushinagar", "Chandauli", "Jalaun", "Farrukhabad",
        "Sambhal", "Unnao", "Kanshiram Nagar", "Sonbhadra", "Shahabad",
        "Tanda", "Lakhimpur Kheri", "Mirzapur", "Pilibhit", "Raebareli",
    ],
    "Uttarakhand": [
        "Dehradun", "Haridwar", "Roorkee", "Nainital", "Haldwani",
        "Rudrapur", "Almora", "Kashipur", "Pithoragarh", "Bageshwar",
        "Kotdwar", "Champawat", "Ranikhet", "Bharatpur", "Mussoorie",
        "Khatima", "Dhanaulti", "Tehri", "Lohaghat", "Kedarnath",
    ],
    "West Bengal": [
        "Kolkata", "Howrah", "Asansol", "Durgapur", "Siliguri",
        "Darjeeling", "Hooghly", "Kharagpur", "Haldia", "Jalpaiguri",
        "Malda", "Raiganj", "Cooch Behar", "Medinipur", "Balurghat",
        "Alipurduar", "Suri", "Krishnanagar", "Tamluk", "Baharampur",
        "Chinsurah", "Rampurhat", "Santipur", "Kandi", "Bongaon",
        "Basirhat", "Habra", "Barrackpore", "Nabadwip", "Katwa",
        "Bolpur", "Uluberia", "Sainthia", "Jaynagar-Majilpur", "Budge Budge",
    ],
}



