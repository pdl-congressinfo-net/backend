import datetime

from sqlalchemy import (
    Boolean,
    Date,
    Float,
    Integer,
    and_,
    asc,
    cast,
    desc,
)
from sqlalchemy.orm import Query as SAQuery


def is_date_only(value: str) -> bool:
    """
    Returns True for values in YYYY-MM-DD format (10 chars).
    """
    return isinstance(value, str) and len(value) == 10 and value.count("-") == 2


def convert_value(column, value):
    """
    Convert query param strings to the correct Python type.
    If YYYY-MM-DD → returns datetime.date
    If ISO datetime → returns datetime.datetime
    """
    # Lists
    if isinstance(value, list):
        return [convert_value(column, v) for v in value]

    # Date-only
    if is_date_only(value):
        try:
            return datetime.date.fromisoformat(value)
        except ValueError:
            pass

    # Datetime
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        pass

    # Int
    if isinstance(column.type, Integer):
        try:
            return int(value)
        except Exception:
            pass

    # Float
    if isinstance(column.type, Float):
        try:
            return float(value)
        except Exception:
            pass

    # Bool
    if isinstance(column.type, Boolean):
        if isinstance(value, str):
            if value.lower() in ["true", "1"]:
                return True
            if value.lower() in ["false", "0"]:
                return False

    return value


def build_expression(column, op, value):
    """
    Build SQLAlchemy expression.
    Handles date-only vs full datetime.
    """

    # DATE ONLY → compare DATE(column) >= DATE(value)
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        date_col = cast(column, Date)

        if op == "gte":
            return date_col >= value
        if op == "lte":
            return date_col <= value
        if op == "gt":
            return date_col > value
        if op == "lt":
            return date_col < value
        if op == "eq":
            return date_col == value
        if op == "ne":
            return date_col != value

        raise ValueError(f"Unsupported date-only operator: {op}")

    # DATETIME → compare full value
    if op == "gte":
        return column >= value
    if op == "lte":
        return column <= value
    if op == "gt":
        return column > value
    if op == "lt":
        return column < value
    if op == "eq":
        return column == value
    if op == "ne":
        return column != value
    if op == "contains" or op == "like":
        return column.like(f"%{value}%")

    if op == "in":
        if isinstance(value, str):
            value = value.split(",")
        return column.in_(value)

    raise ValueError(f"Unsupported operator: {op}")


def apply_filters(query, model, filters):
    grouped = {}  # { "gte": [(column, value), ...] }

    for raw_field, value in filters.items():
        # Parse operator
        if "_" in raw_field:
            field, op = raw_field.rsplit("_", 1)
        else:
            field, op = raw_field, "eq"

        if not hasattr(model, field):
            continue

        column = getattr(model, field)
        converted_value = convert_value(column, value)

        grouped.setdefault(op, []).append((column, converted_value))

    for op, items in grouped.items():
        if len(items) == 1:
            col, val = items[0]
            expr = build_expression(col, op, val)
            query = query.filter(expr)
        else:
            conditions = [build_expression(col, op, val) for col, val in items]
            query = query.filter(and_(*conditions))

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
