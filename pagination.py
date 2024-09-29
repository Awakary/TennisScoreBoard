from session import calculate_quantity_of_objects


class Pagination:

    page_size = 3

    def __init__(self, queryset, page_number, last_page=None, back_page=None):
        self.queryset = queryset
        self.page_number = int(page_number) if not last_page else int(last_page) + 1
        self.quantity_of_objects = self.get_quantity_of_objects()
        self.count_pages = self.get_count_pages()
        self.back_page = back_page
        self.last_page = self.get_last_page(last_page)
        self.start_page = self.get_start_page()

    def get_last_page(self, last_page):
        if self.back_page:
            return int(self.back_page) - 1
        if last_page:
            if int(last_page) + 5 >= self.count_pages:
                return self.count_pages
            else:
                return int(last_page) + 5
        elif int(self.page_number) % 5 != 0:
            p = (int(self.page_number) // 5 + 1) * 5
            a = p if p <= self.count_pages else self.count_pages
            return a
        return int(self.page_number)

    def get_start_page(self):
        if self.back_page:
            return self.last_page - 4
        if int(self.page_number) % 5 != 0 and self.page_number != 1:
            return int(self.page_number) // 5 * 5 + 1
        if self.last_page % 5 != 0:
            return self.last_page // 5 * 5 + 1
        if self.last_page % 5 == 0:
            return self.last_page - 4
        return 1

    def get_quantity_of_objects(self):
        return calculate_quantity_of_objects(self.queryset)

    def get_count_pages(self):
        return self.quantity_of_objects // self.page_size + (1 if self.quantity_of_objects % self.page_size > 0 else 0)

    def get_objects_for_page(self):
        # if self.last_page != 5:
        #     return self.queryset[int(page_number) * self.page_size -
        #                          Pagination.page_size:int(page_number) * self.page_size]

        return self.queryset[int(self.page_number) * self.page_size -
                             Pagination.page_size:int(self.page_number)*self.page_size]


    #
    # def get_objects_on_page(self, current_page):
    #     start_index = (current_page - 1) * self.page_size
    #     end_index = current_page * self.page_size
    #     return self.quantity_of_objects[start_index:end_index]
    #
    # def get_previous_page(self, current_page):
    #     return self.get_current_page(current_page - 1)
    #
    # def get_next_page(self, current_page):
    #     return self.get_current_page(current_page + 1)

