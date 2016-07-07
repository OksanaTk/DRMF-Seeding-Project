import math_mode
import string
import re

def math_string(file):
    # Takes input file and returns list of strings when in math mode
    string = open(file).read()
    output = []
    ranges = math_mode.find_math_ranges(string)
    #print ranges
    for i in ranges:
        new = string[i[0]:i[1]]
        output.append(new)
    return output


def change_original(o_file, changed_math_string):
    # Places changed string from math mode back into place in the original function
    o_string = open(o_file).read()
    ranges = math_mode.find_math_ranges(o_string)
    num = 0
    edited = o_string
    for i in ranges:
        edited = string.replace(edited, o_string[i[0]:i[1]], changed_math_string[num])
        num += 1
    return edited


def formatting(file_str):
    # Proper spacing for the indexes and gets rid of all non beginEq endEq text

    updated = []
    IND_START = r'\index{'
    ind_str = ""
    in_ind = False
    previous = ""

    ranges = math_mode.find_math_ranges(file_str)
    bef_aft = file_str[:ranges[-1][1]+14]

    lines = bef_aft.split('\n')
    in_eq = False
    been_in_eq = False

    section = r'\\[a-zA-Z]*section'

    lines = bef_aft.split("\n")


    for line in lines:

        if 'begin{equation}' in line:
            in_eq = True
            been_in_eq = True

        if 'end{equation}' in line:
            updated.append(line)
            in_eq = False


        if in_eq:
            updated.append(line)

        else:
            if not been_in_eq:
                updated.append(line)
            elif '\\index' in line or re.match(section, line) or line == '':
                updated.append(line)


        # if this line is an index start storing it,or write it if we're done with the indexes
        if IND_START in line:
            in_ind = True
            ind_str += line + "\n"


        if in_ind:
            in_ind = False

            # add a preceding newline if one is not already present
            if previous.strip() != "":
                ind_str = "\n" + ind_str

            fullsplit = ind_str.split("\n")
            ind_str = ""

        previous = line


    wrote = "\n".join(updated)
    wrote = wrote + file_str[ranges[-1][1]+14:]


    # remove consecutive blank lines and blank lines between \index groups
    spaces_pat = re.compile(r'\n{2,}[ ]?\n+')
    wrote = spaces_pat.sub('\n\n', wrote)
    wrote = re.sub(r'\\index{(.*?)}\n\n\\index{(.*?)}', r'\\index{\1}\n\\index{\2}', wrote)

    return wrote

#formatting(open('/home/ont1/DLMF/25.ZE/newMoritz').read())