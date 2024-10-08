import matplotlib
import matplotlib.pyplot as plt

_default_width_pt = 426.79135
_default_file_format = "pdf"

_width_pt = _default_width_pt
_file_format = _default_file_format


_preamble1 = r"""
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}

\usepackage{mathtools}
\usepackage{amsmath}
\usepackage{amssymb}
"""

_preamble2 = r"""
\usepackage{siunitx}

% Define some colors used in CDC
\usepackage{xcolor}
% salmon = #FA8072
\definecolor{salmon}{RGB}{250, 128, 114}
\definecolor{salmonDarker}{RGB}{184, 61, 48}
% lightblue = #7BC8F6
\definecolor{lightblue}{RGB}{123, 200, 246}
\definecolor{lightblueDarker}{RGB}{39, 105, 143}
% green = #008000
\definecolor{green}{RGB}{0, 128, 0}
% blue = #0343DF
\definecolor{blue}{RGB}{3, 67, 223}

% then use these colors with
% \textcolor{salmon}{Loreum ips ...}
"""


def _make_preamble(font: str):
    if font == "times":
        # Use Times font for text and math
        _preamble_font = r"\usepackage{txfonts}"
    elif font == "lmodern":
        _preamble_font = r"\usepackage{lmodern}"
    elif font == "kp":
        _preamble_font = r"\usepackage[largesmallcaps,intlimits,widermath]{kpfonts}"
    else:
        raise NotImplementedError

    return _preamble1 + _preamble_font + _preamble2


def setup(
    width_pt: float = _default_width_pt,
    font: str = "lmodern",
    major_fontsize: int = 10,
    minor_fontsize: int = 8,
    light_grid: bool = True,
    thin_lines: bool = False,
    latex_custom_cmds: str = r"",
    default_file_format: str = _default_file_format,
):
    """Setup matplotlib to be consistent with your .tex document.

    Args:
        width_pt (float, optional): The page width in .tex document.
            Defaults to _default_width_pt.
        font (str, optional): The font used in your .tex document.
            Defaults to "Computer Modern with Serifs".
        major_fontsize (int, optional): The font size used in your
            .tex document. Defaults to 10.
        minor_fontsize (int, optional): A slighlty smaller font size than the
            fontsize of your .tex document. Defaults to 8.
        light_grid (bool, optional): Prettier grid lines. Defaults to True.
        thin_lines (bool, optional): Thinner axes lines.
            Defaults to False.
        latex_custom_cmds (str, optional): The latex preamble to include
            when rendering labels. Defaults to an empty string.
        default_file_format (str, optional): Default file format used by
            `savefig` when not explicitly given in filename.
            Defaults to _default_file_format.
    """
    global _file_format, _width_pt
    _file_format = default_file_format
    _width_pt = width_pt

    matplotlib.use("pgf")

    matplotlib.rcParams.update(
        {
            # Use LaTeX to write all text
            "text.usetex": True,
            "font.family": "serif",
            # "font.serif": [],  # use default fonts
            # "font.sans-serif": [],  # use default fonts
            # "font.monospace": [],  # use default fonts
            # Use 10pt font in plots, to match 10pt font in document
            "axes.labelsize": major_fontsize,
            "axes.titlesize": major_fontsize,
            "font.size": major_fontsize,
            # Make the legend/label fonts a little smaller
            "legend.fontsize": minor_fontsize,
            "xtick.labelsize": minor_fontsize,
            "ytick.labelsize": minor_fontsize,
            # Use system fonts when rendering SVGs.
            "svg.fonttype": "none",
            "pgf.preamble": _make_preamble(font) + latex_custom_cmds,
            "pgf.texsystem": "pdflatex",
            "pgf.rcfonts": False,  # Do not override LaTeX font settings
        }
    )

    if thin_lines:
        _use_thin_lines()

    if light_grid:
        _use_lighter_grid()


golden_ratio = 2.0 / (5**0.5 - 1)
inches_per_pt = 1 / 72.27


def figsize(
    fraction: float = 1.0,
    ratio: float = golden_ratio,
    subplots=(1, 1),
):
    """Set figure dimensions to avoid scaling in LaTeX.

    fraction: float, optional
            Fraction of the latex page width which you wish the figure to occupy
    ratio: float, optional
            The ratio of width / height of each subplot of the figure
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """

    # Figure width in inches
    fig_width_in = _width_pt * inches_per_pt * fraction
    # Figure height in inches
    n_rows, n_cols = subplots
    fig_height_in = fig_width_in * n_rows / (ratio * n_cols)

    return fig_width_in, fig_height_in


def savefig(filename: str, transparent=True, dpi=300, tight=True):
    """Saves the current matplotlib figure.

    Args:
        filename (str): Name of the file
        transparent (bool, optional): Make background transparent. Defaults to True.
        dpi (int, optional): DPI of non-vectorized graphics. Defaults to 300.
        tight (bool, optional): Enables tight figure padding. Defaults to True.
    """
    kwargs = dict()
    split = filename.split(".")
    if len(split) == 2:
        filename, format = split
    elif len(split) == 1:
        format = _file_format
    else:
        raise Exception(
            f"The fileformat could not be uniquely infered from the filename={filename}"
        )

    if format in ["jpg", "png"]:
        kwargs.update(dict(dpi=dpi))
    if tight:
        kwargs.update(dict(bbox_inches="tight"))

    plt.savefig(
        filename + "." + format, format=format, transparent=transparent, **kwargs
    )


def _use_thin_lines():
    matplotlib.rcParams.update(
        {
            # Decrease lineweidths to match thinner TeX lettering.
            "axes.linewidth": 0.1,
            "lines.linewidth": 0.5,
        }
    )


_light_grid_params = {
    # corresponds to default b0b0b0 with grid.alpha=0.3,
    # but looks better
    "grid.color": "e7e7e7",
}


def _use_lighter_grid():
    matplotlib.rcParams.update(_light_grid_params)


def utils_adjust_ligher_grid(alpha: float):
    global _light_grid_params
    _light_grid_params = {"grid.color": "b0b0b0", "grid.alpha": alpha}
    _use_lighter_grid()


def utils_add_second_xaxis(ax):
    """Adds a second x-axis on top frame of figure"""
    ax2 = ax.twiny()
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xbound(ax.get_xbound())
    return ax2


def utils_add_second_yaxis(ax):
    """Adds a second y-axis on right frame of figure"""
    ax2 = ax.twinx()
    ax2.set_yticks(ax.get_yticks())
    ax2.set_ybound(ax.get_ybound())
    return ax2


def utils_matplotlib_default_colors() -> list[str]:
    """Defaults colors used by matplotlib"""
    return plt.rcParams["axes.prop_cycle"].by_key()["color"]


def utils_hide_frame(ax, sides=[0, 1, 2, 3]):
    """Hides the framewires around the figure.
    E.g. [1, 3] hides upper-right axes
    y |_
       x
    """
    for i, spine in enumerate(ax.spines.values()):
        if i not in sides:
            continue
        spine.set_visible(False)
