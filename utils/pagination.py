from db.dao import DAO


class Pagination:

    page_size = 3

    def __init__(self, queryset, page, filtered_param=None,
                 last_page=None, back_page=None):
        self.queryset = queryset
        self.page = self.get_page(page, last_page, back_page)
        self.quantity_of_objects = self.get_quantity_of_objects()
        self.count_pages = self.get_count_pages()
        self.back_page = back_page
        self.last_page = self.get_last_page(last_page)
        self.start_page = self.get_start_page()
        self.filtered_param = filtered_param

    def get_page(self, page, last_page, back_page):
        print(page)
        if last_page:
            return int(last_page) + 1
        elif back_page:
            return int(back_page) - 5
        return int(page)

    def get_last_page(self, last_page):
        if self.back_page:
            return int(self.back_page) - 1
        if last_page:
            if int(last_page) + 5 >= self.count_pages:
                return self.count_pages
            else:
                return int(last_page) + 5
        elif int(self.page) % 5 != 0:
            p = (int(self.page) // 5 + 1) * 5
            return p if p <= self.count_pages else self.count_pages
        return int(self.page)

    def get_start_page(self):
        if self.back_page:
            return self.last_page - 4
        if int(self.page) % 5 != 0 and self.page != 1:
            return int(self.page) // 5 * 5 + 1
        if self.last_page % 5 != 0:
            return self.last_page // 5 * 5 + 1
        if self.last_page % 5 == 0:
            return self.last_page - 4
        return 1

    def get_quantity_of_objects(self):
        return DAO().calculate_quantity_of_objects(self.queryset)

    def get_count_pages(self):
        return self.quantity_of_objects // self.page_size + (1 if self.quantity_of_objects % self.page_size > 0 else 0)

    def get_objects_for_page(self):
        return self.queryset[int(self.page) * self.page_size -
                             Pagination.page_size:int(self.page)*self.page_size]



