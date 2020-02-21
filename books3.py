import time
from collections import deque
file_names = [
    "a_example.txt",
    "b_read_on.txt",
    "c_incunabula.txt",
    "d_tough_choices.txt",
    "e_so_many_books.txt",
    "f_libraries_of_the_world.txt"
]


class Library:
    # Class variables
    book_scores = []
    days_left = 0
    global_books = set()
    list_of_libraries = []

    def __init__(self, nb_of_books, nb_of_days_for_signup, shipment_speed, list_of_books, id):
        self.id = id
        self.nb_of_books = nb_of_books
        self.days_to_signup = nb_of_days_for_signup
        self.speed = shipment_speed
        self.list_of_books = list_of_books
        self.books_to_scan = []
        self.total_score = 0

    def get_sorted_books(self):
        sorted_books = []
        for book in self.list_of_books:
            score = Library.book_scores[book]
            sorted_books.append([score, book])
        sorted_books.sort(reverse=False)
        output = deque()   # Converting into a quee
        for item in sorted_books:
            output.append(item[1])
        return output

    def get_time_required(self):
        # print(f"{self.speed}, {len(self.list_of_books)}")
        shipments_required = len(self.list_of_books) / self.speed
        return self.days_to_signup + shipments_required


    def __str__(self):
        return f"Nb of books: {self.nb_of_books} | " \
               f"Days to signup: {self.days_to_signup} | " \
               f"Books shipped per day: {self.speed} | " \
               f"Library id: {self.id} | " \
               f"NB of books: {self.nb_of_books} | " \
               f""

    @property
    def sort(self):
        average = self.total_score / len(self.list_of_books)
        # print(average)
        return (self.days_to_signup / self.speed) / self.total_score
        # return self.total_score

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
            library = Library(int(params[0]), int(params[1]), int(params[2]), [], i)
            for id in lines[index+1].split():
                int_id = int(id)
                library.total_score += int_id
                library.list_of_books.append(int_id)

            list_of_library.append(library)
            index += 2
    print(f"{time.time()} {file} read")
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

    with open(file.replace("txt", "out3"), "w")as f:
        f.write(output)
    print(f"{time.time()} {file} processed")


def process(file):
    Library.book_scores, Library.days_left, Library.list_of_libraries = read_file(file)
    Library.list_of_libraries.sort(key=lambda c: c.sort, reverse=False)  # Sorting libraries to start with better ones
    # print(f"{file} sorted")
    Library.global_books = set()
    list_of_signed_up = []
    for library_obj in Library.list_of_libraries:
        if Library.days_left > library_obj.days_to_signup:
            list_of_signed_up.append(library_obj)
            Library.days_left -= library_obj.days_to_signup
            ordered_books = library_obj.get_sorted_books()
            for i in range(Library.days_left):  # Performing shipments for as many days are left
                for x in range(library_obj.speed):  # Adding x books in every shipment
                    if len(ordered_books) > 0:
                        current_book = ordered_books.pop()
                        while current_book in Library.global_books:
                            if len(ordered_books) > 0:
                                current_book = ordered_books.pop()
                            else:
                                break
                        Library.global_books.add(current_book)
                        library_obj.books_to_scan.append(current_book)
                    else:
                        break
                if len(ordered_books) == 0:
                    break
        if file == "b_read_on.txt":
            print(f"Days left: {Library.days_left}\t"
                  f"Current library {library_obj.days_to_signup}\t"
                  f"Time required for entire library {library_obj.get_time_required()}")
            pass
    print(f"{time.time()} finished computing{file}")
    write_file(file, list_of_signed_up)


if __name__ == "__main__":
    tic = time.perf_counter()
    from test import main as t
    from test import test_file
    for file in file_names:
        process(file)
    # process("test.txt")
    # test_file("test.out3")

    toc = time.perf_counter()
    print(f"Finished in {toc-tic}")
    t("out3")
