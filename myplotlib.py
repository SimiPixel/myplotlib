import matplotlib
import matplotlib.pyplot as plt


def set_size(width, fraction=1, subplots=(1, 1)):
    """Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float or string
            Document width in points, or string of predined document type
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    if width == "thesis":
        width_pt = 426.79135
    elif width == "beamer":
        width_pt = 307.28987
    else:
        width_pt = width

    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**0.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    return (fig_width_in, fig_height_in)


def set_size_dl(width, height=None, ratio=None, texWidth=None):
    _texWidth = 443.863
    if texWidth:
        textwidth_pt = texWidth  # get this from LaTeX using \the\textwidth
    else:
        textwidth_pt = _texWidth
    inches_per_pt = 1.0 / 72.27  # convert pt to inch
    fig_width = textwidth_pt * inches_per_pt * width  # width in inches
    if height is None:
        if ratio is None:
            ratio = 2.0 / (5.0**0.5 - 1.0)  # golden mean
        fig_height = fig_width / ratio  # height in inches
    else:
        fig_height = textwidth_pt * inches_per_pt * height
    return fig_width, fig_height


_preamble = r"""
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{mathtools}
\usepackage{amsmath}
\usepackage{amssymb}
"""


def use_pgf():
    matplotlib.use("pgf")
    matplotlib.rcParams.update(
        {
            "pgf.preamble": _preamble,
            "pgf.texsystem": "pdflatex",
        }
    )


def use_tex_fonts(usetex: bool = True):
    matplotlib.rcParams.update(
        {
            # Use LaTeX to write all text
            "text.usetex": usetex,
            "font.family": "serif",
            "font.serif": [],  # use default fonts
            "font.sans-serif": [],  # use default fonts
            "font.monospace": [],  # use default fonts
            # Use 10pt font in plots, to match 10pt font in document
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "font.size": 10,
            # Make the legend/label fonts a little smaller
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            # Use system fonts when rendering SVGs.
            "svg.fonttype": "none",
        }
    )


def use_thin_lines():
    matplotlib.rcParams.update(
        {
            # Decrease lineweidths to match thinner TeX lettering.
            "axes.linewidth": 0.1,
            "lines.linewidth": 0.5,
        }
    )


def use_style_and_tex_fonts(usetex: bool = True, use_light_grid: bool = True):
    use_tex_fonts(usetex)
    if use_light_grid:
        use_lighter_grid()


def use_lighter_grid():
    matplotlib.rcParams.update(
        {
            # corresponds to default b0b0b0 with grid.alpha=0.3,
            # but looks better
            "grid.color": "e7e7e7",
        }
    )


def savefig(filename: str, transparent=True, dpi=300, tight=True):
    kwargs = dict()
    format = filename.split(".")[-1]
    if format in ["jpg", "png"]:
        kwargs.update(dict(dpi=dpi))
    if tight:
        kwargs.update(dict(bbox_inches="tight"))

    plt.savefig(filename, format=format, transparent=transparent, **kwargs)
