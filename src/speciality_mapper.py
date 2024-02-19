import pandas as pd

from utils import *

class Speciality_Mapper():
    def __init__(self,speciality,match_threshold = 80):
        self.search_term = remove_punct(remove_abbv(rephrase(speciality.strip().upper()))).strip()
        self.possible_taxonomy_codes_list = []
        self.taxonomy_mapper = pd.read_csv(r".\data\nucc_taxonomy_mapper.csv",dtype=str).fillna("")
        self.match_threshold = match_threshold

        needed_columns = ['Code','Display Name','Classification','Specialization']
        for col in needed_columns:
            if col not in self.taxonomy_mapper.columns:
                raise Exception(f"'{col}' column Missing in the Taxonomy Mapper File.")
        

        for col in needed_columns:
            self.taxonomy_mapper[col] = self.taxonomy_mapper[col].apply(lambda x: remove_punct(x.upper().strip()))

        
    def get_taxonomy_code_with_exact_match(self,search_term):
        
        search_term = search_term.upper().strip()

        if search_term=="":
            return []
        
        taxonomy = self.taxonomy_mapper
        
        
        """Checking if the search term is a Taxonomy Code"""
        info=taxonomy[taxonomy['Code']==search_term].drop_duplicates(subset=['Code']).reset_index(drop=True)
        if len(info) != 0:
            return [search_term]

        """Checking if the search term is a Display Name"""
        disp_name=set(taxonomy['Display Name'])
        if search_term in disp_name:
            data=taxonomy[taxonomy['Display Name'] == search_term].drop_duplicates().reset_index(drop=True)
            taxonomy_code = data.loc[0,'Code']
            return [taxonomy_code]
        
        """Checking if the search term is a Classfication (Parent) or Specialization (Child)"""
        classes=set(taxonomy['Classification'])
        specs=set(taxonomy['Specialization'])

        results = []
        if search_term in classes:
            data=taxonomy[taxonomy['Classification']==search_term].drop_duplicates().reset_index(drop=True)
            taxonomy_code = list(data['Code'])
            if search_term not in specs:
                return taxonomy_code
            else:
                results = results + taxonomy_code
        
        if search_term in specs:
            data=taxonomy[taxonomy['Specialization'] == search_term].drop_duplicates().reset_index(drop=True)
            taxonomy_code = list(data['Code'])
            results = results + taxonomy_code
                
        results = [i for i in results if i.strip()!=""]
        return results

    def get_taxonomy_code_with_fuzzy_match(self,search_term):
        
        search_term = search_term.upper().strip()

        if search_term=="":
            return []

        taxonomy = self.taxonomy_mapper

        """Checking for the best fuzzy match in Display Name"""
        disp_name=set(taxonomy['Display Name'])
        fuzzy_matched_strings = []
        max_score = self.match_threshold

        for spec in disp_name:
            spec=spec.strip()
            score=get_fuzz_score(search_term,spec)
            if score>max_score:
                fuzzy_matched_strings=[spec.upper()]
                max_score=score
            elif score==max_score:
                fuzzy_matched_strings.append(spec.upper())
        
        if len(fuzzy_matched_strings) != 0:
            return fuzzy_matched_strings
        
        """Checking for the best fuzzy match in Classification"""
        classes=set(taxonomy['Classification'])
        for spec in classes:
            score=get_fuzz_score(search_term,spec)
            if score>max_score:
                fuzzy_matched_strings=[spec.upper()]
                max_score=score
            elif score==max_score:
                fuzzy_matched_strings.append(spec.upper())

        if len(fuzzy_matched_strings) != 0:
            return fuzzy_matched_strings

        """Checking for the best fuzzy match in Specialization"""
        specs=set(taxonomy['Specialization'])
        for spec in specs:
            score=get_fuzz_score(search_term,spec)
            if score>max_score:
                fuzzy_matched_strings=[spec.upper()]
                max_score=score
            elif score==max_score:
                fuzzy_matched_strings.append(spec.upper())

        
        return fuzzy_matched_strings
    
    def standardise_from_taxonomy(self):
        search_term = self.search_term

        """Checking for exact match in the Taxonomy file"""
        taxonomy_codes = self.get_taxonomy_code_with_exact_match(search_term=search_term)

        if len(taxonomy_codes) != 0:
            self.possible_taxonomy_codes_list = taxonomy_codes
            return
        
        """Checking for fuzzy match in the Taxonomy file"""
        fuzzy_matched_strings = self.get_taxonomy_code_with_fuzzy_match(search_term=search_term)

        if len(fuzzy_matched_strings) != 0:
            taxonomy_codes = []
            print(fuzzy_matched_strings)
            for search_term in fuzzy_matched_strings:
                results = self.get_taxonomy_code_with_exact_match(search_term=search_term)
                print(search_term,results)
                taxonomy_codes += results
            
            taxonomy_codes = list(set(taxonomy_codes))
            self.possible_taxonomy_codes_list = [i for i in taxonomy_codes if i.strip()!=""]
            return 
        
        """Did not find a match for the term in the taxonomy file"""
        self.possible_taxonomy_codes_list = []
        return 

    def print_data(self):
        print(self.search_term)
        print(self.possible_taxonomy_codes_list)
    


spec = Speciality_Mapper("family Medicine addition medicine")
print("PRINT")
spec.print_data()
spec.standardise_from_taxonomy()
print("PRINT")
spec.print_data()

