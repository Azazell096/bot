def telNumber(s):
    s = s.replace('-', '')
    if len(s) == 12:
        s = s[2:]
    elif len(s) == 11:
        s = s[1:]
    return s

