"""Astro Science Portfolio — AstronomicAL plugin entry point.

The plugin exposes read-only panels over the astro-science research workspace
(catalogues, interactive figures, notebooks/reports and pipeline status).  Heavy
files are loaded lazily by ``panels.py``; this module only declares the
manifest and wires panel factories, keeping plugin enablement cheap.
"""

from __future__ import annotations

from astronomicAL.platform.plugins import PluginManifest


manifest = PluginManifest(
    id="astro.science.portfolio",
    name="Astro Science Portfolio",
    version="0.1.0",
    description=(
        "Read-only research portfolio panels for the astro-science workspace: "
        "project overview, catalogue browser, interactive figure gallery, "
        "notebook/report index and automation pipeline status."
    ),
    author="astro-science",
    capabilities=["panel"],
    tags=["astro", "portfolio", "research"],
)


def register(api) -> None:
    # Import inside register: keeps manifest discovery free of pandas/panel IO.
    from . import panels

    api.register_panel(
        id="overview",
        title="Portfolio: Overview",
        factory=panels.create_overview_panel,
        description=(
            "Hero overview of the Astro Science portfolio with metrics computed "
            "from the real datasets, notebooks, theory documents and figures."
        ),
        category="Astro Science",
        icon="dashboard",
        tags=["astro", "portfolio", "overview", "metrics"],
        default_layout={"x": 0, "y": 0, "w": 8, "h": 6},
    )

    api.register_panel(
        id="catalogs",
        title="Portfolio: Catalogues",
        factory=panels.create_catalogs_panel,
        description=(
            "Browse the twelve curated research catalogues in place: preview "
            "rows, column dictionary and a direct link to each CSV."
        ),
        category="Astro Science",
        icon="table_view",
        tags=["astro", "catalogues", "datasets", "csv"],
        default_layout={"x": 0, "y": 0, "w": 8, "h": 7},
    )

    api.register_panel(
        id="figures",
        title="Portfolio: Figures",
        factory=panels.create_figures_panel,
        description=(
            "Gallery of interactive Plotly figures, GIFs and MP4 animations from "
            "the exotic-compact-objects premium figure set, lazy-loaded on selection."
        ),
        category="Astro Science",
        icon="insights",
        tags=["astro", "figures", "plotly", "gallery"],
        default_layout={"x": 0, "y": 0, "w": 8, "h": 7},
    )

    api.register_panel(
        id="research",
        title="Portfolio: Research Index",
        factory=panels.create_research_panel,
        description=(
            "Index of notebooks, premium theory documents and research reports "
            "with an in-panel markdown reader."
        ),
        category="Astro Science",
        icon="menu_book",
        tags=["astro", "notebooks", "reports", "theory"],
        default_layout={"x": 0, "y": 0, "w": 8, "h": 7},
    )

    api.register_panel(
        id="pipeline",
        title="Portfolio: Pipeline",
        factory=panels.create_pipeline_panel,
        description=(
            "Last data-refresh, notebook-health and graph-drift run status as "
            "coloured badges with timestamps, read from the loops status file."
        ),
        category="Astro Science",
        icon="sync",
        tags=["astro", "automation", "pipeline", "status"],
        default_layout={"x": 0, "y": 0, "w": 8, "h": 5},
    )
