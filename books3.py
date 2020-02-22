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
    scanned_books = set()
    list_of_libraries = []
    list_of_signed_up = []
    required_books = set()

    def __init__(self, nb_of_days_for_signup, shipment_speed, list_of_books, id):
        self.id = id
        self.days_to_signup = nb_of_days_for_signup
        self.speed = shipment_speed
        self.list_of_books = set(list_of_books)
        self.sorted_books = []
        self.books_to_scan = []
        self.total_score = 0

    def calculate_total(self):
        self.total_score = self.calculate_reward(self.list_of_books)

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

    @classmethod
    def reset(cls):
        cls.book_scores = []
        cls.days_left = 0
        cls.scanned_books = set()
        cls.list_of_libraries = []
        cls.list_of_signed_up = []

    @classmethod
    def get_score(cls):
        """
        Must call this method after processing all libraries in the file and after writing to file
        :return: int score achieved for the file
        """
        total = 0
        for book in cls.scanned_books:
            total += cls.book_scores[book]

        return total

    def get_time_required(self):
        # print(f"{self.speed}, {len(self.list_of_books)}")
        shipments_required = len(self.list_of_books) / self.speed
        return self.days_to_signup + shipments_required

    def enroll(self, set_books=None):
        """
        This function enrolls the library in the scanning process and adds the books to the scanning list

        """
        if self in Library.list_of_signed_up:
            return  # Making sure the library was not already enrolled

        self.sort_books()
        if set_books is None and len(self.sorted_books) > 0:
            if self.days_to_signup < Library.days_left:     # Checking if enough days left to enroll
                Library.days_left -= self.days_to_signup
                spare_days = Library.days_left
                for day in range(Library.days_left):
                    for shipment in range(self.speed):
                        if len(self.sorted_books) > 0:
                            current_book = self.sorted_books.pop()
                            while current_book in Library.scanned_books:
                                if len(self.sorted_books) > 0:
                                    current_book = self.sorted_books.pop()
                                    # print("Book exists already")
                                else:
                                    break
                            Library.scanned_books.add(current_book)
                            self.books_to_scan.append(current_book)
                            self.total_score -= Library.book_scores[current_book]
                            self.list_of_books.remove(current_book)
                            # Library.book_scores[current_book] = 0
                        else:
                            break
                    if len(self.sorted_books) == 0:
                        break
                    spare_days -= 1     # This is to see how many days there are left after enrolling the library

            # self.days_to_signup = Library.days_left + 1    # This will make sure we will not add the library again
            # Library.list_of_libraries.remove(self)
            # print(f"Spare days {spare_days}")
            Library.list_of_signed_up.append(self)
        elif set_books is not None and len(set_books) > 0:
            Library.scanned_books.union(set_books)
            self.books_to_scan = list(set_books)
            Library.list_of_signed_up.append(self)

    def sort_books(self):
        """
        Sorts the books according to score
        :return:
        """
        if len(self.sorted_books) == 0: # and self not in Library.list_of_signed_up:
            self.sorted_books = self.get_sorted_books()


    def simulate_enroll(self):
        """
        This method simulates the enrollment of a library
        It is good to keep track of which libraries are worth to enroll
        :return:
        (int: score rewarded, set: books to enroll, int days_to_spare)
        """
        self.sort_books()
        temp_set = set()
        spare_days = Library.days_left
        spare_days -= self.days_to_signup
        ordered_books = self.sorted_books.copy()
        for day in range(spare_days):
            for shipment in range(self.speed):
                if len(ordered_books) > 0:
                    current_book = ordered_books.pop()
                    while current_book in Library.scanned_books:
                        if len(ordered_books) > 0:
                            current_book = ordered_books.pop()
                        else:
                            break
                    temp_set.add(current_book)
                else:
                    break
            if len(ordered_books) == 0:
                break
            spare_days -= 1
        return self.calculate_reward(temp_set), temp_set, spare_days

    def calculate_reward(self, id_set=None):
        if id_set is None:
            id_set = Library.scanned_books
        total = 0
        for book in id_set:
            total += Library.book_scores[book]
        return total

    def __str__(self):
        return f"Days to signup: {self.days_to_signup} | " \
               f"Books shipped per day: {self.speed} | " \
               f"Library id: {self.id} | " \
               f"NB of books: {len(self.list_of_books)} | " \
               f"Sorted books: {self.sorted_books}"

    @property
    def average(self):
        return self.total_score / len(self.list_of_books)

    @property
    def sort(self):
        if self.total_score < 1:
            return 0
        return (self.days_to_signup / self.speed) / self.total_score

    @property
    def test_sort(self):
        # return self.calculate_reward(Library.scanned_books.difference(set(self.list_of_books)))
        return self.calculate_reward(self.list_of_books)

def read_file(file):
    Library.reset()
    with open(file, "r") as f:
        lines = f.read().split("\n")
        library_nb = int(lines[0].split()[1])
        days_to_ship = int(lines[0].split()[2])
        books_score = {}
        key = 0
        for score in lines[1].split():
            books_score[key] = int(score)
            key += 1
        Library.book_scores = books_score
        index = 2
        list_of_library = []

        for i in range(library_nb):
            params = lines[index].split()
            library = Library(int(params[1]), int(params[2]), [], i)
            for id in lines[index+1].split():
                int_id = int(id)
                library.total_score += int_id
                library.list_of_books.add(int_id)

            list_of_library.append(library)
            library.calculate_total()
            index += 2
    Library.scanned_books = set()
    Library.days_left = days_to_ship
    Library.list_of_libraries = list_of_library


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


def sort_libraries(file):
    """
    This method sorts the libraries using different formulas for different files, found by trial and error
    :param file:
    :return:
    """
    if "b_" in file:
        Library.list_of_libraries.sort(key=lambda c: c.days_to_signup / c.speed, reverse=False)
    elif "d_" in file:
        Library.list_of_libraries.sort(key=lambda c: c.simulate_enroll()[0], reverse=True)
    else:
        Library.list_of_libraries.sort(key=lambda c: c.sort, reverse=False)


def loop_libraries(stop_days):
    for library in Library.list_of_libraries:
        if library.simulate_enroll()[0] > 100:
            library.enroll()
        elif "a_" in file:
            library.enroll()
        if Library.days_left < stop_days:
            break

def process(file):
    tic = time.perf_counter()
    read_file(file)
    sort_libraries(file)
    initial_time = Library.days_left
    if "d_" in file:
        for i in range(2, 17):
            sort_libraries(file)
            loop_libraries(initial_time / i)
        # Library.list_of_libraries.sort(key=lambda c: c.test_sort, reverse=False)
        loop_libraries(0)
    else:
        loop_libraries(initial_time / 6)
        sort_libraries(file)
        loop_libraries(0)

    write_file(file, Library.list_of_signed_up)
    score = Library.get_score()
    toc = time.perf_counter()
    print(f"Processed {file} in {toc - tic}. Score = {score}")


if __name__ == "__main__":

    from test import main as test_solutions
    tic = time.perf_counter()
    for file in file_names:
        process(file)

    toc = time.perf_counter()
    print(f"Finished in {toc - tic}")
    test_solutions("out3")
