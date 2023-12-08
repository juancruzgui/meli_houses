
def swap_quotation_marks(string):
    #swap all the " for '
    temp_char = "##|##"

    temp_replaced = string.replace('"',temp_char)

    replacement = temp_replaced.replace("'", '"')

    result = replacement.replace(temp_char, "'")

    return result
