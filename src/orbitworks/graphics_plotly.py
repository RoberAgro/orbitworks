"""Shared Plotly template and figure styling helpers for OrbitWorks."""

from __future__ import annotations

from collections.abc import Sequence

import plotly.graph_objects as go
import plotly.io as pio

from orbitworks.graphics_mpl import COLOR_ORDERS

TEMPLATE_NAME = "orbitworks"


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


def build_template(
    fontsize: float = 14,
    grid: bool = True,
    color_order: str | Sequence[str] = "matlab",
    linewidth: float = 1.25,
) -> go.layout.Template:
    """Build the project-wide Plotly template without modifying global state."""
    colors = _resolve_color_order(color_order)
    axis = {
        "showgrid": grid,
        "gridcolor": "#D0D0D0",
        "gridwidth": 0.5,
        "showline": True,
        "linecolor": "black",
        "linewidth": 1.25,
        "mirror": "ticks",
        "ticks": "inside",
        "tickfont": {"size": fontsize - 1},
        "title": {"font": {"size": fontsize}, "standoff": fontsize},
        "zeroline": False,
    }
    return go.layout.Template(
        layout=go.Layout(
            autosize=True,
            colorway=list(colors),
            font={
                "family": "Times New Roman, Times, serif",
                "size": fontsize,
                "color": "black",
            },
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin={"l": 70, "r": 30, "t": 80, "b": 60},
            title={
                "font": {"size": fontsize},
                "x": 0.5,
                "xanchor": "center",
                "pad": {"b": fontsize},
            },
            legend={
                "bgcolor": "white",
                "bordercolor": "black",
                "borderwidth": 1,
                "font": {"size": fontsize - 2},
            },
            hoverlabel={
                "bgcolor": "white",
                "bordercolor": "black",
                "font": {"family": "Times New Roman, Times, serif"},
            },
            xaxis=axis,
            yaxis=axis,
        ),
        data=go.layout.template.Data(
            scatter=[go.Scatter(line={"width": linewidth}, marker={"size": 6})],
            scattergl=[go.Scattergl(line={"width": linewidth}, marker={"size": 6})],
        ),
    )


def set_plot_options(
    fontsize: float = 14,
    grid: bool = True,
    color_order: str | Sequence[str] = "matlab",
    linewidth: float = 1.25,
    *,
    make_default: bool = True,
) -> go.layout.Template:
    """Register the OrbitWorks template and optionally make it Plotly's default."""
    template = build_template(
        fontsize=fontsize,
        grid=grid,
        color_order=color_order,
        linewidth=linewidth,
    )
    pio.templates[TEMPLATE_NAME] = template
    if make_default:
        pio.templates.default = f"plotly_white+{TEMPLATE_NAME}"
    return template


def apply_plot_options(
    figure: go.Figure,
    *,
    equal_aspect: bool = False,
) -> go.Figure:
    """Apply the registered style and optional equal orbital-axis scaling."""
    if TEMPLATE_NAME not in pio.templates:
        set_plot_options(make_default=False)
    figure.update_layout(template=f"plotly_white+{TEMPLATE_NAME}")
    if equal_aspect:
        figure.update_yaxes(scaleanchor="x", scaleratio=1)
    return figure
