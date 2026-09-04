"""Shared Matplotlib styling and figure-export helpers for OrbitWorks."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import matplotlib as mpl
from cycler import cycler
from matplotlib import font_manager
from matplotlib.figure import Figure

COLORS_PYTHON = (
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
)

COLORS_MATLAB = (
    "#0072BD",
    "#D95319",
    "#EDB120",
    "#7E2F8E",
    "#77AC30",
    "#4DBEEE",
    "#A2142F",
)

COLOR_ORDERS = {
    "default": COLORS_PYTHON,
    "python": COLORS_PYTHON,
    "matlab": COLORS_MATLAB,
}


def _resolve_color_order(color_order: str | Sequence[str]) -> tuple[str, ...]:
    """Return a named palette or normalize a custom color sequence."""
    if isinstance(color_order, str):
        try:
            return COLOR_ORDERS[color_order.lower()]
        except KeyError as error:
            choices = ", ".join(sorted(COLOR_ORDERS))
            raise ValueError(
                f"Unknown color order {color_order!r}; choose one of {choices}."
            ) from error

    colors = tuple(color_order)
    if not colors:
        raise ValueError("A custom color order must contain at least one color.")
    return colors


def set_plot_options(
    fontsize: float = 14,
    grid: bool = True,
    major_ticks: bool = True,
    minor_ticks: bool = True,
    margin: float = 0.05,
    color_order: str | Sequence[str] = "matlab",
    linewidth: float = 1.25,
) -> None:
    """Apply the project-wide Matplotlib style.

    Parameters
    ----------
    fontsize:
        Base font size in points.
    grid:
        Whether major grid lines are visible.
    major_ticks:
        Whether major ticks are visible on all sides of an axes.
    minor_ticks:
        Whether minor ticks are visible.
    margin:
        Fractional data margin applied by Matplotlib axes.
    color_order:
        ``"matlab"``, ``"python"``/``"default"``, or a custom color sequence.
    linewidth:
        Default line and marker-edge width in points.
    """
    colors = _resolve_color_order(color_order)
    rc_params = {
        "text.usetex": False,
        "font.size": fontsize,
        "font.style": "normal",
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.edgecolor": "black",
        "axes.linewidth": 1.25,
        "axes.titlesize": fontsize,
        "axes.titleweight": "normal",
        "axes.titlepad": fontsize * 1.4,
        "axes.labelsize": fontsize,
        "axes.labelweight": "normal",
        "axes.labelpad": fontsize,
        "axes.xmargin": margin,
        "axes.ymargin": margin,
        "axes.zmargin": margin,
        "axes.grid": grid,
        "axes.grid.axis": "both",
        "axes.grid.which": "major",
        "axes.axisbelow": True,
        "axes.prop_cycle": cycler(color=colors),
        "grid.alpha": 1.0,
        "grid.color": "#D0D0D0",
        "grid.linestyle": "-",
        "grid.linewidth": 0.5,
        "legend.borderaxespad": 1.0,
        "legend.borderpad": 0.6,
        "legend.edgecolor": "black",
        "legend.facecolor": "white",
        "legend.labelcolor": "black",
        "legend.labelspacing": 0.3,
        "legend.fancybox": True,
        "legend.fontsize": fontsize - 2,
        "legend.framealpha": 1.0,
        "legend.handleheight": 0.7,
        "legend.handlelength": 1.25,
        "legend.handletextpad": 0.8,
        "legend.markerscale": 1.0,
        "legend.numpoints": 1,
        "lines.linewidth": linewidth,
        "lines.markersize": 4.5,
        "lines.markeredgewidth": linewidth,
        "lines.markerfacecolor": "white",
        "xtick.direction": "in",
        "xtick.labelsize": fontsize - 1,
        "xtick.bottom": major_ticks,
        "xtick.top": major_ticks,
        "xtick.major.size": 6,
        "xtick.major.width": 1.25,
        "xtick.minor.size": 3,
        "xtick.minor.width": 0.75,
        "xtick.minor.visible": minor_ticks,
        "ytick.direction": "in",
        "ytick.labelsize": fontsize - 1,
        "ytick.left": major_ticks,
        "ytick.right": major_ticks,
        "ytick.major.size": 6,
        "ytick.major.width": 1.25,
        "ytick.minor.size": 3,
        "ytick.minor.width": 0.75,
        "ytick.minor.visible": minor_ticks,
        "figure.constrained_layout.use": True,
        "savefig.dpi": 500,
    }
    mpl.rcParams.update(rc_params)


def print_installed_fonts() -> None:
    """Print the font files available to Matplotlib."""
    for font in sorted(font_manager.findSystemFonts(fontext="ttf")):
        print(font)


def print_rc_parameters(filename: str | Path | None = None) -> None:
    """Print active Matplotlib parameters and optionally write them to a file."""
    rendered = "\n".join(f"{key}: {value}" for key, value in mpl.rcParams.items())
    print(rendered)
    if filename is not None:
        Path(filename).write_text(f"{rendered}\n", encoding="utf-8")


def savefig_in_formats(
    figure: Figure,
    path_without_extension: str | Path,
    formats: Sequence[str] = (".png", ".svg", ".eps"),
    dpi: int = 500,
) -> None:
    """Save a Matplotlib figure in one or more raster or vector formats."""
    allowed_formats = {".png", ".svg", ".pdf", ".eps"}
    requested_formats = tuple(formats)
    invalid_formats = set(requested_formats) - allowed_formats
    if invalid_formats:
        invalid = ", ".join(sorted(invalid_formats))
        allowed = ", ".join(sorted(allowed_formats))
        raise ValueError(f"Unsupported formats: {invalid}. Allowed formats: {allowed}.")

    base_path = Path(path_without_extension)
    for extension in requested_formats:
        options = {"dpi": dpi} if extension == ".png" else {}
        figure.savefig(
            base_path.with_suffix(extension),
            bbox_inches="tight",
            **options,
        )
