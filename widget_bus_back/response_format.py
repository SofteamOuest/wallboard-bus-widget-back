def to_json_compatible_object(obj_list):
    return list(map(lambda obj: vars(obj), obj_list))
