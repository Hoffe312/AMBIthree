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


def viterbi(seq, matrix):
    labels = ["A", "C", "G", "T"]

    change_matrix = input("matrix change?(if no : enter, else: dont leave it blank):\n")
    if change_matrix:
        matrix = matrix_change(matrix)

    # initialize
    current_plus = 0.5 * 0.25
    current_minus = 0.5 * 0.25

    plus_path = "+"
    minus_path = "-"

    for i in range(len(seq) - 1):
        index_from = labels.index(seq[i])
        index_to = labels.index(seq[i + 1])

        cell_one = matrix[index_from][index_to]
        cell_two = matrix[index_from][index_to + 4]
        cell_three = matrix[index_from + 4][index_to]
        cell_four = matrix[index_from + 4][index_to + 4]

        if current_plus * cell_one > current_minus * cell_three:
            new_p_plus = 5 * current_plus * cell_one
            plus_path += "+"

        else:
            new_p_plus = 5 * current_minus * cell_three
            plus_path += "-"

        if current_plus * cell_two > current_minus * cell_four:
            new_p_minus = 5 * current_plus * cell_two
            minus_path += "+"
        else:
            new_p_minus = 5 * current_minus * cell_four
            minus_path += "-"

        current_plus = new_p_plus
        current_minus = new_p_minus
    viterbi_path = ""
    if current_plus > current_minus:
        viterbi_path += plus_path[-1]
    else:
        viterbi_path += minus_path[-1]
    for i in range(1, len(seq)):
        if viterbi_path[-1] == "+":
            viterbi_path += plus_path[-i]
        else:
            viterbi_path += minus_path[-i]
    viterbi_path = viterbi_path[::-1]
    print("viterbi states:\n", viterbi_path)
    return viterbi_path


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


# user interface for matrix changes
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
    viterbi_str = viterbi(seq, matrix)
    viterbi_false(hidden_emission, viterbi_str)

    test_seq = "ATCTTGCTCAACAAATACATTTCGCTTTGTTTTGGGCATGCGGCTTTAGGTTCTACGCTCAAAGATGAGAAGTCAGGTAACAGAAGGACGAGTCTTCAACTAGGCGGCCCTGTGCGTGCGACCTGGGCATCCGAGGACCCGGAGCCGTGCCTTACCATCCTGTGCCTGAGCCATAAGTTCTAGGGATGTGATCCCTACCCAAGGATCCAGCCGGCATGGCGGCAGTGAAAATAAGTCCTGGCTCATTTGTTCGGAAACTCAGACAAATCATGCACAGTACTCCCTTAATGGCAGGGAGAGGGAGACCTCCTCAGCAACTGTCTTCGGTTACCCGGGTCCATTTGGCACAAACTCCATAGCCTGGGGATAGGACTCTCCTGTGTAACCCAGTTGCAGTTCAGCTGAACAGAAGGAGGGCACACCCACTTGCAAGTTTTGGGGGGAGAAAAAAGACTACCTATTCGCTGTCATGATCTTCACGCAGAGCTGATGAGTCTCGGGACGAATGCCATGCGACGTTCGGGAGTTCCTCGCTAGGAGCTCAGGCAAACTGATCCTTAAAAAACGGATTCATAGTGTGGCAGGACCCGGCCTATGTTTCCAATTGGATCTCCGATTTTTGATGGTATGCGCCATCCCTTTCGGACCCCACTCTCTTGCTGGGAAGTATACACACGCACAGGATTGGCGTGGCTCCACTTGCAAAAGCTCCATAAGTGCAAGTTGATAATCATCCAAACCTTCTGCTTTTCCATGACACATCCAGGGGTGCCCAGGGACATTATTGGTTTTGCAGGACTCCTGGTCACCAAGTAAGTTGATTAAATTGTGGAGAACAAGTTTAAGGCCCACGCCCGGGGAGAACACTGGTTCAGTCGAGTCGGTGGGGTCCCTCGGCTCCGAACGGAGAGCCTGTGAGCAGGATTAGACTTAAGACTCACCAGGGTTTAGTCGGTGACCCCTTTATATTTAAGAAAGGAGACTGAGACATGAGAAGTGC"
    viterbi(test_seq, matrix)




if __name__ == '__main__':
    main()
