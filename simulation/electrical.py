"""
Electrical helpers for the EnergyMind simulated layer (notebook 04, reused by 05).

Conventions (kept identical everywhere in the project)
    V : line-to-line voltage in volts
    I : line current in amperes
    P : active power in kW
    PF: power factor (dimensionless, 0 to 1)
    f : frequency in Hz
Balanced three-phase relation:  P[kW] * 1000 = sqrt(3) * V * I * PF
"""
import numpy as np
from scipy.signal import lfilter

SQRT3 = np.sqrt(3.0)


def load_profile(dt, daily_amp, peak_hour, weekend_factor, seasonal_amp, seasonal_peak_doy):
    """Multiplicative load profile (daily x weekly x seasonal), normalised to mean 1.

    dt must be a pandas DatetimeIndex of length T. Returns an array of shape (T,).
    """
    hour = dt.hour.values + dt.minute.values / 60.0
    daily = 1.0 + daily_amp * np.cos(2 * np.pi * (hour - peak_hour) / 24.0)
    weekly = np.where(dt.dayofweek.values >= 5, weekend_factor, 1.0)
    seasonal = 1.0 + seasonal_amp * np.cos(2 * np.pi * (dt.dayofyear.values - seasonal_peak_doy) / 365.0)
    prof = daily * weekly * seasonal
    return prof / prof.mean()


def ar1(n, phi, sigma_stationary, rng, burn_in=500):
    """Zero-mean AR(1) series of length n with the given stationary standard deviation."""
    sigma_eps = sigma_stationary * np.sqrt(1.0 - phi ** 2)
    eps = rng.standard_normal(n + burn_in) * sigma_eps
    x = lfilter([1.0], [1.0, -phi], eps)
    return x[burn_in:]


def power_factor(load_factor, intercept, slope, clip):
    """Induction-motor power factor: low at light load, higher near full load."""
    return np.clip(intercept + slope * load_factor, clip[0], clip[1])


def current_from_power(p_kw, v, pf):
    """Line current (A) drawn by a constant-power load: I = P / (sqrt(3) V PF)."""
    return p_kw * 1000.0 / (SQRT3 * v * pf)


def power_from_vi(v, i, pf):
    """Active power (kW) from line voltage, line current and power factor."""
    return SQRT3 * v * i * pf / 1000.0