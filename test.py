from books import Library
from books import read_file


def read_output(file):
    with open(file, "r") as o:
        lines = o.read().split("\n")
        nb_of_libraries = int(lines[0].strip())
        libraries = []
        index = 1
        for i in range(nb_of_libraries):
            library_id = int(lines[index].split()[0])
            scanned_books = set()
            for book_id in lines[index+1].split():
                scanned_books.add(int(book_id))
            temp = Library(len(scanned_books), 0, 0, scanned_books, library_id)
            libraries.append(temp)
            index += 2
        return libraries


def test(file):
    test_libraries = read_output(file)

    input_name = file.split(".")[0] + ".txt"
    book_scores, days_left, list_of_libraries = read_file(input_name)
    global_scanned = set()
    score = 0
    # print(len(list_of_libraries))
    for i in range(len(test_libraries)):
        library_id = test_libraries[i].id
        days_to_signup = list_of_libraries[library_id].days_to_signup
        days_left = days_left - days_to_signup
        validation_library = list_of_libraries[library_id]
        scanned = test_libraries[i].list_of_books
        validation_library.list_of_books = set(validation_library.list_of_books)
        # print(validation_library.list_of_books)
        library_score = 0
        # print(f"scanned {scanned}")
        for book in scanned:
            if book in validation_library.list_of_books:
                if book not in global_scanned:
                    library_score += book_scores[book]
                    global_scanned.add(book)

        score += library_score

    print(f"{file} has score {score}")
    return score

def main(extension):
    file_names = [
        "a_example.txt",
        "b_read_on.txt",
        "c_incunabula.txt",
        "d_tough_choices.txt",
        "e_so_many_books.txt",
        "f_libraries_of_the_world.txt"
    ]
    total = 0
    for file in file_names:
        total += test(file.replace("txt", extension))

    print(f"Total score {total}")


if __name__ == "__main__":
    main("out2")
