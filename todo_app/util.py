

def join_lists_of_dicts(main_list, joining_list, join_key):
    """
    This function performs left outer join between two given lists based on the common field in both lists `join_key`.
    `main_list` is updated to include all other fields from `joining_list` for every matching dict between the two lists.
    """
    for row in main_list:
        join_value = row[join_key]
        joining_row = find_dict_in_list(joining_list, join_key, join_value)
        row.update(joining_row)
    return main_list


def change_key_in_list_of_dicts(list, old_key, new_key):
    for row in list:
        if old_key in row:
            row[new_key] = row.pop(old_key)
    return list


def find_dict_in_list(list, key, value):
    found_item = next((item for item in list if item[key] == value), None)
    return found_item
