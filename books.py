file_names = [
    "a_example.txt",
    "b_read_on.txt",
    "c_incunabula.txt",
    "d_tough_choices.txt",
    "e_so_many_books.txt",
    "f_libraries_of_the_world.txt"
]


class Library:

    def __init__(self, nb_of_books, nb_of_days_for_signup, shipment_speed, list_of_books, id):
        self.id = id
        self.nb_of_books = nb_of_books
        self.days_to_signup = nb_of_days_for_signup
        self.speed = shipment_speed
        self.list_of_books = list_of_books
        self.books_to_scan = []

    def __str__(self):
        return f"Nb of books: {self.nb_of_books} | " \
               f"Days to signup: {self.days_to_signup} | " \
               f"Books shipped per day: {self.speed} | " \
               f"Library id: {self.id} | " \
               f"List of books: {self.list_of_books} | " \
               f""

    @property
    def sort(self):
        return self.days_to_signup / self.speed


def read_file(file):
    with open(file, "r") as f:
        lines = f.read().split("\n")
        books_nb = int(lines[0].split()[0])
        library_nb = int(lines[0].split()[1])
        days_to_ship = int(lines[0].split()[2])
        books_score = {}
        key = 0
        for score in lines[1].split():
            books_score[key] = int(score)
            key += 1

        index = 2
        list_of_library = []
        for i in range(library_nb):
            params = lines[index].split()
            list_of_books = []
            for id in lines[index+1].split():
                list_of_books.append(int(id))
            library = Library(int(params[0]), int(params[1]), int(params[2]), list_of_books, i)
            list_of_library.append(library)
            index += 2
    return books_score, days_to_ship, list_of_library


def write_file(file, list_of_signed_up):
    nb_of_libraries = len(list_of_signed_up)
    output = str(nb_of_libraries)
    for library in list_of_signed_up:
        id = library.id
        nb = len(library.books_to_scan)
        books = ""
        for book in library.books_to_scan:
            books = books + str(book) + " "
        output = output + f"\n{id} {nb}\n{books}"

    with open(file.replace("txt", "out"), "w")as f:
        f.write(output)


def process(file):
    book_scores, days_to_ship, list_of_libraries = read_file(file)
    # print(book_scores)
    list_of_libraries.sort(key=lambda x: x.sort, reverse=False)
    list_of_signed_up = []
    for library in list_of_libraries:
        ind = 0
        if days_to_ship > library.days_to_signup:
            list_of_signed_up.append(library)
            days_to_ship -= library.days_to_signup
                       # counts the books for this specific library
            for i in range(days_to_ship):
                # print(f"Days left {days_to_ship}, index is {ind}")
                for x in range(library.speed):
                    # print(f"{library.books_to_scan} and {library.list_of_books}")
                    if len(library.books_to_scan) == len(library.list_of_books):
                        break

                    library.books_to_scan.append(library.list_of_books[ind + x])
                if ind < len(library.list_of_books) - 1:
                    ind += library.speed
                else:
                    break
                if len(library.books_to_scan) == len(library.list_of_books):
                    break
        # print(library.list_of_books)
        # print(f"Books to scan from {library.id}: {library.books_to_scan}")
    write_file(file, list_of_signed_up)


if __name__ == "__main__":
    for file in file_names:
        process(file)

