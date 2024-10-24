from pprint import pprint
import csv
import re
from collections import defaultdict


phone_pattern = re.compile(r"(\+7|8)?[\s\(]*(\d{3})[\)\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*доб\.*\s*(\d+))?")

def format_phone(phone):
    match = phone_pattern.search(phone)
    if match:
        phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(7):
            phone += f" доб.{match.group(7)}"
    return phone

def merge_contacts(contacts):
    merged_contacts = defaultdict(dict)
    for contact in contacts:
        lastname, firstname, surname = contact[0], contact[1], contact[2]
        key = f"{lastname} {firstname} {surname}".strip()
        
        for i, field in enumerate(contact):
            if field:
                merged_contacts[key][i] = field
    result = []
    for key, fields in merged_contacts.items():
        result.append([fields.get(i, "") for i in range(7)])
    return result

def process_phonebook(input_file, output_file):
    with open(input_file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        pprint(contacts_list)        

    for contact in contacts_list:
        fullname = " ".join(contact[:3]).split()  
        contact[:3] = (fullname + [""])[:3] 

    for contact in contacts_list:
        contact[5] = format_phone(contact[5])

    contacts_list = merge_contacts(contacts_list)

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

process_phonebook("phonebook_raw.csv", "phonebook_result.csv")
