#!/usr/bin/env python3
"""
One-off benchmark for common hosh operations.
Run once from the project root. It inserts `src` on sys.path so it can import the package.

Usage:
    python3 bench_hosh.py [--loops N] [--batches B]

Defaults:
    --loops 10000   : number of repetitions for cheap ops (loops ops use fewer iterations)
    --batches 5     : number of repeated batches; the best batch will be chosen

This script is intentionally simple and prints human-readable timing results.
"""
#  Copyright (c) 2026. Davi Pereira dos Santos
#  This file is part of the hosh project.
#  Please respect the license - more about this in the section (*) below.
#
#  hosh is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  hosh is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with hosh.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.

import sys
import os
import time
import argparse

# Make sure src is importable when running from project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from hosh import Hosh

def timeit(fn, repeats):
    # Measure each iteration separately and return total time and best (minimum) single-run time.
    best = float("inf")
    t0 = time.perf_counter()
    for _ in range(repeats):
        s = time.perf_counter()
        fn()
        e = time.perf_counter()
        dur = e - s
        if dur < best:
            best = dur
    t1 = time.perf_counter()
    total = t1 - t0
    return total, best

def main():
    p = argparse.ArgumentParser(description="Simple one-off benchmark for hosh operations")
    p.add_argument("--loops", type=int, default=20000, help="Number of repetitions for cheap ops (default: 1000)")
    p.add_argument("--batches", type=int, default=5, help="Number of batches to run; the best batch will be chosen (default: 5)")
    args = p.parse_args()

    loops = max(1, args.loops)
    batches = max(1, args.batches)


    a = Hosh(b"benchmark-a")
    b = Hosh(b"benchmark-b")
    c = Hosh(b"benchmark-c")
    id_a = a.id

    ops = [
        ("Hosh(b'...') create", lambda: Hosh(b"bench-blob"), loops),
        ("Hosh.fromid(id)", lambda: Hosh.fromid(id_a), loops),
        ("Hosh.fromn(int)", lambda: Hosh.fromn(1234567890123456789), loops),
        ("multiply a * b", lambda: a * b, loops),
        ("multiply chain a*b*c", lambda: a * b * c, loops),
        ("divide a / b", lambda: a / b, loops),
        ("invert ~a", lambda: ~a, loops),
        ("negate -a", lambda: -a, loops),
        ("add a + b", lambda: a + b, loops),
        ("sub a - b", lambda: a - b, loops),
        ("pow a ** b", lambda: a ** b, loops),
        ("root a.root(3)", lambda: a.root(3), loops),
        ("repr(a)", lambda: repr(a), loops),
        ("str(a)", lambda: str(a), loops),
        ("bits property", lambda: a.bits, loops),
        ("sid property", lambda: a.sid, loops),
        ("ansi property", lambda: a.ansi, loops),
        ("components list(a[:,3]) first time", lambda: list(a[:, 3]), loops),
        ("components list(a[:,3]) second time (memo)", lambda: list(a[:, 3]), loops),
    ]

    print(f"Running simple Hosh micro-benchmarks. loops={loops}  batches={batches}\n")

    # Run `batches` full runs, collecting per-op best times for each batch.
    all_batches = []  # list of lists: per-batch list of (name, reps, best_sec, error)

    for batch_index in range(batches):
        batch_results = []
        for name, fn, rep in ops:
            try:
                total_sec, best_sec = timeit(fn, rep)
                # store both total (sum across repeats) and best (min single-run)
                batch_results.append((name, rep, total_sec, best_sec, None))
            except Exception as e:
                # Record error and set totals to infinity so this batch is unlikely to be chosen
                batch_results.append((name, rep, float('inf'), float('inf'), str(e)))
        all_batches.append(batch_results)

    # Choose the best evaluation for each operation (minimum total time across batches).
    print(f"Best of {batches} evaluations (each evaluation: {loops} runs). Value is mean time per op in the best batch.")

    num_ops = len(ops)
    for i in range(num_ops):
        # Get results for this op across all batches
        # batch is a list of results, result is (name, rep, total_sec, best_sec, err)
        op_results = [batch[i] for batch in all_batches]

        # Filter out errors
        valid_results = [r for r in op_results if r[4] is None]

        if not valid_results:
            # All failed
            name = op_results[0][0]
            err = op_results[0][4]
            print(f"{name:45s}: ERROR -> {err}")
            continue

        # Find best by total_sec (the value of the evaluation)
        best_res = min(valid_results, key=lambda r: r[2])
        name, rep, total_sec, best_single, _ = best_res

        print(f"{name:45s}: {total_sec / loops*1000000:.6f} us")

    print("\nDone.")

if __name__ == "__main__":
    main()
