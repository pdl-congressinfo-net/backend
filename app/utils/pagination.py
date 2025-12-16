from fastapi import Query, Request


class PaginationParams:
    def __init__(
        self,
        request: Request,
        _start: int | None = Query(None, ge=0),
        _end: int | None = Query(None, ge=1),
        currentPage: int | None = Query(None, ge=1, alias="currentPage"),
        pageSize: int | None = Query(None, ge=1, alias="pageSize"),
        _sort: str | None = None,
        _order: str | None = None,
    ):
        # Support both formats: _start/_end and currentPage/pageSize
        if _start is not None and _end is not None:
            # Traditional format: _start and _end
            self.start = _start
            self.end = _end
            self.limit = _end - _start
        elif currentPage is not None and pageSize is not None:
            # Refine format: currentPage and pageSize
            self.start = (currentPage - 1) * pageSize
            self.end = currentPage * pageSize
            self.limit = pageSize
        else:
            # Default values
            self.start = 0
            self.end = 10
            self.limit = 10

        # Parse comma-separated sort fields and orders
        # Format: _sort=first_name,last_name&_order=DESC,ASC
        self.sorts = []
        if _sort:
            sort_fields = _sort.split(",")
            order_values = _order.split(",") if _order else []

            # Pad orders with "ASC" if not enough provided
            while len(order_values) < len(sort_fields):
                order_values.append("ASC")

            self.sorts = [
                {"field": field.strip(), "order": order.strip()}
                for field, order in zip(sort_fields, order_values)
            ]

        # Handle multiple values for the same parameter
        # multi_items() returns list of (key, value) tuples
        multi_items = request.query_params.multi_items()

        # Group values by key to handle multiple values for same parameter
        filters_dict = {}
        for key, value in multi_items:
            if key in filters_dict:
                # If key already exists, convert to list or append to list
                if isinstance(filters_dict[key], list):
                    filters_dict[key].append(value)
                else:
                    filters_dict[key] = [filters_dict[key], value]
            else:
                filters_dict[key] = value

        self.filters = filters_dict

        for key in ["_start", "_end", "_sort", "_order", "currentPage", "pageSize"]:
            self.filters.pop(key, None)
