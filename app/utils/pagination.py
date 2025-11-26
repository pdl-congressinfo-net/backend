from fastapi import Query, Request


class PaginationParams:
    def __init__(
        self,
        request: Request,
        _start: int = Query(0, ge=0),
        _end: int = Query(10, ge=1),
        _sort: str | None = None,
        _order: str = "ASC",
    ):
        self.start = _start
        self.end = _end
        self.limit = _end - _start
        self.sort = _sort
        self.order = _order

        self.filters = dict(request.query_params)

        for key in ["_start", "_end", "_sort", "_order"]:
            self.filters.pop(key, None)
