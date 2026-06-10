"""Tests for BlockCovariance: the memory-light block-diagonal estimator.

The estimator contract (partial_fit, fitted attributes, fit==stream, state roundtrip) is
covered by the parametrized suite in test_estimators.py. Here we check what is special:
block-diagonal structure, positive-definiteness, sub-quadratic state, and JSON state.
"""
from __future__ import annotations

import json

import numpy as np

from precise import BlockCovariance, all_estimators


def _data(n=300, p=24, seed=0):
    return np.random.default_rng(seed).standard_normal((n, p))


def test_registered():
    assert BlockCovariance in all_estimators()


def test_block_diagonal_and_pd():
    p, nb = 24, 4
    e = BlockCovariance(n_blocks=nb, r=0.05).fit(_data(p=p))
    C = e.covariance_
    # off-block entries are exactly zero
    block_id = np.empty(p, dtype=int)
    for bi, idx in enumerate(np.array_split(np.arange(p), nb)):
        block_id[idx] = bi
    off_block = block_id[:, None] != block_id[None, :]
    assert np.all(C[off_block] == 0.0)
    # positive-definite by construction (block-diagonal of PD blocks)
    assert np.all(np.linalg.eigvalsh(C) > 0)


def test_state_is_subquadratic():
    # the running state must scale with block size, not store a dense p x p matrix
    p, nb = 120, 6
    e = BlockCovariance(n_blocks=nb).fit(_data(n=400, p=p))
    state = e.get_state()
    block_elems = sum(np.asarray(c).size for c in state["block_covs"])
    assert block_elems < p * p          # e.g. 6 blocks of 20 -> 2400 << 14400
    assert "block_covs" in state and len(state["block_covs"]) == nb


def test_state_is_json_serializable_and_roundtrips():
    e = BlockCovariance(n_blocks=4).fit(_data())
    state = e.get_state()
    json.loads(json.dumps(state))                       # fully JSON-serializable
    restored = BlockCovariance().set_state(state)
    assert np.allclose(restored.covariance_, e.covariance_, atol=1e-12)


def test_blocks_match_within_block_ewa():
    # each block equals an EwaCovariance fit on that block alone
    from precise import EwaCovariance
    p, nb, r = 24, 4, 0.05
    X = _data(p=p)
    C = BlockCovariance(n_blocks=nb, r=r).fit(X).covariance_
    a, b = np.array_split(np.arange(p), nb)[0][[0, -1]]
    b += 1
    Cblk = EwaCovariance(r=r).fit(X[:, a:b]).covariance_
    assert np.allclose(C[a:b, a:b], Cblk, atol=1e-10)
