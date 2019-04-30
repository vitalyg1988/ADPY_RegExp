import re
import csv
from pprint import pprint

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
header = contacts_list.pop(0)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код


def normalize_name(name_string):
    return name_string.replace(',', ' ', ).split(' ')[: 3]


def normalize_phone(phone_string):
    pattern = r'(8|\+7)\s*\(?(\d{3})\)?[-|\s*]?(\d{3})[-|\s*]?(\d{2})[-|\s*]?(\d{2})((\s*)\(?(доб.)\s*(\d+)\)?)?'
    new_pattern = r'+7(\2)\3-\4-\5\7\8\9'
    return re.sub(pattern, new_pattern, phone_string)


contact_dict = {}
for item in contacts_list:
    name = tuple(normalize_name(','.join(item[0: 3])))
    temp_dict = {
        header[3]: '',
        header[4]: '',
        header[5]: '',
        header[6]: ''
    }
    contact_dict.setdefault(name, temp_dict)
    contact_dict[name][header[3]] = contact_dict[name][header[3]] if contact_dict[name][header[3]] else item[3]
    contact_dict[name][header[4]] = contact_dict[name][header[4]] if contact_dict[name][header[4]] else item[4]
    contact_dict[name][header[5]] = contact_dict[name][header[5]] if contact_dict[name][header[5]] else \
        normalize_phone(item[5])
    contact_dict[name][header[6]] = contact_dict[name][header[6]] if contact_dict[name][header[6]] else item[6]

new_contact_dict = {}
for first_contact in contact_dict:
    if '' in first_contact:
        for second_contact in contact_dict:
            if first_contact[0] == second_contact[0] and '' not in second_contact:
                for contact_info in contact_dict[first_contact]:
                    if contact_dict[first_contact][contact_info]:
                        contact_dict[second_contact][contact_info] = contact_dict[first_contact][contact_info]
                new_contact_dict = contact_dict.copy()
                del new_contact_dict[first_contact]


phonebook_list = [[*key, new_contact_dict[key][header[3]], new_contact_dict[key][header[4]],
                 new_contact_dict[key][header[5]], new_contact_dict[key][header[6]]] for key in new_contact_dict]
phonebook_list.insert(0, header)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(phonebook_list)
