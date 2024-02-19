import re
from fuzzywuzzy import fuzz

def remove_punct(text, exclusions="", replace_with=" "):
        """
        Remove punctuation from a given text, with optional exclusions and replacement.

        Parameters:
        - text: The input text from which punctuation needs to be removed.
        - exclusions: Characters that should be excluded from removal.
        - replace_with: The character to replace removed punctuation.

        Returns:
        - str: The text with punctuation removed.
        """
        # Define a set of default punctuation characters
        punctuations = "¯.,!™¥-♥#$%&:;\()+-<=>@[\\]^_`{|}~/¯( ͡° ͜ʖ ͡°) ͜ʖ° ͜ʖ ͡°ʖ ͡☉ ͡☉ ͡ ͡ ͡  ͡ ▌░╔╗║╔═╗├│Γû╝├▒»ΓÇÖ"

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


def get_fuzz_score(str1,str2):
    return 0.4*fuzz.token_sort_ratio(str1,str2)+0.6*fuzz.token_set_ratio(str1,str2)

def remove_abbv(x,update_cache = {}):
    abbrev={"MED":"MEDICINE","INT":"INTERNAL","PHYS":"PHYSICIAN","PRAC":"PRACTICE","CNTR":'CENTER','PSYCH':"PSYCHIATRY",
       "SURG":"SURGERY","RN":'REGISTERED NURSE',"RAD":"RADIOLOGY",'REHAB':"REHABILITATION","GYN":"GYNECOLOGY","LIC":'LICENSED',
       "INDEPEND":"INDEPENDENT","OTO":'OTOLARYNGOLOGY',"OB":"OBSTETRICS","ORTHO":"ORTHOPAEDIC","FAM":"FAMILY",
       "MRI":"MAGNETIC RESONANCE IMAGING","URO":"UROLOGY","EMERG":"EMERGENCY",'FAC':"FACIAL","PREV":"PREVENTIVE",
       "CERT":"CERTIFIED","CLIN":"CLINICAL","OCCU":"OCCUPATIONAL","ADV":"ADVANCED","LPCC":'LICENSED PROFESSIONAL CLINICAL COUNSELORS',
       "PED":"PEDIATRICS","PEDS":"PEDIATRICS","CTR":"CENTER","BEHAV":"BEHAVIOR","CRNA":'CERTIFIED REGISTERED NURSE ANESTHETISTS',
       "CHIRO":"CHIROPRACTOR","SLP":"SPEECH LANGUAGE PATHOLOGY","ADHD":"ATTENTION DEFICIT HYPERACTIVITY DISORDER",
       'LCSW':"LICENSED CLINICAL SOCIAL WORKER","ESRD":'END STAGE RENAL DISEASE',"RECON":"RECONSTRUCTIVE","PT":"PHYSICAL THERAPIST",
       "TRMT":"TREATMENT","CNSLR":"COUNSELOR","DERM":"DERMATOPATHOLOGY","TMS":"TRANSCRANIAL MAGNETIC STIMULATION","TREA":"TREATMENT",
       "CEAP":"CERTIFIED EMPLOYEE ASSISTANCE PROFESSIONAL",'DIAG':"DIAGNOSTIC","SPEC":'SPECIALIST',"REG":"REGISTERED","DME":"DURABLE MEDICAL EQUIPMENT",
       "RESID":"RESIDENTIAL",'OT':"OCCUPATIONAL THERAPY","DEV":"DEVELOPMENTAL","MGMT":"MANAGEMENT","GEN":"GENERAL",
       "SPCL":"SPECIAL",'HOSP':"HOSPITAL","ENDOC":"ENDOCRINOLOGY","VASC":"VASCULAR","PRO":"PROFESSIONAL"}
    
    abbrev.update(update_cache) ### VALIDATE IF ALL ARE CAPS

    removals=["PCP","BCBA ","HSPP"]
    x=remove_punct(x.upper().strip().replace(" AND "," & "))
    new_list=[]
    for word in x.split():
        if word in removals:
            continue
        if word in abbrev:
            replace_term=abbrev[word]
            if replace_term in x or get_fuzz_score(replace_term,x)>=90:
                continue
            else:
                new_list.append(replace_term)
        else:
            new_list.append(word)
    return " ".join(new_list)
remove_abbv('CRNA CERTIFIED REGISTERED NURSE ANESTHETIST')