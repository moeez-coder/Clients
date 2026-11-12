from listbuild.sharding import plan_shards

# Synthetic population: each record has exactly one value per dimension.
POP = []
for c, n_c in (("US", 60), ("GB", 12), ("NZ", 3)):
    for lvl, n_l in (("C-Team", 2), ("VP", 1), ("Director", 3)):
        for ind in ("A", "B"):
            POP += [{"country": c, "level": lvl, "industry": ind}] * (n_c * n_l)

DIMS = [("country", ["US", "GB", "NZ"]), ("level", ["C-Team", "VP", "Director"]), ("industry", ["A", "B"])]


def count(filters):
    return sum(1 for r in POP if all(r[k] == v for k, v in filters.items()))


def test_leaves_respect_cap_and_partition_is_lossless():
    shards = plan_shards({}, DIMS, count, cap=100)
    assert all(s.expected_total <= 100 for s in shards if not s.oversized)
    assert sum(s.expected_total for s in shards) == len(POP)
    # disjoint cover: every record matches exactly one leaf
    for r in POP:
        hits = [s for s in shards if all(r[k] == v for k, v in s.filters.items())]
        assert len(hits) == 1


def test_small_population_yields_single_unsplit_shard():
    shards = plan_shards({"country": "NZ"}, DIMS[1:], count, cap=100)
    assert len(shards) == 1 and shards[0].filters == {"country": "NZ"} and shards[0].expected_total == 36


def test_exhausted_dimensions_flag_oversized_leaf():
    shards = plan_shards({}, DIMS, count, cap=10)
    big = [s for s in shards if s.oversized]
    assert big and all(s.expected_total > 10 for s in big)
    assert sum(s.expected_total for s in shards) == len(POP)


def test_empty_shards_are_dropped():
    shards = plan_shards({}, DIMS + [("bogus", ["x", "y"])], lambda f: 0 if "bogus" in f else count(f), cap=10)
    assert all(s.expected_total > 0 for s in shards)
