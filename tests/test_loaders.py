import pandas as pd
from yieldcurve.loaders.gsw import load_gsw_params, load_gsw_zeros
from yieldcurve.loaders.fred import load_par_yields

"""Tests for loaders against frozen fixtures in tests/fixtures

Fixtures are 30 line slices of raw files , committed to git
Every asserted value below was read from the fixture by eye first 
the assert pins what the parser MUST produce from those exact bytes"""

FIXTURES = "tests/fixtures"

def test_gsw_sentinel_to_nan():
    p = load_gsw_params(raw_dir=FIXTURES)
    first_row_tau2 = p.loc["1961-06-14", "TAU2"]

    assert pd.isna(first_row_tau2)

def test_gsw_skiprows_and_columns():
    p = load_gsw_params(raw_dir=FIXTURES)

    assert p.index[0] == pd.Timestamp("1961-06-14")
    assert list(p.columns) == ["BETA0","BETA1","BETA2","BETA3","TAU1","TAU2"]

def test_gsw_zeros_tenor_columns():
    z = load_gsw_zeros(raw_dir=FIXTURES)
    
    assert list(z.columns) == [float(i) for i in range(1,31)]
    assert z.loc["1961-06-14",1.0] == 2.9825

def test_par_yields_parses_values():
    par = load_par_yields(raw_dir=FIXTURES)

    assert len(par.columns) == 11
    assert list(par.columns) == [1/12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    assert par.loc["1962-01-02", 10.0] == 4.06

def test_par_missing_value_is_nan():
    par = load_par_yields(raw_dir=FIXTURES)

    assert pd.isna(par.loc["1969-07-21",7.0])