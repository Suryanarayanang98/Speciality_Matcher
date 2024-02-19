# speciality_mapper.py

"""
Speciality Mapper Module

This module provides a Python tool for mapping medical specialties to their corresponding taxonomy codes. It includes a class, Speciality_Mapper, which offers various methods for standardizing medical specialty names and retrieving associated taxonomy codes.

The tool employs both exact matching and fuzzy matching techniques to accurately map specialties to taxonomy codes. It utilizes a provided taxonomy mapping file to perform these mappings.

Classes:
    Speciality_Mapper:
        A class for mapping medical specialties to taxonomy codes.

        Attributes:
            speciality (str): The medical specialty to be mapped.
            match_threshold (int): The threshold for fuzzy matching similarity (default is 80).
            search_term (str): The standardized version of the input medical specialty.
            possible_taxonomy_codes_list (list): List of possible taxonomy codes for the input specialty.
            taxonomy_mapper (DataFrame): DataFrame containing the taxonomy mapping data.

        Methods:
            __init__(speciality, match_threshold=80):
                Initializes the Speciality_Mapper object with the given specialty and match threshold.
            get_taxonomy_code_with_exact_match(search_term):
                Retrieves taxonomy codes with exact matches for the given search term.
            get_taxonomy_code_with_fuzzy_match(search_term):
                Retrieves taxonomy codes with fuzzy matches for the given search term.
            standardise_from_taxonomy():
                Standardizes the input specialty and retrieves associated taxonomy codes.
            print_data():
                Prints the standardized specialty and associated taxonomy codes.


Usage:
    To use this module, import it into your Python script and create an instance of the Speciality_Mapper class with the medical specialty to be mapped. Then, call the necessary methods to perform the mapping.

Example:
    spec = Speciality_Mapper("family Medicine addition medicine")
    spec.standardise_from_taxonomy()
    spec.print_data()

    match_status = speciality_comparer("family Medicine", "Internal Medicine")
    print(match_status)

"""

import pandas as pd
import os

from utils import *

class Speciality_Mapper:
    """
    A class to map medical specialties to their corresponding taxonomy codes.

    Attributes:
        speciality (str): The medical specialty to be mapped.
        match_threshold (int): The threshold for fuzzy matching similarity (default is 80).
        search_term (str): The standardized version of the input medical specialty.
        possible_taxonomy_codes_list (list): List of possible taxonomy codes for the input specialty.
        taxonomy_mapper (DataFrame): DataFrame containing the taxonomy mapping data.

    Methods:
        __init__(speciality, match_threshold=80):
            Initializes the Speciality_Mapper object with the given specialty and match threshold.
        get_taxonomy_code_with_exact_match(search_term):
            Retrieves taxonomy codes with exact matches for the given search term.
        get_taxonomy_code_with_fuzzy_match(search_term):
            Retrieves taxonomy codes with fuzzy matches for the given search term.
        standardise_from_taxonomy():
            Standardizes the input specialty and retrieves associated taxonomy codes.
        print_data():
            Prints the standardized specialty and associated taxonomy codes.
    """

    def __init__(self, speciality, match_threshold=80):
        """
        Initializes the Speciality_Mapper object.

        Parameters:
            speciality (str): The medical specialty to be mapped.
            match_threshold (int): The threshold for fuzzy matching similarity (default is 80).
        """
        self.speciality = speciality
        self.match_threshold = match_threshold
        self.search_term = remove_punct(remove_abbv(rephrase(speciality.strip().upper()))).strip()
        self.possible_taxonomy_codes_list = []
        self.load_taxonomy_mapper()

    def load_taxonomy_mapper(self):
        data_dir = os.path.join(".", 'data')
        csv_file = os.path.join(data_dir, 'nucc_taxonomy_mapper.csv')
        print(csv_file)
        self.taxonomy_mapper = pd.read_csv(csv_file, dtype=str).fillna("")


        needed_columns = ['Code', 'Display Name', 'Classification', 'Specialization']
        for col in needed_columns:
            if col not in self.taxonomy_mapper.columns:
                raise Exception(f"'{col}' column Missing in the Taxonomy Mapper File.")

        for col in needed_columns:
            self.taxonomy_mapper[col] = self.taxonomy_mapper[col].apply(lambda x: remove_punct(x.upper().strip()))

    def get_taxonomy_code_with_exact_match(self, search_term):
        """
        Retrieves taxonomy codes with exact matches for the given search term.

        Parameters:
            search_term (str): The search term to be matched.

        Returns:
            list: List of taxonomy codes with exact matches.
        """
        search_term = search_term.upper().strip()

        if search_term == "":
            return []

        taxonomy = self.taxonomy_mapper

        info = taxonomy[taxonomy['Code'] == search_term].drop_duplicates(subset=['Code']).reset_index(drop=True)
        if len(info) != 0:
            return [search_term]

        disp_name = set(taxonomy['Display Name'])
        if search_term in disp_name:
            data = taxonomy[taxonomy['Display Name'] == search_term].drop_duplicates().reset_index(drop=True)
            taxonomy_code = data.loc[0, 'Code']
            return [taxonomy_code]

        classes = set(taxonomy['Classification'])
        specs = set(taxonomy['Specialization'])

        results = []
        if search_term in classes:
            data = taxonomy[taxonomy['Classification'] == search_term].drop_duplicates().reset_index(drop=True)
            taxonomy_code = list(data['Code'])
            if search_term not in specs:
                return taxonomy_code
            else:
                results = results + taxonomy_code

        if search_term in specs:
            data = taxonomy[taxonomy['Specialization'] == search_term].drop_duplicates().reset_index(drop=True)
            taxonomy_code = list(data['Code'])
            results = results + taxonomy_code

        results = [i for i in results if i.strip() != ""]
        return results

    def get_taxonomy_code_with_fuzzy_match(self, search_term):
        """
        Retrieves taxonomy codes with fuzzy matches for the given search term.

        Parameters:
            search_term (str): The search term to be matched.

        Returns:
            list: List of taxonomy codes with fuzzy matches.
        """
        search_term = search_term.upper().strip()

        if search_term == "":
            return []

        taxonomy = self.taxonomy_mapper

        disp_name = set(taxonomy['Display Name'])
        fuzzy_matched_strings = []
        max_score = self.match_threshold

        for spec in disp_name:
            spec = spec.strip()
            score = get_fuzz_score(search_term, spec)
            if score > max_score:
                fuzzy_matched_strings = [spec.upper()]
                max_score = score
            elif score == max_score:
                fuzzy_matched_strings.append(spec.upper())

        if len(fuzzy_matched_strings) != 0:
            return fuzzy_matched_strings

        classes = set(taxonomy['Classification'])
        for spec in classes:
            score = get_fuzz_score(search_term, spec)
            if score > max_score:
                fuzzy_matched_strings = [spec.upper()]
                max_score = score
            elif score == max_score:
                fuzzy_matched_strings.append(spec.upper())

        if len(fuzzy_matched_strings) != 0:
            return fuzzy_matched_strings

        specs = set(taxonomy['Specialization'])
        for spec in specs:
            score = get_fuzz_score(search_term, spec)
            if score > max_score:
                fuzzy_matched_strings = [spec.upper()]
                max_score = score
            elif score == max_score:
                fuzzy_matched_strings.append(spec.upper())

        return fuzzy_matched_strings

    def standardise_from_taxonomy(self):
        """
        Standardizes the input specialty and retrieves associated taxonomy codes.
        """
        search_term = self.search_term

        taxonomy_codes = self.get_taxonomy_code_with_exact_match(search_term=search_term)

        if len(taxonomy_codes) != 0:
            self.possible_taxonomy_codes_list = taxonomy_codes
            return

        fuzzy_matched_strings = self.get_taxonomy_code_with_fuzzy_match(search_term=search_term)

        if len(fuzzy_matched_strings) != 0:
            taxonomy_codes = []
            for search_term in fuzzy_matched_strings:
                results = self.get_taxonomy_code_with_exact_match(search_term=search_term)
                taxonomy_codes += results

            taxonomy_codes = list(set(taxonomy_codes))
            self.possible_taxonomy_codes_list = [i for i in taxonomy_codes if i.strip() != ""]
            return

        self.possible_taxonomy_codes_list = []

    def print_data(self):
        """
        Prints the standardized specialty and associated taxonomy codes.
        """
        print(self.search_term)
        print(self.possible_taxonomy_codes_list)

if __name__ == "__main__":
    spec = Speciality_Mapper("family Medicine addition medicine")
    spec.standardise_from_taxonomy()
    spec.print_data()
