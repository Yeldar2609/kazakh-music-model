#!/usr/bin/env python
"""Run upstream ACE-Step-1.5 train.py unchanged, with its path-safety root set to our tensor dir.

Upstream acestep/training/path_safety.py fixes the safe root to the working directory at import
time (the upstream clone), so a tensor dir under KMM_WORK (e.g. C:\\kmm\\work\\tensors_train) is
rejected with "Path escapes safe root" and training ends after 0 steps. set_safe_root() is
upstream's own override hook; we point it at the --dataset-dir value only, so the check still
guards everything the data module reads.

Usage (the train_adapter wrappers call this; cwd must be upstream/ACE-Step-1.5):
    python ../../scripts/sidestep_train.py --yes --plain fixed --dataset-dir <tensor_dir> ...
"""

import os
import runpy
import sys

UPSTREAM = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "upstream", "ACE-Step-1.5")


def main():
    argv = sys.argv[1:]
    if "--dataset-dir" not in argv:
        sys.exit("sidestep_train.py: --dataset-dir is required")
    tensor_dir = os.path.abspath(argv[argv.index("--dataset-dir") + 1])
    if not os.path.isdir(tensor_dir):
        sys.exit(f"sidestep_train.py: tensor dir not found: {tensor_dir}")

    sys.path.insert(0, UPSTREAM)
    from acestep.training import path_safety

    path_safety.set_safe_root(tensor_dir)
    print(f"[sidestep_train] path-safety root -> {path_safety.get_safe_root()}")

    sys.argv = [os.path.join(UPSTREAM, "train.py")] + argv
    runpy.run_path(sys.argv[0], run_name="__main__")


if __name__ == "__main__":
    main()
