from sqlalchemy import asc, desc
from sqlalchemy.orm import Query as SAQuery


def apply_filters(query, model, filters):
    for field, value in filters.items():
        if isinstance(value, list):
            query = query.filter(getattr(model, field).in_(value))
        elif hasattr(model, field):
            query = query.filter(getattr(model, field) == value)

    return query


def apply_sorting(query: SAQuery, model, sort: str | None, order: str):
    if sort and hasattr(model, sort):
        col = getattr(model, sort)
        return query.order_by(desc(col) if order == "DESC" else asc(col))
    return query


def apply_pagination(query: SAQuery, start: int, limit: int):
    return query.offset(start).limit(limit)


def refine_query(query: SAQuery, model, params):
    filtered = apply_filters(query, model, params.filters)

    total = filtered.count()

    sorted_query = apply_sorting(filtered, model, params.sort, params.order)
    paginated = apply_pagination(sorted_query, params.start, params.limit)

    return paginated.all(), total
