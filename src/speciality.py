import pandas as pd
import numpy as np
import sys
import boto3
import configparser
import botocore
from io import StringIO
import fuzzywuzzy
from fuzzywuzzy import fuzz
import re
from tqdm import tqdm
import time
import requests

class Speciality_Mapper():

    def __init__(self,speciality):
        self.speciality = speciality
        self.parent = ""
        self.child = ""
        self.commonly_called_name = ""
        self.taxonomy_mapper = pd.read_csv(".\data\nucc_taxonomy_mapper.csv")

    def convert_taxonomy_to_display_name(self):
        if self.speciality.strip()=="":
            return ""
        
        if "Code" in self.taxonomy_mapper:
            info=self.taxonomy_mapper[self.taxonomy_mapper['Code']==self.speciality].drop_duplicates(subset=['Code']).reset_index(drop=True)
            if len(info) == 0:
                print("Taxonomy Code not present in the Taxonomy Mapper")
            else:
                self.commonly_called_name = list(info['Display Name'])[0]
                self.parent = list(info['Classification'])[0]
                self.child = list(info['Specialization'])[0]
        else:
            raise Exception("Code Column Missing in the Taxonomy Mapper File")
        return
    
    
        
    