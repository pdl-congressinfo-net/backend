from typing import Any

from fastapi import Response


def refine_list_response(
    response: Response,
    data: list[Any],
    total: int,
):
    response.headers["X-Total-Count"] = str(total)
    response.headers["Access-Control-Expose-Headers"] = "X-Total-Count"

    return data
