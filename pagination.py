from session import calculate_quantity_of_objects


class Pagination:

    page_size = 3

    def __init__(self, queryset):
        self.quantity_of_objects = self.get_quantity_of_objects(queryset)

    def get_quantity_of_objects(self, queryset):
        return calculate_quantity_of_objects(queryset)

    def get_count_pages(self):
        return self.quantity_of_objects // self.page_size + (1 if self.quantity_of_objects % self.page_size > 0 else 0)

    def get_objects_for_page(self, queryset, page_number):
        return queryset[int(page_number) * self.page_size -
                        Pagination.page_size:int(page_number)*self.page_size]


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

