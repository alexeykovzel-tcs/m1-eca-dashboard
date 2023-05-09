import json

ambulance_codes = ['b', 'a1', 'a2']
fire_alarm_codes = ['br 1', 'br 2', 'br 3', 'hv 1', 'hv 2', 'hv 3', 'hv 5']


# gets an emergency code by different pieces of prior information (heads)
def get_head_code(txt, heads, codes):
    for head in heads:
        code = None
        next_idx = len(head)

        # checks if the text starts with a head
        if txt.startswith(head) and txt[next_idx] in codes:
            code = txt[next_idx]

        # otherwise checks if the head is in the middle of the text
        else:
            mid_head = (' ' + head)
            next_idx = txt.find(mid_head)

            # returns the code found in the middle of the text
            if next_idx != -1:
                code = txt[next_idx + len(mid_head)]

        # returns the code found at the beginning of the text
        if code != None and code in codes:
            return code

    # if not found return None
    return None


# return an emergency code by tweet text
def get_emergency_code(txt):
    txt = txt.lower()
    emergency_codes = ambulance_codes + fire_alarm_codes

    # returns an emergency code if it was specifically stated in the text
    for code in emergency_codes:
        if txt.startswith(code + ' ') or (' ' + code + ' ') in txt:
            return code

    # identifies 'p 1', 'p 2', 'p 3' emergency codes
    prio_heads = ['prio ', 'prio: ', 'p ', 'p: ']
    prio_code = get_head_code(txt, prio_heads, ['1', '2', '3'])
    if prio_code != None:
        return 'p ' + prio_code

    # returns an ambulance code by assigned keywords
    ambu_keywords = ['ambu', 'letsel']
    for keyword in ambu_keywords:
        if keyword in txt:
            return 'amb'

    # returns a fire alarm code by assigned keywords
    fire_alarm_keywords = ['gebouwbrand']
    for keyword in fire_alarm_keywords:
        if keyword in txt:
            return 'br'

    # if an emergency code was not identified
    return 'u'  # undefined notation


# gets the priority of an emergency code
def get_emerg_code_priority(code):
    # retrieves the last code symbol
    last_chr  = code[-1]

    # returns the code priority according
    # to the last char element of an emergency code
    if last_chr == '1':
        return 'high'
    elif last_chr == '2':
        return 'normal'
    elif last_chr == '3':
        return 'low'
    else:
        return 'undefined'


# returns an emergency type by an emergency code
def get_emergency_type(code):
    if code in ambulance_codes or code == 'amb':
        return 'ambu'
    elif code in fire_alarm_codes or code == 'br':
        return 'firealarm'
    else:
        return 'undefined'


#  returns an element with the lowest value from dictionary
def get_outsider(dict):
    outsider = None

    for el in dict:
        if el != 'other':
            if outsider == None or dict[el] < dict[outsider]:
                outsider = el

    return outsider


#  returns a given number of elements from dictionary with largest values
def get_dict_top(top_num, dict):
    if top_num >= len(dict):
        return dict

    top = {'other': 0}

    # goes through each element in dictionary
    for el in dict:
        if top_num < len(top):
            # gets an outsider (element with the lowest value) from the top list
            outsider = get_outsider(top)

            # checks if an outsider is lower than a taken element 
            # in dictionary and if so is being replaced and taken into 'other'
            if top[outsider] <= dict[el]:
                top['other'] += top.pop(outsider)
                top[el] = dict[el]
            else:
                top['other'] += dict[el]

        else:
            top[el] = dict[el]

    return top
