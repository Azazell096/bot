tel=["89280301600","9280301600","+79280301600","79280301600","7-928-030-16-00"]
for s in tel:

    s=s.replace('-', '')
    if len(s)==12:
        s=s[2:]
    elif len(s)==11:
        s=s[1:]
    print(s)