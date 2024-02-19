#main.py

"""
Main Module:

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

from speciality_mapper import Speciality_Mapper


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

    if len(intersection) == 0:
        return "No Match"
    return "Match"

