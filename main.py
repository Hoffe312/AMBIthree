from random import randint as r
from termcolor import cprint


def print_factory(m, tuple_arr):
    labels = ["A+", "C+", "G+", "T+", "A-", "C-", "G-", "T-"]
    for i in range(len(labels)):
        if i == 0:
            print("   ", end="")
        print(labels[i], end="    ")
    print("")
    for i in range(len(m)):
        print(labels[i], end=" ")
        for j in range(len(m)):
            if (i, j) in tuple_arr:
                cprint("%0.3f" % m[i][j], "red", end=" ")
            else:
                print("%0.3f" % m[i][j], end=" ")
        print("")
    print("")


def create_hmm(hmm_size, matrix):
    markov_chain = ""
    labels = ["A+", "C+", "G+", "T+", "A-", "C-", "G-", "T-"]
    digit = labels[r(0, 7)]
    for i in range(hmm_size):
        rand_number = r(0, 1000)
        digit_index = labels.index(digit)
        sum = 0
        count = 0
        while True:
            if sum <= rand_number and count < 8:
                sum += matrix[digit_index][count] * 1000
                count += 1
            else:
                markov_chain += labels[count - 1]
                digit = labels[count - 1]
                break
    seq = markov_chain[::2]
    hidden_emission = markov_chain[1::2]
    print(seq + "\n" + hidden_emission)

    return seq, hidden_emission


def viterbi(seq, matrix, hidden_emission):
    labels = ["A", "C", "G", "T"]
    viterbi_chance_arr = []
    viterbi_status_arr = hidden_emission
    viterbi_str = ""
    change_matrix = input("matrix change?(if no : enter, else: dont leave it blank):\n")
    if change_matrix:
        matrix = matrix_change(matrix)
    for i in range(len(seq) - 1):
        if hidden_emission == "+":
            index_from = labels.index(seq[i])
        else:
            index_from = labels.index(seq[i]) + 4
        index_to = labels.index(seq[i + 1])
        cell_one = matrix[index_from][index_to]
        cell_two = matrix[index_from][index_to + 4]
        if cell_one < cell_two:
            viterbi_chance_arr.append(cell_two)
            viterbi_status_arr += "-"
            hidden_emission = "-"
        else:
            viterbi_chance_arr.append(cell_one)
            viterbi_status_arr += "+"
            hidden_emission = "+"
    #  viterbi_num = viterbi_chance_arr[0]
    #  for i in range(0, len(viterbi_chance_arr)):
    #      print(f"{i + 1}. {viterbi_num}")
    #       viterbi_num = viterbi_num * viterbi_chance_arr[i]
    for i in range(len(viterbi_status_arr)):
        # print(viterbi_status_arr[i], end="")
        viterbi_str += viterbi_status_arr[i]
    print("viterbi:\n", viterbi_str)
    viterbi_false(hidden_emission, viterbi_str)


def hamming_distance(obj1, obj2):
    """Calculates hamming distance for two objects at the time.
    The method we have used is better explained in the protocol."""
    len_obj1, len_obj2 = len(obj1), len(obj2)
    get_min_len = min(len_obj1, len_obj2)
    count = 0
    for i in range(get_min_len):
        if obj1[i] != obj2[i]:
            count += 1

    return count


def viterbi_false(seq, vit):
    vit_distance = hamming_distance(seq, vit)
    vit_err_rate = (vit_distance / len(seq)) * 100
    print("Die Fehlerrate des Viterbi-Algorithmus liegt bei: ", vit_err_rate, "%")


def matrix_change(matrix):
    labels = ["A+", "C+", "G+", "T+", "A-", "C-", "G-", "T-"]
    choice = True
    tuple_arr = []
    while choice:
        print("A+=0 C+=1 G+=2 T+=3 A-=4 C-=5 G-=6 T-=7")
        row, col = input("which cell would you like to change?:\n").split(" ")
        new_value = float(input("please put in the new value of the cell:\n"))
        row, col = int(row), int(col)
        tuple_arr.append((row, col))
        print(f"you are changing the cell {labels[row]}, {labels[col]} from {matrix[row][col]} to {new_value} \n")
        matrix[row].pop(col)
        matrix[row].insert(col, new_value)
        print_factory(matrix, tuple_arr)
        choice = input("change another cell?:\n")

    return matrix


def main():  # A+     C       G      T      A-      C      G      T
    matrix = [[0.144, 0.219, 0.341, 0.096, 0.050, 0.050, 0.050, 0.050],
              [0.137, 0.294, 0.219, 0.150, 0.050, 0.050, 0.050, 0.050],
              [0.129, 0.271, 0.300, 0.100, 0.050, 0.050, 0.050, 0.050],
              [0.063, 0.284, 0.307, 0.146, 0.050, 0.050, 0.050, 0.050],
              [0.025, 0.025, 0.025, 0.025, 0.270, 0.184, 0.256, 0.189],
              [0.025, 0.025, 0.025, 0.025, 0.290, 0.268, 0.070, 0.272],
              [0.025, 0.025, 0.025, 0.025, 0.223, 0.221, 0.268, 0.187],
              [0.025, 0.025, 0.025, 0.025, 0.159, 0.215, 0.263, 0.263]]

    seq, hidden_emission = create_hmm(1000, matrix)
    viterbi(seq, matrix, hidden_emission[0])


if __name__ == '__main__':
    main()
