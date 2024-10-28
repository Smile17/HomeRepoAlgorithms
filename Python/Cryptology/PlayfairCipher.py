n = 8
k = 4

def create_playfair_matrix(key):
    matrix = []
    alphabet = "АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    used = set()
    for char in key:
        if char not in used:
            matrix.append(char)
            used.add(char)
    for char in alphabet:
        if char not in used:
            matrix.append(char)
    
    return [matrix[i:i+n] for i in range(0, len(alphabet), n)]

def matrix_to_dict(matrix):
    letter_dict = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            letter_dict[matrix[i][j]] = (i, j)
    return letter_dict

def prepare_text(text):
    text = text.upper().replace(" ", "")
    i = 0
    while i < len(text) - 1:
        if text[i] == text[i+1]:
            text = text[:i+1] + 'Ь' + text[i+2:]
        i += 1
    if len(text) % 2 == 1:
        text += 'Ь'
    return text

def get_next_letter_row(c, idx, matrix):
    return matrix[idx[0]][(idx[1] + 1) % n]

def get_next_letter_column(c, idx, matrix):
    return matrix[(idx[0] + 1) % k][(idx[1])]

def encrypt(text, matrix):
    letter_dict = matrix_to_dict(matrix)
    print(letter_dict)
    ciphertext = ""
    for i in range(0, len(text), 2):
        c1 = text[i]
        c2 = text[i + 1]
        idx1 = letter_dict[c1]
        idx2 = letter_dict[c2]
        idx = (0, 0)
        if idx1[0] == idx2[0]: # the same row
            c11 = get_next_letter_row(c1, idx1, matrix)
            c12 = get_next_letter_row(c1, idx2, matrix)
        elif idx1[1] == idx2[1]: # the same column
            c11 = get_next_letter_column(c1, idx1, matrix)
            c12 = get_next_letter_column(c1, idx2, matrix)
        else:
            c11 = matrix[idx1[0]][idx2[1]]
            c12 = matrix[idx2[0]][idx1[1]]
        ciphertext += c11 + c12

    return ciphertext

def decrypt(ciphertext, matrix):
    letter_dict = matrix_to_dict(matrix)
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        c1 = ciphertext[i]
        c2 = ciphertext[i + 1]
        idx1 = letter_dict[c1]
        idx2 = letter_dict[c2]

        if idx1[0] == idx2[0]:  # same row
            p1 = matrix[idx1[0]][(idx1[1] - 1) % n]
            p2 = matrix[idx2[0]][(idx2[1] - 1) % n]
        elif idx1[1] == idx2[1]:  # same column
            p1 = matrix[(idx1[0] - 1) % k][idx1[1]]
            p2 = matrix[(idx2[0] - 1) % k][idx2[1]]
        else:
            p1 = matrix[idx1[0]][idx2[1]]
            p2 = matrix[idx2[0]][idx1[1]]

        plaintext += p1 + p2

    return plaintext

if __name__ == "__main__":
    key = "ПРИПКЛАДКЛЮЧ"
    # key = "БАНДЕРОЛЬ"
    matrix = create_playfair_matrix(key)
    print(matrix)
    plaintext = input("Введіть текст для шифрування: ")
    plaintext = prepare_text(plaintext)
    print(plaintext)
    ciphertext = encrypt(plaintext, matrix)
    print("Зашифрований текст:", ciphertext)
    # Для дешифрування:
    decrypted_text = decrypt(ciphertext, matrix)
    print("Дешифрований текст:", decrypted_text)