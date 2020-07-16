def parse_last_name(username):
    res = username.split(":")
    return res[0]

def parse_first_name(username):
    res = username.split(":")
    if len(res)<2:
        return res[0]
    else:
        return res[1]

def create_username(first_name, last_name):
    return f'{first_name}:{last_name}'