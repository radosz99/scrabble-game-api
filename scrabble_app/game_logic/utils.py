def parse_letters_string_to_list(country, letters):
    letters = letters.upper()
    letters_list = []
    skip_next = False
    for index, letter in enumerate(letters):
        if skip_next:
            skip_next = False
            continue
        if country.name == "ES" and index < len(letters) - 1:
            letter, skip_next = check_if_contains_spanish_doubles(letters, index)
        letters_list.append(letter)
    return letters_list


def check_if_contains_spanish_doubles(word, index):
    word = word.upper()
    spanish_doubles = ['LL', 'RR', 'CH']
    if (double := word[index:index + 2]) in spanish_doubles:
        return double, True
    else:
        return word[index], False


def get_empty_board():
    return [[' ' for _ in range(15)] for _ in range(15)]


gb_letter_values = {
    "A": 1,
    "B": 3,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 4,
    "G": 2,
    "H": 4,
    "I": 1,
    "J": 8,
    "K": 5,
    "L": 1,
    "M": 3,
    "N": 1,
    "O": 1,
    "P": 3,
    "Q": 10,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 1,
    "V": 4,
    "W": 4,
    "X": 8,
    "Y": 4,
    "Z": 10
}

gb_legal_letters = [key for key in gb_letter_values.keys()] + [key.lower() for key in gb_letter_values.keys()]

pl_letter_values = {
    "A": 1,
    "Ą": 5,
    "B": 3,
    "C": 2,
    "Ć": 6,
    "D": 2,
    "E": 1,
    "Ę": 5,
    "F": 5,
    "G": 3,
    "H": 3,
    "I": 1,
    "J": 3,
    "K": 2,
    "L": 2,
    "Ł": 3,
    "M": 2,
    "N": 1,
    "Ń": 7,
    "O": 1,
    "Ó": 5,
    "P": 2,
    "R": 1,
    "S": 1,
    "Ś": 5,
    "T": 2,
    "U": 3,
    "W": 1,
    "Y": 2,
    "Z": 1,
    "Ź": 5,
    "Ż": 9
}

pl_legal_letters = [key for key in pl_letter_values.keys()] + [key.lower() for key in pl_letter_values.keys()]

es_letter_values = {
    "A": 1,
    "B": 3,
    "C": 3,
    "CH": 5,
    "D": 2,
    "E": 1,
    "F": 4,
    "G": 2,
    "H": 4,
    "I": 1,
    "J": 8,
    "L": 1,
    "LL": 8,
    "M": 3,
    "N": 1,
    "Ñ": 8,
    "O": 1,
    "P": 3,
    "Q": 5,
    "R": 1,
    "RR": 8,
    "S": 1,
    "T": 1,
    "U": 1,
    "V": 4,
    "X": 8,
    "Y": 4,
    "Z": 10
}

es_legal_letters = [key for key in es_letter_values.keys()] + [key.lower() for key in es_letter_values.keys()]

de_letter_values = {
    "A": 1,
    "Ä": 6,
    "B": 3,
    "C": 4,
    "D": 1,
    "E": 1,
    "F": 4,
    "G": 2,
    "H": 2,
    "I": 1,
    "J": 6,
    "K": 4,
    "L": 2,
    "M": 3,
    "N": 1,
    "O": 2,
    "Ö": 8,
    "P": 4,
    "Q": 10,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 1,
    "Ü": 6,
    "V": 6,
    "W": 3,
    "X": 8,
    "Y": 10,
    "Z": 3
}

de_legal_letters = [key for key in de_letter_values.keys()] + [key.lower() for key in de_letter_values.keys()]

fr_letter_values = {
    "A": 1,
    "B": 3,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 4,
    "G": 2,
    "H": 4,
    "I": 1,
    "J": 8,
    "K": 10,
    "L": 1,
    "M": 2,
    "N": 1,
    "O": 1,
    "P": 3,
    "Q": 8,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 1,
    "V": 4,
    "W": 10,
    "X": 10,
    "Y": 10,
    "Z": 10
}

fr_legal_letters = [key for key in fr_letter_values.keys()] + [key.lower() for key in fr_letter_values.keys()]

gb_occurrences = {
    "A": 9,
    "B": 2,
    "C": 2,
    "D": 4,
    "E": 12,
    "F": 2,
    "G": 3,
    "H": 2,
    "I": 9,
    "J": 1,
    "K": 1,
    "L": 4,
    "M": 2,
    "N": 6,
    "O": 8,
    "P": 2,
    "Q": 1,
    "R": 6,
    "S": 4,
    "T": 6,
    "U": 4,
    "V": 2,
    "W": 2,
    "X": 1,
    "Y": 2,
    "Z": 1
}

pl_occurrences = {
    "A": 9,
    "Ą": 1,
    "B": 2,
    "C": 3,
    "Ć": 1,
    "D": 3,
    "E": 7,
    "Ę": 1,
    "F": 1,
    "G": 2,
    "H": 2,
    "I": 8,
    "J": 2,
    "K": 3,
    "L": 3,
    "Ł": 2,
    "M": 3,
    "N": 5,
    "Ń": 1,
    "O": 6,
    "Ó": 1,
    "P": 3,
    "R": 4,
    "S": 4,
    "Ś": 1,
    "T": 3,
    "U": 2,
    "W": 4,
    "Y": 4,
    "Z": 5,
    "Ź": 1,
    "Ż": 1
}

es_occurrences = {
    "A": 12,
    "B": 2,
    "C": 4,
    "CH": 1,
    "D": 5,
    "E": 12,
    "F": 1,
    "G": 2,
    "H": 2,
    "I": 6,
    "J": 1,
    "L": 4,
    "LL": 1,
    "M": 2,
    "N": 5,
    "Ñ": 1,
    "O": 9,
    "P": 2,
    "Q": 1,
    "R": 5,
    "RR": 1,
    "S": 6,
    "T": 4,
    "U": 5,
    "V": 1,
    "X": 1,
    "Y": 1,
    "Z": 1
}

de_occurrences = {
    "A": 5,
    "Ä": 1,
    "B": 2,
    "C": 2,
    "D": 4,
    "E": 15,
    "F": 2,
    "G": 3,
    "H": 4,
    "I": 6,
    "J": 1,
    "K": 2,
    "L": 3,
    "M": 4,
    "N": 9,
    "O": 3,
    "Ö": 1,
    "P": 1,
    "Q": 1,
    "R": 6,
    "S": 7,
    "T": 6,
    "U": 6,
    "Ü": 1,
    "V": 1,
    "W": 1,
    "X": 1,
    "Y": 1,
    "Z": 1
}

fr_occurrences = {
    "A": 9,
    "B": 2,
    "C": 2,
    "D": 3,
    "E": 15,
    "F": 2,
    "G": 2,
    "H": 2,
    "I": 8,
    "J": 1,
    "K": 1,
    "L": 5,
    "M": 3,
    "N": 6,
    "O": 6,
    "P": 2,
    "Q": 1,
    "R": 6,
    "S": 6,
    "T": 6,
    "U": 6,
    "V": 2,
    "W": 1,
    "X": 1,
    "Y": 1,
    "Z": 1
}

occurrences = {
    "GB": gb_occurrences,
    "PL": pl_occurrences,
    "ES": es_occurrences,
    "DE": de_occurrences,
    "FR": fr_occurrences
}

letters_values = {
    "GB": gb_letter_values,
    "PL": pl_letter_values,
    "ES": es_letter_values,
    "DE": de_letter_values,
    "FR": fr_letter_values
}

legal_letters = {
    "GB": gb_legal_letters,
    "PL": pl_legal_letters,
    "ES": es_legal_letters,
    "DE": de_legal_letters,
    "FR": fr_legal_letters
}

word_multiplier = [[3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 3],
                   [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                   [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
                   [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
                   [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
                   [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
                   [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
                   [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
                   [3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 3]]

letter_multiplier = [[1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
                     [1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1],
                     [2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1],
                     [1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1],
                     [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
                     [1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1],
                     [1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2],
                     [1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1],
                     [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1]]
