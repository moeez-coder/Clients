"""Adaptive, lossless partitioning of a large search into shards under a provider's result cap.

Dimensions must be single-valued per record (a person has exactly one country, one job level,
one current-company industry ...). Splitting on such dimensions guarantees the shards are
disjoint and together cover the parent, so the sum of shard totals must equal the parent total.
"""
from dataclasses import dataclass, field


@dataclass
class Shard:
    filters: dict
    expected_total: int
    oversized: bool = False
    parent_total: int | None = None
    split_log: list = field(default_factory=list)


def plan_shards(base_filters, dims, count_fn, cap, on_split=None):
    """Recursively split `base_filters` along `dims` until every leaf is <= cap.

    dims: ordered list of (dimension_name, [values]).
    count_fn(filters) -> int, injected so it can be a live provider count or a fake.
    on_split(parent_filters, parent_total, children_total) is called after each split so the
    caller can log partition integrity (provider totals may be estimates).
    """
    total = count_fn(dict(base_filters))
    return _split(dict(base_filters), total, list(dims), count_fn, cap, on_split, None)


def _split(filters, total, dims, count_fn, cap, on_split, parent_total):
    if total <= 0:
        return []
    if total <= cap:
        return [Shard(filters, total, parent_total=parent_total)]
    if not dims:
        return [Shard(filters, total, oversized=True, parent_total=parent_total)]
    name, values = dims[0]
    leaves = []
    children_total = 0
    for v in values:
        child = dict(filters)
        child[name] = v
        n = count_fn(child)
        children_total += max(n, 0)
        leaves.extend(_split(child, n, dims[1:], count_fn, cap, on_split, total))
    if on_split:
        on_split(filters, total, children_total)
    return leaves
