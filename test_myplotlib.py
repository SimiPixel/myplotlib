import matplotlib.pyplot as plt
import numpy as np

from myplotlib import figsize, savefig, setup


def _make_figure(fraction):
    plt.figure(figsize=figsize(fraction))
    plt.plot(np.arange(10))
    plt.xlabel("A very long x-axis label. Myplotlib")


def test_getting_started():
    setup()
    _make_figure(1)
    savefig("figures/my_figure")


def test_png():
    setup()
    _make_figure(1)
    savefig("figures/my_figure.png")


def test_fontsize():
    setup(major_fontsize=8)
    _make_figure(1)
    savefig("figures/my_figure_small_major")

    setup(minor_fontsize=6)
    _make_figure(1)
    savefig("figures/my_figure_small_minor")


def test_font_family():
    setup(font_family="arial")
    _make_figure(1)
    savefig("figures/my_figure_arial")

    setup(font_family="times")
    _make_figure(1)
    savefig("figures/my_figure_times")


def test_fraction():
    setup()
    _make_figure(0.5)
    savefig("figures/my_figure_halfpage")
