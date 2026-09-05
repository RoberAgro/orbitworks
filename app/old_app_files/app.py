import os
import io
import base64
import yaml
import numpy as np
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc


from datetime import datetime

from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
    State,
    ctx,
)

import turbomaps as tm


# TODO: add control over the number of speed lines?

# =========================
# Global / setup
# =========================
# app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


def main():
    app.run(debug=True)


# =========================
# Default inputs (from config.yaml)
# =========================
DEFAULTS = dict(
    # Design parameters
    flow_coefficient=0.10,
    work_coefficient=0.65,
    tip_mach_number=1.00,
    polytropic_efficiency=0.90,
    # Fluid parameters
    inlet_temperature=288.15,
    inlet_pressure=101325.0,
    heat_capacity_ratio=1.4,
    molecular_mass=28.97e-3,
    # Efficiency parameters
    A=0.50,
    B=1.15,
    C=4.50,
    flow_coefficient_ratio_low=0.50,
    flow_coefficient_ratio_high=0.90,
    D_low=2.1,
    D_high=1.7,
    H_low=2.0,
    H_high=3.5,
    G_low=2.0,
    G_high=0.3,
    blending_factor=1.0,
    # Work parameters
    slip_velocity_ratio=0.13,
    disk_friction_coefficient=0.003,
    degree_of_reaction=0.60,
    # Surge parameters
    A_s=0.0,
    B_s=1.25,
    C_s=4.75,
    flow_ratio_surge2choke_pessimistic_low=0.32,
    flow_ratio_surge2choke_pessimistic_high=0.84,
    flow_ratio_surge2choke_realistic_low=0.24,
    flow_ratio_surge2choke_realistic_high=0.80,
    flow_ratio_surge2choke_optimistic_low=0.16,
    flow_ratio_surge2choke_optimistic_high=0.75,
)

# =========================
# Documentation layout
# =========================
docs_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "docs",
    "equation_derivations.md",
)
if os.path.exists(docs_path):
    with open(docs_path, "r", encoding="utf-8") as f:
        theory_md = f.read()
else:
    theory_md = "Documentation not found."

docs_layout = html.Div(
    style={"maxWidth": "1000px", "margin": "auto", "padding": "30px"},
    children=[
        dcc.Markdown(
            theory_md,
            mathjax=True,
            style={
                "whiteSpace": "pre-wrap",
                "padding": "40px",
                "fontFamily": "Segoe UI, Roboto, Helvetica, Arial, sans-serif",
                "fontSize": "16px",
                "lineHeight": "1.6",
                "color": "#24292e",
                "backgroundColor": "#ffffff",
            },
        ),
    ],
)

# =========================
# UI helpers — identical to turbodash
# =========================
LABEL_STYLE = dict(
    fontWeight="normal",
    display="block",
    marginBottom="6px",
    marginTop="8px",
)

CONTROLS_STYLE = dict(
    width="450px",
    minWidth="450px",
    padding="30px",
    overflowY="auto",
    borderRight="1px solid #ddd",
    backgroundColor="#fdfdfd",
)


def html_section(title):
    return html.H4(
        title,
        style={
            "marginTop": "24px",
            "paddingBottom": "6px",
            "borderBottom": "1px solid #ddd",
        },
    )


def labeled(label, component):
    return html.Div([html.Label(label, style=LABEL_STYLE), component])


def input_only(label_children, id_prefix, default):
    return html.Div(
        style={"marginBottom": "16px", "marginTop": "8px"},
        children=[
            html.Label(
                label_children,
                style=LABEL_STYLE,
            ),
            dcc.Input(
                id=f"{id_prefix}_input",
                type="number",
                value=default,
                debounce=True,
                style={
                    "width": "95%",
                    "padding": "6px 8px",
                    "fontSize": "14px",
                    "borderRadius": "4px",
                    "border": "1px solid #ccc",
                    "backgroundColor": "#ffffff",
                    "boxShadow": "inset 0 1px 2px rgba(0,0,0,0.08)",
                },
            ),
        ],
    )


def linked_input(label_children, id_prefix, min_val, max_val, step, default):
    return html.Div(
        style={"marginBottom": "16px", "marginTop": "8px"},
        children=[
            html.Label(label_children, style=LABEL_STYLE),
            html.Div(
                style={"display": "flex", "alignItems": "center", "gap": "10px"},
                children=[
                    html.Div(
                        dcc.Slider(
                            id=f"{id_prefix}_slider",
                            min=min_val,
                            max=max_val,
                            step=step,
                            value=default,
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": False},
                            updatemode="drag",
                        ),
                        style={"flexGrow": "1"},
                    ),
                    dcc.Input(
                        id=f"{id_prefix}_input",
                        type="number",
                        value=default,
                        min=min_val,
                        max=max_val,
                        step=step,
                        debounce=True,
                        style={
                            "width": "85px",
                            "padding": "6px 8px",
                            "fontSize": "14px",
                            "borderRadius": "4px",
                            "border": "1px solid #ccc",
                            "backgroundColor": "#ffffff",
                            "boxShadow": "inset 0 1px 2px rgba(0,0,0,0.08)",
                        },
                    ),
                ],
            ),
        ],
    )


BUTTON_STYLE = {
    "padding": "8px 16px",
    "fontWeight": "bold",
    "fontSize": "14px",
    "borderRadius": "4px",
    "border": "1px solid #ccc",
    "backgroundColor": "#f8f9fa",
    "cursor": "pointer",
    "boxShadow": "0 1px 2px rgba(0,0,0,0.08)",
}


def save_load_row():
    return html.Div(
        [
            html.Button(
                "Save configuration",
                id="save_button",
                n_clicks=0,
                style=BUTTON_STYLE,
            ),
            dcc.Upload(
                id="load_button",
                accept=".yaml,.yml",
                children=html.Button(
                    "Load configuration",
                    style=BUTTON_STYLE,
                ),
            ),
        ],
        style=dict(display="flex", gap="12px", marginBottom="16px"),
    )


# =========================
# Design variable definitions
# =========================
DESIGN_VARS = [
    (["Flow coefficient, φ", html.Sub("d")], "flow_coefficient", 0.01, 0.30, 0.005),
    (["Work coefficient, λ", html.Sub("d")], "work_coefficient", 0.30, 1.20, 0.005),
    (["Tip Mach number, Ma", html.Sub("u,d")], "tip_mach_number", 0.20, 1.80, 0.01),
    (
        ["Polytropic efficiency, η", html.Sub("p,d")],
        "polytropic_efficiency",
        0.50,
        0.98,
        0.005,
    ),
]

FLUID_VARS = [
    (
        ["Inlet temperature, T", html.Sub("01"), " [K]"],
        "inlet_temperature",
        200.0,
        700.0,
        0.01,
    ),
    (["Inlet pressure, p", html.Sub("01"), " [Pa]"], "inlet_pressure", 1e4, 1e7, 1.0),
    (["Heat capacity ratio, γ"], "heat_capacity_ratio", 1.10, 1.67, 0.001),
    (["Molecular mass [kg/mol]"], "molecular_mass", 2e-3, 0.25, 1e-5),
]

EFFICIENCY_VARS = [
    (["Blending factor A"], "A", 0.0, 1.0, 0.01),
    (["Mach midpoint B"], "B", 0.5, 2.0, 0.01),
    (["Steepness C"], "C", 2.0, 8.0, 0.01),
    (["φ_p/φ_c low"], "flow_coefficient_ratio_low", 0.30, 0.80, 0.01),
    (["φ_p/φ_c high"], "flow_coefficient_ratio_high", 0.70, 1.00, 0.01),
    (["D low"], "D_low", 1.0, 4.0, 0.01),
    (["D high"], "D_high", 1.0, 4.0, 0.01),
    (["H low"], "H_low", 1.0, 5.0, 0.01),
    (["H high"], "H_high", 1.0, 5.0, 0.01),
    (["G low"], "G_low", 0.0, 3.0, 0.01),
    (["G high"], "G_high", 0.0, 1.5, 0.01),
    (["Stage blending factor"], "blending_factor", 0.0, 1.0, 0.01),
]

WORK_VARS = [
    (
        ["Slip velocity ratio, c", html.Sub("s"), "/u₂"],
        "slip_velocity_ratio",
        0.05,
        0.35,
        0.0001,
    ),
    (
        ["Disk friction coeff., k", html.Sub("df")],
        "disk_friction_coefficient",
        0.0,
        0.01,
        0.0001,
    ),
    (["Degree of reaction, R"], "degree_of_reaction", 0.30, 0.80, 0.0001),
]

SURGE_VARS = [
    (["Surge A", html.Sub("s")], "A_s", 0.0, 1.0, 0.01),
    (["Surge B", html.Sub("s")], "B_s", 0.5, 2.0, 0.01),
    (["Surge C", html.Sub("s")], "C_s", 2.0, 8.0, 0.01),
    (
        ["φ_s/φ_c pessimistic low"],
        "flow_ratio_surge2choke_pessimistic_low",
        0.1,
        0.6,
        0.01,
    ),
    (
        ["φ_s/φ_c pessimistic high"],
        "flow_ratio_surge2choke_pessimistic_high",
        0.5,
        1.0,
        0.01,
    ),
    (["φ_s/φ_c realistic low"], "flow_ratio_surge2choke_realistic_low", 0.1, 0.5, 0.01),
    (
        ["φ_s/φ_c realistic high"],
        "flow_ratio_surge2choke_realistic_high",
        0.5,
        1.0,
        0.01,
    ),
    (
        ["φ_s/φ_c optimistic low"],
        "flow_ratio_surge2choke_optimistic_low",
        0.05,
        0.4,
        0.01,
    ),
    (
        ["φ_s/φ_c optimistic high"],
        "flow_ratio_surge2choke_optimistic_high",
        0.4,
        0.9,
        0.01,
    ),
]

# =========================
# Controls layout
# =========================


def accordion_title(text):
    return html.Span(text, style={"fontWeight": "bold", "fontSize": "15px"})


controls = html.Div(
    style=CONTROLS_STYLE,
    children=[
        save_load_row(),
        dcc.Download(id="download_config_yaml"),
        dcc.Store(id="loaded_cfg_store"),
        dbc.Accordion(
            start_collapsed=False,
            always_open=True,
            children=[
                dbc.AccordionItem(
                    title=accordion_title("Design point parameters"),
                    children=[
                        *[
                            linked_input(lbl, key, lo, hi, step, DEFAULTS[key])
                            for lbl, key, lo, hi, step in DESIGN_VARS
                        ],
                    ],
                ),
                dbc.AccordionItem(
                    title=accordion_title("Fluid parameters"),
                    children=[
                        *[
                            linked_input(lbl, key, lo, hi, step, DEFAULTS[key])
                            for lbl, key, lo, hi, step in FLUID_VARS
                        ],
                    ],
                ),
                dbc.AccordionItem(
                    title=accordion_title("Efficiency parameters"),
                    item_id="efficiency",
                    children=[
                        *[
                            linked_input(lbl, key, lo, hi, step, DEFAULTS[key])
                            for lbl, key, lo, hi, step in EFFICIENCY_VARS
                        ],
                    ],
                ),
                dbc.AccordionItem(
                    title=accordion_title("Work coefficient parameters"),
                    item_id="work",
                    children=[
                        *[
                            linked_input(lbl, key, lo, hi, step, DEFAULTS[key])
                            for lbl, key, lo, hi, step in WORK_VARS
                        ],
                    ],
                ),
                dbc.AccordionItem(
                    title=accordion_title("Surge parameters"),
                    item_id="surge",
                    children=[
                        *[
                            linked_input(lbl, key, lo, hi, step, DEFAULTS[key])
                            for lbl, key, lo, hi, step in SURGE_VARS
                        ],
                    ],
                ),
            ],
        ),
    ],
)


# =========================
# Plots layout
# =========================
def plot_card(title, graph_id):
    return html.Div(
        style={
            "border": "1px solid #ddd",
            "borderRadius": "6px",
            "padding": "10px",
            "backgroundColor": "white",
        },
        children=[
            html.Div(title, style={"fontWeight": "bold", "marginBottom": "6px"}),
            dcc.Graph(
                id=graph_id,
                style={"height": "360px"},
                config={"responsive": True},
            ),
        ],
    )


plots = html.Div(
    style={
        "display": "grid",
        "gridTemplateColumns": "1fr 1fr",
        "gridTemplateRows": "1fr 1fr",
        "gap": "10px",
        "padding": "10px",
    },
    children=[
        plot_card("Polytropic efficiency", "efficiency_plot"),
        plot_card("Work coefficient", "work_coeff_plot"),
        plot_card("Head coefficient", "head_coeff_plot"),
        plot_card("Total pressure ratio", "pressure_ratio_plot"),
    ],
)

# =========================
# App layout
# =========================
app.layout = html.Div(
    children=[
        dcc.Tabs(
            id="tabs",
            value="calculator",
            style={
                "fontFamily": "Segoe UI, Arial, sans-serif",
                "fontSize": "16px",
                "borderBottom": "1px solid #d0d7de",
            },
            children=[
                dcc.Tab(
                    label="Turbomaps",
                    value="calculator",
                    style={
                        "fontWeight": "bold",
                        "padding": "10px 18px",
                        "backgroundColor": "#f6f8fa",
                        "border": "1px solid #d0d7de",
                        "borderBottom": "none",
                    },
                    selected_style={
                        "fontWeight": "bold",
                        "padding": "10px 18px",
                        "backgroundColor": "#ffffff",
                        "border": "1px solid #d0d7de",
                        "borderBottom": "3px solid #007acc",
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "width": "100vw",
                                "height": "100vh",
                                "overflow": "hidden",
                                "fontFamily": "Arial",
                            },
                            children=[
                                controls,
                                html.Div(
                                    style={"flex": "1 1 auto", "overflowY": "auto"},
                                    children=[plots],
                                ),
                            ],
                        )
                    ],
                ),
                dcc.Tab(
                    label="Documentation",
                    value="docs",
                    style={
                        "fontWeight": "bold",
                        "padding": "10px 18px",
                        "backgroundColor": "#f6f8fa",
                        "border": "1px solid #d0d7de",
                        "borderBottom": "none",
                    },
                    selected_style={
                        "fontWeight": "bold",
                        "padding": "10px 18px",
                        "backgroundColor": "#ffffff",
                        "border": "1px solid #d0d7de",
                        "borderBottom": "3px solid #007acc",
                    },
                    children=[docs_layout],
                ),
            ],
        )
    ]
)


# =========================
# Helper: assemble parameters dict from inputs
# =========================
def build_parameters(
    flow_coefficient,
    work_coefficient,
    tip_mach_number,
    polytropic_efficiency,
    inlet_temperature,
    inlet_pressure,
    heat_capacity_ratio,
    molecular_mass,
    A,
    B,
    C,
    flow_coefficient_ratio_low,
    flow_coefficient_ratio_high,
    D_low,
    D_high,
    H_low,
    H_high,
    G_low,
    G_high,
    blending_factor,
    slip_velocity_ratio,
    disk_friction_coefficient,
    degree_of_reaction,
    A_s,
    B_s,
    C_s,
    flow_ratio_surge2choke_pessimistic_low,
    flow_ratio_surge2choke_pessimistic_high,
    flow_ratio_surge2choke_realistic_low,
    flow_ratio_surge2choke_realistic_high,
    flow_ratio_surge2choke_optimistic_low,
    flow_ratio_surge2choke_optimistic_high,
):
    return {
        "design_parameters": {
            "flow_coefficient": flow_coefficient,
            "work_coefficient": work_coefficient,
            "tip_mach_number": tip_mach_number,
            "polytropic_efficiency": polytropic_efficiency,
        },
        "efficiency_parameters": {
            "A": A,
            "B": B,
            "C": C,
            "flow_coefficient_ratio_low": flow_coefficient_ratio_low,
            "flow_coefficient_ratio_high": flow_coefficient_ratio_high,
            "D_low": D_low,
            "D_high": D_high,
            "H_low": H_low,
            "H_high": H_high,
            "G_low": G_low,
            "G_high": G_high,
            "blending_factor": blending_factor,
        },
        "work_parameters": {
            "slip_velocity_ratio": slip_velocity_ratio,
            "disk_friction_coefficient": disk_friction_coefficient,
            "degree_of_reaction": degree_of_reaction,
        },
        "surge_parameters": {
            "A_s": A_s,
            "B_s": B_s,
            "C_s": C_s,
            "flow_ratio_surge2choke_pessimistic_low": flow_ratio_surge2choke_pessimistic_low,
            "flow_ratio_surge2choke_pessimistic_high": flow_ratio_surge2choke_pessimistic_high,
            "flow_ratio_surge2choke_realistic_low": flow_ratio_surge2choke_realistic_low,
            "flow_ratio_surge2choke_realistic_high": flow_ratio_surge2choke_realistic_high,
            "flow_ratio_surge2choke_optimistic_low": flow_ratio_surge2choke_optimistic_low,
            "flow_ratio_surge2choke_optimistic_high": flow_ratio_surge2choke_optimistic_high,
        },
        "fluid_parameters": {
            "model": "perfect_gas",
            "inlet_temperature": inlet_temperature,
            "inlet_pressure": inlet_pressure,
            "perfect_gas": {
                "heat_capacity_ratio": heat_capacity_ratio,
                "molecular_mass": molecular_mass,
            },
            "real_gas": {
                "fluid_name": "Air",
                "backend": "HEOS",
            },
        },
    }


# =========================
# Callback: compute + plot
# =========================
ALL_SLIDER_INPUTS = (
    [Input(f"{key}_slider", "value") for _, key, *_ in DESIGN_VARS]
    + [Input(f"{key}_slider", "value") for _, key, *_ in FLUID_VARS]
    + [Input(f"{key}_slider", "value") for _, key, *_ in EFFICIENCY_VARS]
    + [Input(f"{key}_slider", "value") for _, key, *_ in WORK_VARS]
    + [Input(f"{key}_slider", "value") for _, key, *_ in SURGE_VARS]
)

ALL_KEYS = (
    [key for _, key, *_ in DESIGN_VARS]
    + [key for _, key, *_ in FLUID_VARS]
    + [key for _, key, *_ in EFFICIENCY_VARS]
    + [key for _, key, *_ in WORK_VARS]
    + [key for _, key, *_ in SURGE_VARS]
)


@app.callback(
    Output("efficiency_plot", "figure"),
    Output("work_coeff_plot", "figure"),
    Output("head_coeff_plot", "figure"),
    Output("pressure_ratio_plot", "figure"),
    ALL_SLIDER_INPUTS,
)
def update_maps(*slider_values):
    values = dict(zip(ALL_KEYS, slider_values))

    if any(v is None for v in values.values()):
        import plotly.graph_objects as go

        empty = go.Figure()
        return empty, empty, empty, empty

    try:
        parameters = build_parameters(**values)
        compressor = tm.CentrifugalCompressor(parameters)

        Ma_range = np.linspace(0.5, 1.5, 100)
        flow_range = np.linspace(0.01, 1.0, 200)
        results = compressor.compute_performance_map(Ma_range, flow_range)

        N_lines = 11
        mach_colors = plt.cm.plasma(np.linspace(0.2, 0.85, N_lines))
        mach_colors = plt.cm.Blues(np.linspace(0.55, 1.00, N_lines))

        common = dict(
            show_efficiency=False,
            show_surge=True,
            show_choke=True,
            show_design_point=True,
            show_peak_points=True,
            mach_colors=mach_colors,
            N_speed_lines=N_lines,
            x_key="flow_coefficient_sonic",
            x_label="Sonic flow coefficient, φ · Ma<sub>u</sub>",
            xlim=(1e-4, None),
        )

        fig_eta = compressor.plot_performance_map_plotly(
            results,
            y_key="efficiency",
            y_label="Polytropic efficiency, η<sub>p</sub>",
            ylim=(0.0, 1.0),
            **common,
        )

        fig_work = compressor.plot_performance_map_plotly(
            results,
            y_key="work_coefficient",
            y_label="Work coefficient, λ = Δh / U²",
            ylim=(0.2, 1.0),
            **common,
        )

        fig_head = compressor.plot_performance_map_plotly(
            results,
            y_key="head_coefficient",
            y_label="Head coefficient, λ · η<sub>p</sub>",
            ylim=(0.0, None),
            **common,
        )

        fig_pr = compressor.plot_performance_map_plotly(
            results,
            y_key="pressure_ratio",
            y_label="Total pressure ratio, π = p<sub>02</sub>/p<sub>01</sub>",
            ylim=(1.0, None),
            **common,
        )

        return fig_eta, fig_work, fig_head, fig_pr

    except Exception as e:
        print(f"Error in update_maps: {e}")
        import plotly.graph_objects as go

        empty = go.Figure()
        return empty, empty, empty, empty


# =========================
# YAML save
# =========================
@app.callback(
    Output("download_config_yaml", "data"),
    Input("save_button", "n_clicks"),
    [
        State(f"{key}_slider", "value")
        for _, key, *_ in DESIGN_VARS
        + FLUID_VARS
        + EFFICIENCY_VARS
        + WORK_VARS
        + SURGE_VARS
    ],
    prevent_initial_call=True,
)
def save_config(n_clicks, *slider_values):
    values = dict(zip(ALL_KEYS, slider_values))
    parameters = build_parameters(**values)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return dict(
        content=yaml.dump(parameters, sort_keys=False, default_flow_style=False),
        filename=f"turbomaps_config_{timestamp}.yaml",
        type="text/yaml",
    )


# =========================
# YAML load
# =========================
@app.callback(
    Output("loaded_cfg_store", "data"),
    Input("load_button", "contents"),
    prevent_initial_call=True,
)
def load_config(contents):
    if contents is None:
        return {}
    _, content_string = contents.split(",")
    decoded = base64.b64decode(content_string).decode("utf-8")
    return yaml.safe_load(decoded) or {}


# =========================
# Slider <-> input sync + YAML load
# =========================
def register_link(prefix, min_val, max_val, yaml_path):
    """
    yaml_path: tuple of keys to navigate the loaded config dict,
    e.g. ("design_parameters", "flow_coefficient")
    """
    slider_id = f"{prefix}_slider"
    input_id = f"{prefix}_input"

    @app.callback(
        Output(slider_id, "value"),
        Output(input_id, "value"),
        Input(slider_id, "value"),
        Input(input_id, "value"),
        Input("loaded_cfg_store", "data"),
        prevent_initial_call=True,
    )
    def _sync(val_slider, val_input, loaded_cfg):
        trigger = ctx.triggered_id

        if trigger == "loaded_cfg_store" and loaded_cfg:
            cfg = loaded_cfg
            for key in yaml_path:
                cfg = cfg.get(key, {}) if isinstance(cfg, dict) else {}
            if isinstance(cfg, (int, float)):
                v = float(np.clip(cfg, min_val, max_val))
                return v, v

        v_slider = float(
            np.clip(val_slider if val_slider is not None else min_val, min_val, max_val)
        )
        v_input = float(
            np.clip(val_input if val_input is not None else min_val, min_val, max_val)
        )

        if trigger == slider_id:
            return v_slider, v_slider
        if trigger == input_id:
            return v_input, v_input
        return v_slider, v_input


# Register all linked sliders with their yaml paths
_YAML_PATHS = {
    "flow_coefficient": ("design_parameters", "flow_coefficient"),
    "work_coefficient": ("design_parameters", "work_coefficient"),
    "tip_mach_number": ("design_parameters", "tip_mach_number"),
    "polytropic_efficiency": ("design_parameters", "polytropic_efficiency"),
    "inlet_temperature": ("fluid_parameters", "inlet_temperature"),
    "inlet_pressure": ("fluid_parameters", "inlet_pressure"),
    "heat_capacity_ratio": ("fluid_parameters", "perfect_gas", "heat_capacity_ratio"),
    "molecular_mass": ("fluid_parameters", "perfect_gas", "molecular_mass"),
    "A": ("efficiency_parameters", "A"),
    "B": ("efficiency_parameters", "B"),
    "C": ("efficiency_parameters", "C"),
    "flow_coefficient_ratio_low": (
        "efficiency_parameters",
        "flow_coefficient_ratio_low",
    ),
    "flow_coefficient_ratio_high": (
        "efficiency_parameters",
        "flow_coefficient_ratio_high",
    ),
    "D_low": ("efficiency_parameters", "D_low"),
    "D_high": ("efficiency_parameters", "D_high"),
    "H_low": ("efficiency_parameters", "H_low"),
    "H_high": ("efficiency_parameters", "H_high"),
    "G_low": ("efficiency_parameters", "G_low"),
    "G_high": ("efficiency_parameters", "G_high"),
    "blending_factor": ("efficiency_parameters", "blending_factor"),
    "slip_velocity_ratio": ("work_parameters", "slip_velocity_ratio"),
    "disk_friction_coefficient": ("work_parameters", "disk_friction_coefficient"),
    "degree_of_reaction": ("work_parameters", "degree_of_reaction"),
    "A_s": ("surge_parameters", "A_s"),
    "B_s": ("surge_parameters", "B_s"),
    "C_s": ("surge_parameters", "C_s"),
    "flow_ratio_surge2choke_pessimistic_low": (
        "surge_parameters",
        "flow_ratio_surge2choke_pessimistic_low",
    ),
    "flow_ratio_surge2choke_pessimistic_high": (
        "surge_parameters",
        "flow_ratio_surge2choke_pessimistic_high",
    ),
    "flow_ratio_surge2choke_realistic_low": (
        "surge_parameters",
        "flow_ratio_surge2choke_realistic_low",
    ),
    "flow_ratio_surge2choke_realistic_high": (
        "surge_parameters",
        "flow_ratio_surge2choke_realistic_high",
    ),
    "flow_ratio_surge2choke_optimistic_low": (
        "surge_parameters",
        "flow_ratio_surge2choke_optimistic_low",
    ),
    "flow_ratio_surge2choke_optimistic_high": (
        "surge_parameters",
        "flow_ratio_surge2choke_optimistic_high",
    ),
}

for _, key, lo, hi, _ in (
    DESIGN_VARS + FLUID_VARS + EFFICIENCY_VARS + WORK_VARS + SURGE_VARS
):
    register_link(key, lo, hi, _YAML_PATHS[key])


if __name__ == "__main__":
    main()
