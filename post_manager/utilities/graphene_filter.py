from graphql import GraphQLError


class Filter:
    supported_filter_expr = [
        "exact",
        "icontains",
    ]

    def __init__(self, data):
        self.data = data

    def set_data(self, data):
        self.data = data

    def all(self):
        return self.data

    def check_filter_type(self, filter_type):
        if filter_type not in self.supported_filter_expr:
            raise GraphQLError(
                f"{filter_type} is not under supported filter expression"
            )

    def filter_new(self, filter_name, filter_value, filter_type=None):
        """
        simulate django-filter
        but over here we dont use orm mapping
        """
        self.check_filter_type(filter_type)
        data = []
        index = 0
        # loop list of dictionaries
        for element in self.data:

            matched = 0
            # loop the dictionaries to get key and value
            for data_key, data_value in element.items():
                # check filter expression specified by child class's Meta attribute
                if filter_name == data_key:
                    matched = self._filter(filter_value, data_value, filter_type)

            if matched:
                temp_dict = {}
                for data_key, data_value in self.data[index].items():
                    temp_dict[data_key] = data_value
                data.append(temp_dict)
            index += 1
        self.set_data(data)

    def _filter(self, a, b, filter_expr=None):
        if filter_expr == "exact":
            return 1 if str(a) == str(b) else 0

        if filter_expr == "icontains":
            return 1 if str(a) in str(b) else 0

    def sort(self, sortBy=False):
        if sortBy:
            if sortBy[0] == "-":
                sortBy = sortBy.split("-")[1]
                reverse = True
            else:
                reverse = False

        return sorted(self.all(), key=lambda k: k.get(sortBy, 0), reverse=reverse)


def get_pagination_index(page_number):
    page_size = 10
    if page_number == 1:
        first = 0
        last = page_size
    else:
        first = page_size * page_number - 10
        last = page_size * page_number

    return first, last
