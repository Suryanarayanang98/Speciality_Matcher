# Medical Speciality Mapper


The Speciality Mapper is a Python tool aimed at providing accurate mapping of medical specialties to their corresponding taxonomy codes. This tool offers a robust set of features tailored to meet the diverse needs of healthcare professionals and researchers.


## Key Features

- **Exact Match**: The Speciality Mapper utilizes advanced algorithms to precisely match input medical specialties with exact entries in the provided taxonomy file. This ensures reliable and consistent mappings for a wide range of medical disciplines.

- **Fuzzy Match**: In scenarios where an exact match cannot be found, the tool employs sophisticated fuzzy matching techniques to identify closely related specialties based on user-defined similarity thresholds. This enables the system to handle variations and nuances in specialty names with high accuracy.

- **Taxonomy Code Retrieval**: Once a match is established, the Speciality Mapper retrieves the corresponding taxonomy codes associated with the mapped specialties. This facilitates seamless integration with existing healthcare databases and systems, streamlining data management processes.

- **Data Standardization**: By standardizing medical specialty names according to the entries in the taxonomy file, the tool ensures consistency and coherence in data representation. This promotes interoperability and enhances the reliability of downstream analyses and reporting.

- **Speciality Comparison**: The tool provides functionality to compare the taxonomy codes of two different medical specialties. This can be achieved by creating an instance of the `Speciality_Mapper` class for each specialty, standardizing them to obtain their respective taxonomy codes, and then checking for the intersection of the taxonomy codes.
This is done automatically in the speciality_comparer module, but if you want any custom logic, please go ahead with the object and write custom logics.

## Getting Started



### Usage

1. Import the Speciality_Mapper class from the speciality_mapper.py file: 
    ```python
    from speciality_matcher.speciality_mapper import Speciality_Mapper


2. Create an instance of Speciality_Mapper with the medical specialty as input:
     ```python
     spec_mapper = Speciality_Mapper("Medical Specialty")

3. Use the standardise_from_taxonomy() method to standardize the input specialty and retrieve associated taxonomy codes:
    ```python
    spec_mapper.standardise_from_taxonomy()

4. Access the standardized specialty and associated taxonomy codes:
    ```python
    print("Standardized Specialty:", spec_mapper.search_term)
    print("Associated Taxonomy Codes:", spec_mapper.possible_taxonomy_codes_list)

5. For comparing two medical specialities, you can use the speciality_comparer module:
    ```python
    from speciality_matcher.speciality_comparer import speciality_comparer
    
    # Example 1
    speciality1, speciality2 = "Internal Medicine", "Family Medicine"
    print(speciality1, speciality2,speciality_comparer(speciality1, speciality2))

    # Example 2
    speciality1, speciality2 = "Addiction Medicine Internal Medicine Physician", "Addiction Medicine Family Medicine Physician"
    print(speciality1, speciality2,speciality_comparer(speciality1, speciality2))

    # Example 3
    speciality1, speciality2 = "Addiction Medicine", "Internal Medicine"
    print(speciality1, speciality2,speciality_comparer(speciality1, speciality2))

    # Example 4
    speciality1, speciality2 = "General Dentist", "ORAL & MAXILLOFACIAL PATHOLOGY"
    print(speciality1, speciality2,speciality_comparer(speciality1, speciality2))

Note: The speciality_comparer will match even if one speciality is the parent of the another one.



