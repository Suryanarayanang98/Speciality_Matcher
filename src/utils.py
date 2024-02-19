#utils.py

"""
Text Processing Module

This module provides various text processing utilities for standardizing medical specialty names and removing punctuation from text.

Functions:
    remove_punct(text, exclusions="", replace_with=" "):
        Remove punctuation from a given text, with optional exclusions and replacement.
    
    get_fuzz_score(str1, str2):
        Calculate a fuzzy matching score between two strings.
    
    remove_abbv(x, update_cache={}):
        Remove abbreviations from a given text.
    
    rephrase(x):
        Rephrase medical specialty names to standardize them.

Usage:
    The functions provided in this module can be used to preprocess text data related to medical specialties before mapping them to taxonomy codes. 
    These functions are particularly useful for cleaning and standardizing medical specialty names obtained from various sources.

Example:
    Cleaned_Text = remove_punct("Family Medicine & Addition Medicine", exclusions="&")
    print(Cleaned_Text)
    # Output: "Family Medicine  Addition Medicine"

    Score = get_fuzz_score("Family Medicine", "Internal Medicine")
    print(Score)
    # Output: 90.0

    Standardized_Text = remove_abbv("PCP & CNTR in Psychology")
    print(Standardized_Text)
    # Output: "PRIMARY CARE PHYSICIAN & CENTER in PSYCHOLOGY"

    Rephrased_Text = rephrase("Neurosurgery")
    print(Rephrased_Text)
    # Output: "Neurological Surgery"
"""

import re
from fuzzywuzzy import fuzz

def remove_punct(text, exclusions="", replace_with=" "):
    """
    Remove punctuation from a given text, with optional exclusions and replacement.

    Parameters:
        text (str): The input text from which punctuation needs to be removed.
        exclusions (str): Characters that should be excluded from removal.
        replace_with (str): The character to replace removed punctuation.

    Returns:
        str: The text with punctuation removed.
    """

    # Define a set of default punctuation characters
    punctuations = "¯.,!™¥-♥#$%&:;()+-<=>@[\\]^_`{|}~/¯( ͡° ͜ʖ ͡°) ͜ʖ° ͜ʖ ͡°ʖ ͡☉ ͡☉ ͡ ͡ ͡  ͡ ▌░╔╗║╔═╗├│Γû╝├▒»ΓÇÖ"

    # Remove characters in exclusions from the default set of punctuation
    for ex in exclusions:
        punctuations = punctuations.replace(ex, "")

    # Replace each punctuation character with the specified replacement character
    for p in punctuations:
        text = text.replace(p, replace_with)

    # Replace specific characters and clean additional whitespace
    text = (
        text.replace('"', " ")
        .replace("'S", " ")
        .replace("'", " ")
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("\t", " ")
        .replace("\\n", " ")
        .replace("\\r", " ")
        .replace("\\t", " ")
    )

    try:
        # Use regular expression to replace multiple consecutive whitespaces with a single space
        text = re.sub(r"\s+", " ", text)
    except:
        pass

    return text

def get_fuzz_score(str1, str2):
    """
    Calculate a fuzzy matching score between two strings.

    Parameters:
        str1 (str): The first string.
        str2 (str): The second string.

    Returns:
        float: The fuzzy matching score between the two strings.
    """
    score = 0.2 * fuzz.token_sort_ratio(str1, str2) + 0.8 * fuzz.token_set_ratio(str1, str2) - 5 * abs(
        len(str1.split()) - len(str2.split())
    ) / (len(str1.split()) + len(str2.split()))
    return score

def remove_abbv(x, update_cache={}):
    """
    Remove abbreviations from a given text.

    Parameters:
        x (str): The input text containing abbreviations.
        update_cache (dict): Dictionary containing additional abbreviations to update the cache.

    Returns:
        str: The text with abbreviations replaced by their full forms.
    """
    abbrev = {
        "MED": "MEDICINE", "INT": "INTERNAL", "PHYS": "PHYSICIAN", "PRAC": "PRACTICE", "CNTR": "CENTER",
        "PSYCH": "PSYCHIATRY", "SURG": "SURGERY", "RN": "REGISTERED NURSE", "RAD": "RADIOLOGY", "REHAB": "REHABILITATION",
        "GYN": "GYNECOLOGY", "LIC": "LICENSED", "INDEPEND": "INDEPENDENT", "OTO": "OTOLARYNGOLOGY", "OB": "OBSTETRICS",
        "ORTHO": "ORTHOPAEDIC", "FAM": "FAMILY", "MRI": "MAGNETIC RESONANCE IMAGING", "URO": "UROLOGY", "EMERG": "EMERGENCY",
        "FAC": "FACIAL", "PREV": "PREVENTIVE", "CERT": "CERTIFIED", "CLIN": "CLINICAL", "OCCU": "OCCUPATIONAL",
        "ADV": "ADVANCED", "LPCC": "LICENSED PROFESSIONAL CLINICAL COUNSELORS", "PED": "PEDIATRICS", "PEDS": "PEDIATRICS",
        "CTR": "CENTER", "BEHAV": "BEHAVIOR", "CRNA": "CERTIFIED REGISTERED NURSE ANESTHETISTS", "CHIRO": "CHIROPRACTOR",
        "SLP": "SPEECH LANGUAGE PATHOLOGY", "ADHD": "ATTENTION DEFICIT HYPERACTIVITY DISORDER", "LCSW": "LICENSED CLINICAL SOCIAL WORKER",
        "ESRD": "END STAGE RENAL DISEASE", "RECON": "RECONSTRUCTIVE", "PT": "PHYSICAL THERAPIST", "TRMT": "TREATMENT", "CNSLR": "COUNSELOR",
        "DERM": "DERMATOPATHOLOGY", "TMS": "TRANSCRANIAL MAGNETIC STIMULATION", "TREA": "TREATMENT", "CEAP": "CERTIFIED EMPLOYEE ASSISTANCE PROFESSIONAL",
        "DIAG": "DIAGNOSTIC", "SPEC": "SPECIALIST", "REG": "REGISTERED", "DME": "DURABLE MEDICAL EQUIPMENT", "RESID": "RESIDENTIAL",
        "OT": "OCCUPATIONAL THERAPY", "DEV": "DEVELOPMENTAL", "MGMT": "MANAGEMENT", "GEN": "GENERAL", "SPCL": "SPECIAL", "HOSP": "HOSPITAL",
        "ENDOC": "ENDOCRINOLOGY", "VASC": "VASCULAR", "PRO": "PROFESSIONAL",
    }

    abbrev.update(update_cache)

    removals = ["PCP", "BCBA ", "HSPP"]
    x = remove_punct(x.upper().strip().replace(" AND ", " & "))
    new_list = []
    for word in x.split():
        if word in removals:
            continue
        if word in abbrev:
            replace_term = abbrev[word]
            if replace_term in x or get_fuzz_score(replace_term, x) >= 90:
                continue
            else:
                new_list.append(replace_term)
        else:
            new_list.append(word)
    return " ".join(new_list)

def rephrase(x):
    """
    Rephrase medical specialty names to standardize them.

    Parameters:
        x (str): The input medical specialty name.

    Returns:
        str: The standardized medical specialty name.
    """
    modifications_dict = {
        "General Dentistry": "Dentist", "Neurosurgery": "Neurological Surgery", "Endocrinology": "Endocrinology, Diabetes & Metabolism",
        "Psychology": "Psychologist", "General Surgery": "Surgery", "Hematology/Oncology": "Hematology & Oncology", "Podiatry": "Podiatrist",
        "Audiology": "Audiologist", "Orthodontics": "Orthodontics and Dentofacial Orthopedics", "Cardiology": "Interventional Cardiology",
        "PULMONARY MEDICINE": "PULMONARY DISEASE", "ORAL SURGERY": "ORAL & MAXILLOFACIAL SURGERY", "NEUROTOLOGY": "Otology & Neurotology",
        "CHIROPRACTIC MEDICINE": "CHIROPRACTOR", "PHYSICAL MEDICINE & REHAB": "PHYSICAL MEDICINE & REHABILITATION",
        "CARDIOTHORACIC SURGERY": "Thoracic Surgery (Cardiothoracic Vascular Surgery)", "ACUPUNCTURE SERVICES": "ACUPUNCTURIST", "OPTOMETRY": "OPTOMETRIST",
        "CARDIAC SURGERY": "Vascular Surgery", "family practice": "Family Medicine", "PSYCHOLOGY PHD": "Psychologist",
        "MARRIAGE FAMILY FOCUS": "MARRIAGE & FAMILY THERAPIST", "OB GYN": "OBSTETRICS & GYNECOLOGY", "WOMEN'S ISSUES": "WOMEN'S HEALTH",
        "MASTER'S LEVEL NURSE": "REGISTERED NURSE", "DIALECTIC BEHAVIORAL THERAPY": "BEHAVIOR ANALYST", "CRNA ANESTHETIST": "ANESTHESIOLOGY",
        "APPLIED BEHAVIORAL ANALYSIS": "BEHAVIOR ANALYST", "FAMILY PRACTICE SPECIALIST": "FAMILY MEDICINE", "PSYCHOLOGY HSPP": "Psychologist",
        "THORACIC CARDIOVASCULAR SURGERY": "Thoracic Surgery (Cardiothoracic Vascular Surgery)", "MATERNAL & FETAL MED PERINATOLOGY": "MATERNAL & FETAL MEDICINE",
        "SURGERY THORACIC CARDIOVASCULAR": "Thoracic Surgery (Cardiothoracic Vascular Surgery)",
        "FEMALE PELVIC & RECON SURG": "FEMALE PELVIC MEDICINE & RECONSTRUCTIVE SURGERY",
        "ADDICTION MEDICINE INT MED": "ADDICTION MEDICINE (INTERNAL MEDICINE) PHYSICIAN",
    }

    target = x.upper().strip()
    for mods in modifications_dict.keys():
        if target == mods.upper().strip():
            return modifications_dict[mods].upper().strip()
    return x
