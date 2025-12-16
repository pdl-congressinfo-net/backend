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
        _order: str = "ASC",
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

        self.sort = _sort
        self.order = _order

        self.filters = request.query_params.multi_items()
        self.filters = dict(self.filters)

        for key in ["_start", "_end", "_sort", "_order", "currentPage", "pageSize"]:
            self.filters.pop(key, None)
