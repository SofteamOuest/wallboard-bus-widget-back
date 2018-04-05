def to_json_compatible_object(obj_list):
    return [vars(obj) for obj in obj_list]
