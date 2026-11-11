"""Check that the full run visits every new clip without changing the pilot schedule."""
from train_assignment2_4bit import sample_position

full = [sample_position(step, 4, True) for step in range(3088)]
assert [index for group, index in full if group == 0] == list(range(2316))
assert [index for group, index in full if group == 1] == list(range(772))
assert [sample_position(step, 2, True) for step in range(100)] == [
    (step % 2, step // 2) for step in range(100)
]
assert [sample_position(step, 4, False) for step in range(10)] == [
    (0, step) for step in range(10)
]
print("Full coverage, interleaving and pilot compatibility checks passed")
