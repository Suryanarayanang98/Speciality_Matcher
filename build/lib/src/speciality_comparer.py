#speciality_comparer.py

"""
speciality_comparer Module:

        speciality_comparer:
        A function to compare two medical specialties and find the intersection of their taxonomy codes.

        Parameters:
            speciality1 (str): The first medical specialty.
            speciality2 (str): The second medical specialty.

        Returns:
            str: A message indicating whether there is a match or not.
            
Example:

    match_status = speciality_comparer("family Medicine", "Internal Medicine")
    print(match_status)

"""

from src.speciality_mapper import Speciality_Mapper

def speciality_comparer(speciality1, speciality2):
    """
    Compares two medical specialties and finds the intersection of their taxonomy codes.

    Parameters:
        speciality1 (str): The first medical specialty.
        speciality2 (str): The second medical specialty.

    Returns:
        str: A message indicating whether there is a match or not.
    """
    spec1 = Speciality_Mapper(speciality1)
    spec2 = Speciality_Mapper(speciality2)

    spec1.standardise_from_taxonomy()
    spec2.standardise_from_taxonomy()

    intersection = set(spec1.possible_taxonomy_codes_list).intersection(set(spec2.possible_taxonomy_codes_list))

    if len(intersection) != 0:
        return "Match"

    # Code to check if there are any speciality and a subspeciality is being compared
    for taxonomy_code_1 in spec1.possible_taxonomy_codes_list:
        if taxonomy_code_1[4:-1] == "0"*5:
            for taxonomy_code_2 in spec2.possible_taxonomy_codes_list:
                if taxonomy_code_2[:4] == taxonomy_code_1[:4]:
                    return "Match"

    return "No Match"
        

if __name__ == "__main__":
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