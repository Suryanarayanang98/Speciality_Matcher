import pandas as pd

from src.utils import *

class Speciality_Mapper():
    def __init__(self,speciality):
        self.search_term = speciality.strip().upper()
        self.possible_taxonomy_codes_list = []
        self.taxonomy_mapper = pd.read_csv(".\data\nucc_taxonomy_mapper.csv")

        needed_columns = ['Code','Display Name','Classification','Specialization']
        for col in needed_columns:
            if col not in self.taxonomy_mapper.columns:
                raise Exception(f"'{col}' column Missing in the Taxonomy Mapper File.")
        
        self.search_term = remove_punct(self.search_term).upper().strip()

        for col in self.taxonomy_mapper.columns:
            self.taxonomy_mapper[col] = self.taxonomy_mapper[col].apply(lambda x: remove_punct(x).upper().strip())

        
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
        max_score=-1
        for spec in disp_name:
            spec=spec.strip()
            score=get_fuzz_score(search_term,spec)
            if score>max_score:
                fuzzy_matched_strings=[spec.upper()]
                max_score=score
            elif score==max_score:
                fuzzy_matched_strings.append(spec.upper())
        
        """Checking for the best fuzzy match in Specialization"""
        specs=set(taxonomy['Specialization'])
        for spec in specs:
            score=get_fuzz_score(search_term,spec)
            if score>max_score:
                fuzzy_matched_strings=[spec.upper()]
                max_score=score
            elif score==max_score:
                fuzzy_matched_strings.append(spec.upper())

        """Checking for the best fuzzy match in Classification"""
        classes=set(taxonomy['Classification'])
        for spec in classes:
            score=get_fuzz_score(search_term,spec)
            if score>max_score:
                fuzzy_matched_strings=[spec.upper()]
                max_score=score
            elif score==max_score:
                fuzzy_matched_strings.append(spec.upper())
        
        return fuzzy_matched_strings
    
    def 

spec = Speciality_Mapper("Additiction Medicine")