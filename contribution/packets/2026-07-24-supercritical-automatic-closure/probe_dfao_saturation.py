#!/usr/bin/env python3
"""Target 3 kill criterion: does the complexity method saturate as automaton
size grows?

A 2-automatic word is a letter-coding of the fixed point of a 2-uniform
morphism on the DFAO's state set (Cobham).  A DFAO (Q, delta, q0, tau)
reading binary MSB-first with delta(q0,0)=q0 gives sigma(s)=delta(s,0)delta(s,1)
with sigma(q0)[0]=q0, so u = lim sigma^t(q0) exists and q = tau(u).

If q is the parity transcript of a DIVERGENT positive orbit then q is
aperiodic and Phi(q) is a positive integer, so:
  * drift wall  : liminf s_L/L >= alpha, but liminf <= B = f(l)/l, so B > alpha;
  * Corollary 7 : C >= alpha/(B - alpha).
A word with B < alpha, or with C*(B-alpha) < alpha, is therefore not the
transcript of a divergent orbit.  No periodicity test is needed.

Reports, per number of states d, how many words each route kills and what the
complexity constant looks like against the threshold.
"""

import importlib.util
import os
import sys
import time
from fractions import Fraction
from itertools import product

PKT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "verify_supercritical_closure.py")
_spec = importlib.util.spec_from_file_location("vsac", PKT)
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)

M0 = int(os.environ.get("T3_M0", "96"))
ELL = int(os.environ.get("T3_ELL", "512"))
DEDUP = 256


def morphisms(d):
    """2-uniform morphisms on {0..d-1} with sigma(0)[0] = 0."""
    others = list(product(range(d), repeat=2))
    for first in range(d):
        for rest in product(others, repeat=d - 1):
            yield ((0, first),) + rest


def codings(d):
    for mask in range(1, 2 ** d - 1):          # nonconstant only
        yield tuple((mask >> a) & 1 for a in range(d))


def analyse_d(d, budget=None):
    t0 = time.time()
    R = 0
    while 2 ** R < max(2 * M0 + 1, ELL):
        R += 1
    kR = 2 ** R
    seen = set()
    n_words = 0
    killed_drift = 0
    killed_cor7 = 0
    survivors = []
    ratios = []                                 # (C_bound, B, threshold)
    for sigma in morphisms(d):
        # u depends only on sigma; complexity bound likewise
        base = V.fixed_point_prefix(sigma, 0, max(DEDUP, ELL))
        blocks = None
        cbound = None
        for cod in codings(d):
            word = tuple(cod[a] for a in base)
            key = word[:DEDUP]
            if key in seen:
                continue
            seen.add(key)
            n_words += 1
            if blocks is None:
                blocks = V.window_blocks(sigma, 0, R)
                cbound, _ = V.complexity_bound(blocks, kR, 2, M0)
                cbound = V.round_up_frac(cbound, 64)
            f = V.max_factor_ones(blocks, kR, cod, ELL)
            B = Fraction(f, ELL)
            if V.cmp_frac_alpha(B) < 0:         # B < alpha
                killed_drift += 1
                continue
            fired, _ = V.kill_density(cbound, B)
            thr = None
            if fired:
                killed_cor7 += 1
            else:
                survivors.append((sigma, cod, str(B), str(cbound)))
            ratios.append((cbound, B))
        if budget and time.time() - t0 > budget:
            return None
    return {"d": d, "words": n_words, "killed_drift": killed_drift,
            "killed_cor7": killed_cor7, "survivors": survivors,
            "ratios": ratios, "secs": round(time.time() - t0, 1)}


def main():
    dmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    for d in range(2, dmax + 1):
        r = analyse_d(d)
        if r is None:
            print(f"d={d}: budget exceeded")
            break
        nsurv = len(r["survivors"])
        # saturation diagnostic: among supercritical words, how does the
        # proved C compare with the threshold alpha/(B-alpha)?
        sup = [(c, B) for c, B in r["ratios"]]
        maxc = max((c for c, _ in sup), default=Fraction(0))
        print(f"d={d}: distinct words={r['words']:7d}  "
              f"killed_by_drift={r['killed_drift']:7d}  "
              f"killed_by_cor7={r['killed_cor7']:6d}  "
              f"SURVIVORS={nsurv:5d}  max C bound={maxc}  "
              f"[{r['secs']}s]", flush=True)
        for s in r["survivors"][:6]:
            print(f"     survivor sigma={s[0]} coding={s[1]} B={s[2]} C<={s[3]}")
        if nsurv > 6:
            print(f"     ... and {nsurv-6} more")


if __name__ == "__main__":
    main()
