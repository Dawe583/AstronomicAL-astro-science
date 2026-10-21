"""Panel factories for the Astro Science Portfolio plugin.

Everything here is intentionally read-only: the panels render files that live in
the astro-science research workspace and never copy, rewrite, or commit them.

Heavy CSVs (for example the 50k-row Gaia wide-binary catalogue) are loaded
lazily, only when the user selects them, and cached with ``pn.cache``.
"""

from __future__ import annotations

import base64
import html as html_lib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import panel as pn

try:  # normal case: loaded as a package by the AstronomicAL plugin manager
    from .theme import CSS
except ImportError:  # pragma: no cover - direct import while developing
    from theme import CSS  # type: ignore[no-redef]

# ---------------------------------------------------------------------------
# theme
# ---------------------------------------------------------------------------

pn.extension("tabulator")

_THEME_APPLIED = False


def apply_theme() -> None:
    """Install the plugin CSS once per process."""

    global _THEME_APPLIED
    if _THEME_APPLIED:
        return
    try:
        pn.extension(raw_css=[CSS])
        _THEME_APPLIED = True
    except Exception:  # pragma: no cover - never break the host for styling
        pass


def _style_pane() -> pn.pane.HTML:
    """Inject the stylesheet into the panel DOM.

    ``pn.extension(raw_css=...)`` covers the page-level styling, but it is
    called lazily when the first portfolio panel is built.  A real ``<style>``
    element guarantees the theme also applies to sessions that were already
    rendered when the plugin loaded.
    """

    return pn.pane.HTML(
        f"<style>{CSS}</style>",
        height=0,
        min_height=0,
        margin=(0, 0, 0, 0),
        sizing_mode="stretch_width",
    )


# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------

DEFAULT_ROOT = "/home/dawe/Projects/astro-science"


def _resolve_root() -> Path:
    for candidate in (
        os.environ.get("ASTRO_SCIENCE_ROOT"),
        DEFAULT_ROOT,
        str(Path.home() / "Projects" / "astro-science"),
    ):
        if candidate and Path(candidate).expanduser().is_dir():
            return Path(candidate).expanduser()
    return Path(DEFAULT_ROOT)


ROOT = _resolve_root()
PROJECTS = ROOT / "research" / "projects"
PROJECT = PROJECTS / "exotic-compact-objects"
PROCESSED = PROJECT / "data" / "processed"
RESULTS = PROJECT / "results"
EXTERNAL = PROJECT / "data" / "external"
FIGURES = PROJECT / "premium" / "figures"
STATUS_FILE = ROOT / ".opencode" / "loops" / "latest-status.json"
STATUS_FALLBACK = ROOT / ".opencode" / "loops" / "logs" / "latest-status.json"

# Inline embedding guard: keep websocket messages reasonable.
MAX_INLINE_HTML = 12 * 1024 * 1024
MAX_INLINE_MEDIA = 12 * 1024 * 1024


# ---------------------------------------------------------------------------
# dataset registry
# ---------------------------------------------------------------------------

DATASETS: Tuple[Dict[str, Any], ...] = (
    {
        "key": "atnfpulsar",
        "label": "Atnfpulsar",
        "rows": 4503,
        "path": EXTERNAL / "atnfpulsar.csv",
        "note": "coords | 147 cols",
    },
    {
        "key": "black_melody",
        "label": "Black Melody",
        "rows": 7,
        "path": EXTERNAL / "black_melody.csv",
        "note": "coords+mag | 97 cols",
    },
    {
        "key": "changalxrb",
        "label": "Changalxrb",
        "rows": 4442,
        "path": EXTERNAL / "changalxrb.csv",
        "note": "coords | 17 cols",
    },
    {
        "key": "chanulxcat",
        "label": "Chanulxcat",
        "rows": 155,
        "path": EXTERNAL / "chanulxcat.csv",
        "note": "coords | 23 cols",
    },
    {
        "key": "dxrbs",
        "label": "Dxrbs",
        "rows": 229,
        "path": EXTERNAL / "dxrbs.csv",
        "note": "coords+mag | 47 cols",
    },
    {
        "key": "gaia_dr3_bh_candidates",
        "label": "Gaia Dr3 Bh Candidates",
        "rows": 20000,
        "path": EXTERNAL / "gaia_dr3_bh_candidates.csv",
        "note": "coords+mag | 20 cols",
    },
    {
        "key": "gaia_dr3_known_bh_systems",
        "label": "Gaia Dr3 Known Bh Systems",
        "rows": 1,
        "path": EXTERNAL / "gaia_dr3_known_bh_systems.csv",
        "note": "coords+mag | 152 cols",
    },
    {
        "key": "gaia_dr3_wide_binaries",
        "label": "Gaia Dr3 Wide Binaries",
        "rows": 50000,
        "path": EXTERNAL / "gaia_dr3_wide_binaries.csv",
        "note": "coords+mag | 22 cols",
    },
    {
        "key": "gwb_theoretical_spectra",
        "label": "Gwb Theoretical Spectra",
        "rows": 100,
        "path": EXTERNAL / "gwb_spectra" / "gwb_theoretical_spectra.csv",
        "note": "tabular | 6 cols",
    },
    {
        "key": "gwosc_gwtc_all",
        "label": "Gwosc Gwtc All",
        "rows": 391,
        "path": EXTERNAL / "gwosc_gwtc_all.csv",
        "note": "tabular | 31 cols",
    },
    {
        "key": "gwosc_o4_events",
        "label": "Gwosc O4 Events",
        "rows": 301,
        "path": EXTERNAL / "gwosc_o4_events.csv",
        "note": "tabular | 55 cols",
    },
    {
        "key": "m83xrbcxo",
        "label": "M83Xrbcxo",
        "rows": 325,
        "path": EXTERNAL / "m83xrbcxo.csv",
        "note": "coords+mag | 17 cols",
    },
    {
        "key": "m87cxo",
        "label": "M87Cxo",
        "rows": 174,
        "path": EXTERNAL / "m87cxo.csv",
        "note": "coords | 13 cols",
    },
    {
        "key": "maxi_gsc_sources",
        "label": "Maxi Gsc Sources",
        "rows": 500,
        "path": EXTERNAL / "maxi_gsc" / "maxi_gsc_sources.csv",
        "note": "tabular | 10 cols",
    },
    {
        "key": "nicer_observations",
        "label": "Nicer Observations",
        "rows": 5000,
        "path": EXTERNAL / "nicer" / "nicer_observations.csv",
        "note": "tabular | 11 cols",
    },
    {
        "key": "pulsar",
        "label": "Pulsar",
        "rows": 706,
        "path": EXTERNAL / "pulsar.csv",
        "note": "coords | 71 cols",
    },
    {
        "key": "sgraregcsc",
        "label": "Sgraregcsc",
        "rows": 318,
        "path": EXTERNAL / "sgraregcsc.csv",
        "note": "coords | 22 cols",
    },
    {
        "key": "snrgreen",
        "label": "Snrgreen",
        "rows": 295,
        "path": EXTERNAL / "snrgreen.csv",
        "note": "coords | 16 cols",
    },
    {
        "key": "swift_bat_sources",
        "label": "Swift Bat Sources",
        "rows": 1000,
        "path": EXTERNAL / "swift_bat" / "swift_bat_sources.csv",
        "note": "tabular | 11 cols",
    },
    {
        "key": "sxs_bbh_catalog",
        "label": "Sxs Bbh Catalog",
        "rows": 28,
        "path": EXTERNAL / "sxs_catalog" / "sxs_bbh_catalog.csv",
        "note": "tabular | 9 cols",
    },
    {
        "key": "ulxngcat",
        "label": "Ulxngcat",
        "rows": 107,
        "path": EXTERNAL / "ulxngcat.csv",
        "note": "coords | 14 cols",
    },
    {
        "key": "ulxrbcat",
        "label": "Ulxrbcat",
        "rows": 229,
        "path": EXTERNAL / "ulxrbcat.csv",
        "note": "coords+mag | 25 cols",
    },
    {
        "key": "vlulxcat",
        "label": "Vlulxcat",
        "rows": 119,
        "path": EXTERNAL / "vlulxcat.csv",
        "note": "coords | 15 cols",
    },
    {
        "key": "blackcat_bhxb",
        "label": "Blackcat Bhxb",
        "rows": 60,
        "path": EXTERNAL / "xray_binary_catalogs" / "blackcat_bhxb.csv",
        "note": "tabular | 11 cols",
    },
    {
        "key": "corbet_hmxb",
        "label": "Corbet Hmxb",
        "rows": 80,
        "path": EXTERNAL / "xray_binary_catalogs" / "corbet_hmxb.csv",
        "note": "tabular | 5 cols",
    },
    {
        "key": "liu_hmxb",
        "label": "Liu Hmxb",
        "rows": 114,
        "path": EXTERNAL / "xray_binary_catalogs" / "liu_hmxb.csv",
        "note": "tabular | 11 cols",
    },
    {
        "key": "liu_lmxb",
        "label": "Liu Lmxb",
        "rows": 187,
        "path": EXTERNAL / "xray_binary_catalogs" / "liu_lmxb.csv",
        "note": "tabular | 10 cols",
    },
    {
        "key": "xrbcat",
        "label": "Xrbcat",
        "rows": 229,
        "path": EXTERNAL / "xrbcat.csv",
        "note": "coords | 16 cols",
    },
    {
        "key": "agn_reverberation_masses",
        "label": "Agn Reverberation Masses",
        "rows": 86,
        "path": PROCESSED / "agn_reverberation_masses.csv",
        "note": "coords | 15 cols",
    },
    {
        "key": "blackcat_dynamical",
        "label": "Blackcat Dynamical",
        "rows": 18,
        "path": PROCESSED / "blackcat_dynamical.csv",
        "note": "mag | 51 cols",
    },
    {
        "key": "gwosc_gwtc",
        "label": "Gwosc Gwtc",
        "rows": 391,
        "path": PROCESSED / "gwosc_gwtc.csv",
        "note": "tabular | 17 cols",
    },
    {
        "key": "gwtc_recent_20_remnants",
        "label": "Gwtc Recent 20 Remnants",
        "rows": 20,
        "path": PROCESSED / "gwtc_recent_20_remnants.csv",
        "note": "tabular | 19 cols",
    },
    {
        "key": "known_compact_objects",
        "label": "Known Compact Objects",
        "rows": 10,
        "path": PROCESSED / "known_compact_objects.csv",
        "note": "tabular | 5 cols",
    },
)

    {
        "key": "exoplanets",
        "label": "Exoplanets (NASA Archive)",
        "rows": 6451,
        "path": Path("/home/dawe/Projects/astro-science/research/projects/exoplanets/data/processed/exoplanets.csv"),
        "note": "Confirmed exoplanets, 6451 rows | coords+mag | 22 cols",
    },
DATASET_BY_KEY = {item["key"]: item for item in DATASETS}
DATASET_BY_LABEL = {item["label"]: item["key"] for item in DATASETS}

RESEARCH_AREAS = (
    "Black holes & wormholes",
    "Exotic compact objects",
    "Gravitational waves",
    "AGN reverberation",
    "Early SMBH growth",
    "Quantum gravity",
)


@pn.cache(max_items=4)
def load_dataset(key: str) -> pd.DataFrame:
    """Read one catalogue from disk. Cached, bounded, and only on demand."""

    spec = DATASET_BY_KEY.get(key)
    if spec is None:
        raise KeyError(f"Unknown dataset: {key}")

    path: Path = spec["path"]
    if not path.exists():
        raise FileNotFoundError(f"Dataset file is missing: {path}")

    df = pd.read_csv(path, low_memory=False)
    return df


def _safe_row_count(key: str) -> Optional[int]:
    try:
        return int(len(load_dataset(key)))
    except Exception:
        return None


def _count_files(pattern: str) -> int:
    try:
        return sum(1 for _ in PROJECTS.glob(pattern))
    except Exception:
        return 0


def _find_files(pattern: str) -> List[Path]:
    try:
        return sorted(p for p in PROJECTS.glob(pattern) if p.is_file())
    except Exception:
        return []


def _human_size(num_bytes: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num_bytes < 1024 or unit == "GB":
            return (
                f"{num_bytes:.0f} {unit}"
                if unit in ("B", "KB")
                else f"{num_bytes:.1f} {unit}"
            )
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} GB"


def _file_uri(path: Path) -> str:
    try:
        return path.as_uri()
    except Exception:
        return "file://" + str(path)


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def _fmt_ts(value: Any) -> str:
    if value is None:
        return "unknown"
    text = str(value)
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    except Exception:
        return text


# ---------------------------------------------------------------------------
# small reusable HTML fragments
# ---------------------------------------------------------------------------


def _header_html(title: str, subtitle: str, kicker: str = "Astro Science") -> str:
    return f"""
<div class="asp-hero" style="padding:20px 24px 18px 24px;">
  <span class="asp-kicker"><span class="asp-dot"></span>{html_lib.escape(kicker)}</span>
  <h1 class="asp-title" style="font-size:28px;margin:10px 0 4px 0;">{html_lib.escape(title)}</h1>
  <p class="asp-subtitle" style="font-size:13px;">{subtitle}</p>
</div>
"""


def _note_html(message: str) -> str:
    return f'<div class="asp-note">{message}</div>'


def _mono(text: Any) -> str:
    return f'<span class="asp-mono">{html_lib.escape(str(text))}</span>'


# ---------------------------------------------------------------------------
# overview
# ---------------------------------------------------------------------------

_METRICS: Optional[Dict[str, Any]] = None


def portfolio_metrics(force: bool = False) -> Dict[str, Any]:
    """Compute headline numbers from the real files (cached per process)."""

    global _METRICS
    if _METRICS is not None and not force:
        return _METRICS

    existing = [item for item in DATASETS if item["path"].exists()]

    notebooks = _find_files("*/notebooks/*.ipynb")
    premium_docs = _find_files("*/premium/*.md")
    report_docs = _find_files("*/reports/*.md")

    figures = (
        sorted(p for p in FIGURES.glob("*") if p.is_file()) if FIGURES.is_dir() else []
    )
    figure_html = [p for p in figures if p.suffix.lower() == ".html"]
    figure_media = [
        p
        for p in figures
        if p.suffix.lower() in {".gif", ".mp4", ".png", ".jpg", ".jpeg", ".webp"}
    ]

    mtimes = [
        item["path"].stat().st_mtime for item in existing if item["path"].exists()
    ]
    snapshot = (
        datetime.fromtimestamp(max(mtimes)).strftime("%Y-%m-%d %H:%M")
        if mtimes
        else "unavailable"
    )

    _METRICS = {
        "datasets": len(existing),
        "datasets_expected": len(DATASETS),
        "gwtc_events": _safe_row_count("gwtc"),
        "agn_masses": _safe_row_count("agn_masses"),
        "notebooks": len(notebooks),
        "theory_docs": len(premium_docs) + len(report_docs),
        "premium_docs": len(premium_docs),
        "report_docs": len(report_docs),
        "figures": len(figure_html),
        "figure_media": len(figure_media),
        "figures_total": len(figures),
        "projects": len([p for p in PROJECTS.glob("*") if p.is_dir()])
        if PROJECTS.is_dir()
        else 0,
        "snapshot": snapshot,
    }
    return _METRICS


def _metric_card(label: str, value: Any, note: str, accent: str = "") -> str:
    value_text = (
        "—" if value is None else f"{value:,}" if isinstance(value, int) else str(value)
    )
    accent_class = f" asp-v-{accent}" if accent else ""
    return f"""
<div class="asp-card">
  <div class="asp-card-label">{html_lib.escape(label)}</div>
  <div class="asp-card-value{accent_class}">{html_lib.escape(value_text)}</div>
  <div class="asp-card-note">{html_lib.escape(note)}</div>
</div>
"""


class OverviewPanel:
    def __init__(self, context: Any = None, **kwargs: Any) -> None:
        self.context = context
        self._disposed = False
        self.view = pn.Column(
            _style_pane(),
            css_classes=["asp-panel", "asp-root"],
            sizing_mode="stretch_width",
            margin=(14, 16, 18, 16),
        )
        self.render()

    # -- rendering ----------------------------------------------------------
    def render(self) -> None:
        m = portfolio_metrics(force=True)

        hero = f"""
<div class="asp-hero">
  <span class="asp-kicker"><span class="asp-dot"></span>Research portfolio · live local data</span>
  <h1 class="asp-title">Astro <span class="asp-accent">Science</span></h1>
  <p class="asp-subtitle">
    An astrophysics research portfolio on black holes, wormholes, exotic compact objects,
    gravitational-wave remnants, AGN reverberation, early supermassive black hole growth and
    quantum-gravity phenomenology — reproducible notebooks, curated catalogues and
    publication-grade interactive figures, all read directly from the research workspace.
  </p>
  <div class="asp-hero-meta">
    <span class="asp-chip"><strong>{m["datasets"]}</strong> datasets</span>
    <span class="asp-chip"><strong>{m["notebooks"]}</strong> notebooks</span>
    <span class="asp-chip"><strong>{m["figures"]}</strong> interactive figures</span>
    <span class="asp-chip"><strong>{m["theory_docs"]}</strong> theory &amp; reports</span>
    <span class="asp-chip">snapshot <strong>{html_lib.escape(m["snapshot"])}</strong></span>
  </div>
</div>
"""

        cards = "".join(
            [
                _metric_card(
                    "Datasets",
                    m["datasets"],
                    f"{m['datasets_expected']} registered catalogues",
                    "cyan",
                ),
                _metric_card(
                    "GWTC events", m["gwtc_events"], "mergers in GWTC-3/O4", ""
                ),
                _metric_card(
                    "AGN masses",
                    m["agn_masses"],
                    "reverberation-mapped SMBHs",
                    "violet",
                ),
                _metric_card("Notebooks", m["notebooks"], "reproducible analyses", ""),
                _metric_card(
                    "Theory documents",
                    m["theory_docs"],
                    f"{m['premium_docs']} premium · {m['report_docs']} reports",
                    "amber",
                ),
                _metric_card(
                    "Interactive figures",
                    m["figures"],
                    f"{m['figure_media']} animations / media",
                    "cyan",
                ),
            ]
        )

        areas = "".join(
            f'<li><span class="asp-idx">{index:02d}</span>{html_lib.escape(area)}</li>'
            for index, area in enumerate(RESEARCH_AREAS, start=1)
        )

        metrics = f'<div class="asp-metrics">{cards}</div>'

        left = f"""
<div class="asp-section">
  <div class="asp-section-title">Research areas</div>
  <ul class="asp-areas">{areas}</ul>
</div>
"""

        right = f"""
<div class="asp-section">
  <div class="asp-section-title">Workspace</div>
  <div class="asp-kv">
    <div class="k">Root</div><div class="v">{html_lib.escape(str(ROOT))}</div>
    <div class="k">Projects</div><div class="v">{m["projects"]} research projects</div>
    <div class="k">Catalogues</div><div class="v">{html_lib.escape(_rel(PROCESSED))}</div>
    <div class="k">Figures</div><div class="v">{html_lib.escape(_rel(FIGURES))}</div>
    <div class="k">Pipeline</div><div class="v">{html_lib.escape(_rel(STATUS_FILE))}</div>
    <div class="k">Mode</div><div class="v">read-only · lazy loading</div>
  </div>
</div>
"""

        footer = (
            f'<div class="asp-footer">Astro Science Portfolio · plugin '
            f'<span class="asp-mono">astro.science.portfolio</span> · data read in place from '
            f"{html_lib.escape(str(ROOT))}</div>"
        )

        self.view[:] = [
            pn.pane.HTML(hero, sizing_mode="stretch_width"),
            pn.pane.HTML(metrics, sizing_mode="stretch_width"),
            pn.pane.HTML(
                f'<div class="asp-grid-2">{left}{right}</div>',
                sizing_mode="stretch_width",
            ),
            pn.pane.HTML(footer, sizing_mode="stretch_width"),
        ]

    # -- lifecycle ----------------------------------------------------------
    def panel(self) -> pn.Column:
        return self.view

    def dispose(self) -> None:
        self._disposed = True


# ---------------------------------------------------------------------------
# catalogs
# ---------------------------------------------------------------------------


def _preview_frame(df: pd.DataFrame, limit: int = 500) -> pd.DataFrame:
    """Return a display copy safe for the browser.

    Bokeh serialises integers as JavaScript numbers, so 64-bit identifiers
    (e.g. Gaia ``source_id``) lose precision above 2**53. Those columns are
    rendered as strings in the preview; the CSV on disk is untouched.
    """

    preview = df.head(limit).copy()
    for column in preview.columns:
        series = preview[column]
        if not pd.api.types.is_integer_dtype(series):
            continue
        try:
            largest = series.abs().max()
            if pd.notna(largest) and float(largest) > 2**53:
                preview[column] = series.astype("string")
        except Exception:
            continue
    return preview


def _column_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    total = max(len(df), 1)
    for column in df.columns:
        series = df[column]
        non_null = int(series.notna().sum())
        example = ""
        try:
            if non_null:
                first = series.dropna().iloc[0]
                example = str(first)
        except Exception:
            example = ""
        if len(example) > 70:
            example = example[:67] + "…"
        rows.append(
            {
                "column": str(column),
                "dtype": str(series.dtype),
                "non_null": non_null,
                "null_%": round(100.0 * (total - non_null) / total, 1),
                "example": example,
            }
        )
    return pd.DataFrame(rows)


class CatalogsPanel:
    def __init__(self, context: Any = None, **kwargs: Any) -> None:
        self.context = context
        self._disposed = False

        self.select = pn.widgets.Select(
            name="Catalogue",
            options=DATASET_BY_LABEL,
            value=DATASETS[0]["key"],
            sizing_mode="stretch_width",
        )
        self.reload_button = pn.widgets.Button(
            name="Reload CSV",
            button_type="default",
            width=110,
            height=32,
            margin=(22, 0, 0, 8),
        )

        self.summary = pn.pane.HTML(sizing_mode="stretch_width")
        self.link = pn.pane.Markdown(
            sizing_mode="stretch_width", css_classes=["asp-link"]
        )
        self.preview = pn.widgets.Tabulator(
            sizing_mode="stretch_width",
            height=360,
            page_size=15,
            pagination="local",
            theme="midnight",
            show_index=False,
            selectable=False,
            disabled=True,
        )
        self.columns_table = pn.widgets.Tabulator(
            sizing_mode="stretch_width",
            height=300,
            page_size=10,
            pagination="local",
            theme="midnight",
            show_index=False,
            selectable=False,
            disabled=True,
            widths={
                "column": 190,
                "dtype": 110,
                "non_null": 100,
                "null_%": 90,
                "example": 360,
            },
        )

        self.view = pn.Column(
            _style_pane(),
            pn.pane.HTML(
                _header_html(
                    "Catalogues",
                    "Curated research datasets read directly from disk. Previews show the first "
                    "500 rows; column profiles are computed over the full table.",
                    kicker="Datasets · read-only",
                ),
                sizing_mode="stretch_width",
            ),
            pn.Row(
                self.select,
                self.reload_button,
                sizing_mode="stretch_width",
                margin=(8, 0, 8, 0),
            ),
            self.summary,
            self.link,
            pn.pane.HTML(
                '<div class="asp-section-title" style="margin-top:14px;">Preview · first 500 rows</div>'
            ),
            self.preview,
            pn.pane.HTML(
                '<div class="asp-section-title" style="margin-top:16px;">Column dictionary</div>'
            ),
            self.columns_table,
            css_classes=["asp-panel", "asp-root"],
            sizing_mode="stretch_width",
            margin=(14, 16, 18, 16),
        )

        self.select.param.watch(self._on_select, "value")
        self.reload_button.on_click(self._on_reload)
        self._render(self.select.value)

    # -- callbacks ----------------------------------------------------------
    def _on_select(self, event: Any) -> None:
        self._render(event.new)

    def _on_reload(self, _event: Any) -> None:
        try:
            load_dataset.clear()
        except Exception:
            pass
        self._render(self.select.value)

    def _render(self, key: str) -> None:
        spec = DATASET_BY_KEY.get(key)
        if spec is None:
            self.summary.object = _note_html("Unknown dataset selection.")
            self.preview.value = pd.DataFrame()
            self.columns_table.value = pd.DataFrame()
            self.link.object = ""
            return

        path: Path = spec["path"]
        self.summary.object = (
            f'<div class="asp-fig-head" style="margin-top:4px;">'
            f'<div class="asp-fig-title">{html_lib.escape(spec["label"])}</div>'
            f'<div class="asp-fig-meta">loading…</div></div>'
        )
        self.link.object = ""
        self.preview.value = pd.DataFrame()
        self.columns_table.value = pd.DataFrame()

        if not path.exists():
            self.summary.object = _note_html(
                f"<strong>{html_lib.escape(spec['label'])}</strong> is not available. "
                f"Expected file: <code>{html_lib.escape(str(path))}</code>"
            )
            return

        try:
            df = load_dataset(key)
        except Exception as exc:  # pragma: no cover - depends on local files
            self.summary.object = _note_html(
                f"Could not read <code>{html_lib.escape(path.name)}</code>: "
                f"<code>{html_lib.escape(repr(exc))}</code>"
            )
            return

        n_rows, n_cols = df.shape
        numeric = int(sum(pd.api.types.is_numeric_dtype(df[c]) for c in df.columns))
        text = int(
            sum(
                pd.api.types.is_object_dtype(df[c])
                or pd.api.types.is_string_dtype(df[c])
                for c in df.columns
            )
        )
        other = max(n_cols - numeric - text, 0)
        size = _human_size(path.stat().st_size)
        expected = spec.get("rows")

        expected_note = ""
        if expected is not None and int(expected) != int(n_rows):
            expected_note = (
                f' <span class="asp-badge asp-badge-warn">expected {expected:,}</span>'
            )

        self.summary.object = f"""
<div class="asp-fig-head" style="margin-top:4px;">
  <div>
    <div class="asp-fig-title">{html_lib.escape(spec["label"])}</div>
    <div class="asp-muted" style="font-size:12px;margin-top:3px;">{html_lib.escape(spec["note"])}</div>
  </div>
  <div class="asp-fig-meta">
    <span class="asp-mono">{n_rows:,}</span> rows × <span class="asp-mono">{n_cols}</span> columns
    · {size} · {numeric} numeric / {text} text / {other} other
    {expected_note}
  </div>
</div>
"""

        self.link.object = f"[Open CSV on disk ↗]({_file_uri(path)}) · `{_rel(path)}`"

        self.preview.value = _preview_frame(df)
        self.columns_table.value = _column_dictionary(df)

    # -- lifecycle ----------------------------------------------------------
    def panel(self) -> pn.Column:
        return self.view

    def dispose(self) -> None:
        self._disposed = True


# ---------------------------------------------------------------------------
# figures
# ---------------------------------------------------------------------------

_TOKEN_LABELS = {
    "agn": "AGN",
    "adm": "ADM",
    "bh": "BH",
    "blackcat": "BlackCAT",
    "cmb": "CMB",
    "gw": "GW",
    "gwosc": "GWOSC",
    "gwtc": "GWTC",
    "hmxb": "HMXB",
    "isco": "ISCO",
    "pta": "PTA",
    "smbh": "SMBH",
    "snr": "SNR",
    "sxs": "SXS",
    "xrb": "XRB",
    "schw": "Schwarzschild",
    "rs": "RS",
    "wh": "WH",
    "ai": "AI",
    "ml": "ML",
    "3d": "3D",
    "2d": "2D",
}


def humanize(name: str, title_case: bool = False) -> str:
    """Turn a file stem into a readable caption.

    ``title_case=False`` gives sentence case for figure captions
    (``BH merger animation``); ``title_case=True`` gives document titles
    (``01 Black Hole Fundamentals``).
    """

    tokens = [token for token in name.replace("-", "_").split("_") if token]
    words = []
    for index, token in enumerate(tokens):
        lower = token.lower()
        if lower in _TOKEN_LABELS:
            words.append(_TOKEN_LABELS[lower])
        elif title_case:
            words.append(token.capitalize())
        elif index == 0:
            words.append(token.capitalize())
        else:
            words.append(lower)
    title = " ".join(words).strip()
    return title[:1].upper() + title[1:] if title else name


def _figure_files() -> List[Path]:
    if not FIGURES.is_dir():
        return []
    order = {
        ".html": 0,
        ".png": 1,
        ".gif": 2,
        ".mp4": 3,
        ".jpg": 4,
        ".jpeg": 5,
        ".webp": 6,
    }
    files = [p for p in FIGURES.glob("*") if p.is_file()]
    return sorted(files, key=lambda p: (order.get(p.suffix.lower(), 9), p.name.lower()))


def _figure_label(path: Path) -> str:
    suffix = path.suffix.lower()
    kind = {
        ".html": "interactive",
        ".png": "PNG",
        ".gif": "GIF",
        ".mp4": "MP4",
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
        ".webp": "WebP",
    }.get(suffix, suffix.lstrip(".").upper() or "file")
    return f"{humanize(path.stem)} · {kind}"


class FiguresPanel:
    def __init__(self, context: Any = None, **kwargs: Any) -> None:
        self.context = context
        self._disposed = False

        self.files = _figure_files()
        self.by_label = {_figure_label(path): path for path in self.files}
        labels = list(self.by_label)

        self.select = pn.widgets.Select(
            name="Figure",
            options=labels,
            value=labels[0] if labels else None,
            sizing_mode="stretch_width",
        )
        self.embed_toggle = pn.widgets.Checkbox(
            name="Inline content (works when file:// is blocked)",
            value=True,
            width=320,
            margin=(22, 0, 0, 8),
        )
        self.gallery = pn.widgets.RadioButtonGroup(
            options=labels,
            value=labels[0] if labels else None,
            orientation="horizontal",
            sizing_mode="stretch_width",
            css_classes=["asp-gallery"],
            margin=(4, 0, 4, 0),
        )
        self.stage = pn.Column(sizing_mode="stretch_width")
        self.caption = pn.pane.HTML(sizing_mode="stretch_width")

        summary = (
            f"{len([p for p in self.files if p.suffix.lower() == '.html'])} interactive HTML · "
            f"{len([p for p in self.files if p.suffix.lower() == '.gif'])} GIF · "
            f"{len([p for p in self.files if p.suffix.lower() == '.mp4'])} MP4 · "
            f"{len([p for p in self.files if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}])} PNG/JPEG"
        )

        self.view = pn.Column(
            _style_pane(),
            pn.pane.HTML(
                _header_html(
                    "Figures",
                    "Interactive Plotly figures and animations from the exotic-compact-objects "
                    f"premium figure set · {summary}.",
                    kicker=f"Gallery · {len(self.files)} files",
                ),
                sizing_mode="stretch_width",
            ),
            pn.Row(
                self.select,
                self.embed_toggle,
                sizing_mode="stretch_width",
                margin=(8, 0, 8, 0),
            ),
            pn.pane.HTML(
                '<div class="asp-section-title" style="margin-top:6px;">Gallery</div>'
            ),
            self.gallery,
            self.caption,
            self.stage,
            css_classes=["asp-panel", "asp-root"],
            sizing_mode="stretch_width",
            margin=(14, 16, 18, 16),
        )

        self._syncing = False
        self.select.param.watch(self._on_select, "value")
        self.gallery.param.watch(self._on_gallery, "value")
        self.embed_toggle.param.watch(lambda _event: self._render(), "value")

        self._render()

    # -- callbacks ----------------------------------------------------------
    def _on_select(self, event: Any) -> None:
        if self._syncing:
            return
        self._syncing = True
        try:
            self.gallery.value = event.new
        finally:
            self._syncing = False
        self._render()

    def _on_gallery(self, event: Any) -> None:
        if self._syncing:
            return
        self._syncing = True
        try:
            self.select.value = event.new
        finally:
            self._syncing = False
        self._render()

    def _render(self) -> None:
        label = self.select.value
        path = self.by_label.get(label) if label else None

        self.stage[:] = []
        self.caption.object = ""

        if path is None:
            self.stage.append(pn.pane.HTML(_note_html("No figure files were found.")))
            return

        if not path.exists():
            self.stage.append(
                pn.pane.HTML(
                    _note_html(
                        f"Figure file is missing: <code>{html_lib.escape(str(path))}</code>"
                    )
                )
            )
            return

        suffix = path.suffix.lower()
        size = path.stat().st_size
        kind = {
            ".html": "interactive HTML",
            ".png": "PNG image",
            ".gif": "animated GIF",
            ".mp4": "MP4 video",
        }.get(suffix, suffix.lstrip(".").upper())

        self.caption.object = f"""
<div class="asp-fig-head" style="margin-top:12px;">
  <div>
    <div class="asp-fig-title">{html_lib.escape(humanize(path.stem))}</div>
    <div class="asp-muted" style="font-size:12px;margin-top:2px;">{html_lib.escape(kind)} · {_human_size(size)}</div>
  </div>
  <div class="asp-fig-meta">
    <a href="{html_lib.escape(_file_uri(path))}" target="_blank">Open file ↗</a>
    · <span class="asp-mono">{html_lib.escape(path.name)}</span>
  </div>
</div>
"""

        try:
            pane = self._build_pane(path, suffix, size)
        except Exception as exc:  # pragma: no cover - defensive
            pane = pn.pane.HTML(
                _note_html(
                    f"Could not render this figure: <code>{html_lib.escape(repr(exc))}</code>"
                )
            )

        self.stage.append(pane)

    def _build_pane(self, path: Path, suffix: str, size: int) -> Any:
        embed = bool(self.embed_toggle.value)

        if suffix == ".html":
            if embed and size <= MAX_INLINE_HTML:
                text = path.read_text(encoding="utf-8", errors="replace")
                document = html_lib.escape(text, quote=True)
                return pn.pane.HTML(
                    f'<iframe class="asp-frame" srcdoc="{document}" '
                    f'referrerpolicy="no-referrer"></iframe>',
                    sizing_mode="stretch_width",
                )
            reason = (
                "file:// iframe (browser security may block local files)"
                if embed
                else "file:// iframe"
            )
            warning = (
                f'<div class="asp-fig-meta" style="margin:0 0 6px 0;">'
                f"Large file ({_human_size(size)}), not inlined — {html_lib.escape(reason)}.</div>"
            )
            return pn.Column(
                pn.pane.HTML(warning, sizing_mode="stretch_width"),
                pn.pane.HTML(
                    f'<iframe class="asp-frame" src="{html_lib.escape(_file_uri(path))}"></iframe>',
                    sizing_mode="stretch_width",
                ),
            )

        if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
            return pn.pane.PNG(
                path, sizing_mode="stretch_width", css_classes=["asp-media"]
            )

        if suffix == ".gif":
            if embed and size <= MAX_INLINE_MEDIA:
                data = base64.b64encode(path.read_bytes()).decode("ascii")
                return pn.pane.HTML(
                    f'<img class="asp-media" alt="{html_lib.escape(humanize(path.stem))}" '
                    f'src="data:image/gif;base64,{data}">',
                    sizing_mode="stretch_width",
                )
            return pn.pane.GIF(
                path, sizing_mode="stretch_width", css_classes=["asp-media"]
            )

        if suffix == ".mp4":
            if embed and size <= MAX_INLINE_MEDIA:
                data = base64.b64encode(path.read_bytes()).decode("ascii")
                return pn.pane.HTML(
                    f'<video class="asp-media" controls loop muted playsinline '
                    f'src="data:video/mp4;base64,{data}"></video>',
                    sizing_mode="stretch_width",
                )
            return pn.pane.HTML(
                f'<video class="asp-media" controls loop muted playsinline '
                f'src="{html_lib.escape(_file_uri(path))}"></video>',
                sizing_mode="stretch_width",
            )

        return pn.pane.HTML(
            _note_html(
                f"Unsupported figure type: <code>{html_lib.escape(suffix)}</code>"
            )
        )

    # -- lifecycle ----------------------------------------------------------
    def panel(self) -> pn.Column:
        return self.view

    def dispose(self) -> None:
        self._disposed = True


# ---------------------------------------------------------------------------
# research index
# ---------------------------------------------------------------------------


def _project_name(path: Path) -> str:
    try:
        relative = path.relative_to(PROJECTS)
        return relative.parts[0]
    except Exception:
        return path.parent.name


def research_index() -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []

    for path in _find_files("*/notebooks/*.ipynb"):
        rows.append(
            {
                "name": humanize(path.stem, title_case=True),
                "project": _project_name(path),
                "type": "notebook",
                "path": _rel(path),
                "_path": str(path),
            }
        )

    for path in _find_files("*/reports/*.md"):
        rows.append(
            {
                "name": humanize(path.stem, title_case=True),
                "project": _project_name(path),
                "type": "report",
                "path": _rel(path),
                "_path": str(path),
            }
        )

    for path in _find_files("*/premium/*.md"):
        rows.append(
            {
                "name": humanize(path.stem, title_case=True),
                "project": _project_name(path),
                "type": "theory",
                "path": _rel(path),
                "_path": str(path),
            }
        )

    frame = pd.DataFrame(rows)
    if not frame.empty:
        type_order = {"notebook": 0, "theory": 1, "report": 2}
        frame["_order"] = frame["type"].map(type_order).fillna(9)
        frame = (
            frame.sort_values(["_order", "project", "name"])
            .drop(columns=["_order"])
            .reset_index(drop=True)
        )
    return frame


def _notebook_summary(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"Could not read notebook metadata.\n\n```text\n{exc}\n```"

    cells = data.get("cells", [])
    code_cells = sum(1 for cell in cells if cell.get("cell_type") == "code")
    md_cells = sum(1 for cell in cells if cell.get("cell_type") == "markdown")
    kernelspec = (data.get("metadata", {}) or {}).get("kernelspec", {}) or {}

    excerpts: List[str] = []
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        source = source.strip()
        if source and not source.startswith("#!"):
            excerpts.append(source)
        if len(excerpts) >= 3:
            break

    lines = [
        f"# {humanize(path.stem, title_case=True)}",
        "",
        f"**Notebook** · `{_rel(path)}`",
        "",
        f"- cells: **{len(cells)}** ({code_cells} code, {md_cells} markdown)",
        f"- kernel: `{kernelspec.get('name', 'unknown')}`",
        f"- size: {_human_size(path.stat().st_size)}",
        "",
    ]
    if excerpts:
        lines.append("## Opening notes")
        lines.append("")
        for excerpt in excerpts:
            lines.append(excerpt)
            lines.append("")
    lines.append(
        "_Open the notebook in Jupyter to run it; this panel is a read-only index._"
    )
    return "\n".join(lines)


class ResearchPanel:
    def __init__(self, context: Any = None, **kwargs: Any) -> None:
        self.context = context
        self._disposed = False

        self.index = research_index()
        self.table = pn.widgets.Tabulator(
            self.index.drop(columns=["_path"]) if not self.index.empty else self.index,
            sizing_mode="stretch_width",
            height=330,
            page_size=12,
            pagination="local",
            theme="midnight",
            show_index=False,
            selectable=True,
            disabled=True,
            widths={"name": 300, "project": 240, "type": 110, "path": 520},
        )

        counts = (
            self.index["type"].value_counts().to_dict() if not self.index.empty else {}
        )

        self.viewer = pn.Column(sizing_mode="stretch_width")
        self.meta = pn.pane.HTML(
            f'<div class="asp-fig-meta" style="margin:2px 0 8px 0;">'
            f'<span class="asp-badge asp-badge-ok">{counts.get("notebook", 0)} notebooks</span> '
            f'<span class="asp-badge asp-badge-idle">{counts.get("theory", 0)} theory docs</span> '
            f'<span class="asp-badge asp-badge-idle">{counts.get("report", 0)} reports</span>'
            f"</div>",
            sizing_mode="stretch_width",
        )

        self.view = pn.Column(
            _style_pane(),
            pn.pane.HTML(
                _header_html(
                    "Research index",
                    "Notebooks, premium theory documents and research reports. Select a row to "
                    "read the markdown in place; notebooks show a structural summary.",
                    kicker="Notebooks · reports · theory",
                ),
                sizing_mode="stretch_width",
            ),
            self.meta,
            self.table,
            pn.pane.HTML(
                '<div class="asp-section-title" style="margin-top:16px;">Reader</div>'
            ),
            self.viewer,
            css_classes=["asp-panel", "asp-root"],
            sizing_mode="stretch_width",
            margin=(14, 16, 18, 16),
        )

        self.table.param.watch(self._on_selection, "selection")
        self._render_placeholder()

    # -- callbacks ----------------------------------------------------------
    def _on_selection(self, event: Any) -> None:
        selection = list(event.new or [])
        if not selection:
            self._render_placeholder()
            return
        row_index = int(selection[-1])
        if row_index < 0 or row_index >= len(self.index):
            return
        row = self.index.iloc[row_index]
        path = Path(str(row["_path"]))
        kind = str(row["type"])

        if kind == "notebook":
            text = _notebook_summary(path)
        else:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except Exception as exc:
                text = f"Could not read `{path}`.\n\n```text\n{exc}\n```"

        header = (
            f'<div class="asp-fig-head" style="margin-top:4px;">'
            f'<div class="asp-fig-title">{html_lib.escape(str(row["name"]))}</div>'
            f'<div class="asp-fig-meta">{html_lib.escape(kind)} · '
            f'<a href="{html_lib.escape(_file_uri(path))}" target="_blank">open file ↗</a>'
            f"</div></div>"
        )

        self.viewer[:] = [
            pn.pane.HTML(header, sizing_mode="stretch_width"),
            pn.pane.Markdown(text, sizing_mode="stretch_width", css_classes=["asp-md"]),
        ]

    def _render_placeholder(self) -> None:
        self.viewer[:] = [
            pn.pane.HTML(
                _note_html(
                    "Select a row above to open a notebook summary, theory document or report "
                    "in the reader."
                ),
                sizing_mode="stretch_width",
            )
        ]

    # -- lifecycle ----------------------------------------------------------
    def panel(self) -> pn.Column:
        return self.view

    def dispose(self) -> None:
        self._disposed = True


# ---------------------------------------------------------------------------
# pipeline status
# ---------------------------------------------------------------------------

LOOP_LABELS = {
    "refresh-data": "Data refresh",
    "notebook-health": "Notebook health",
    "refresh-graphs": "Graph refresh",
    "research": "Research loop",
}

LOOP_HINTS = {
    "refresh-data": "download → process → dashboards",
    "notebook-health": "execute notebooks → fix → report",
    "refresh-graphs": "code / domain / wiki graphs",
    "research": "agent-driven, not scheduled",
}


def _badge_class(value: Any) -> Tuple[str, str]:
    text = str(value or "").strip().lower()
    if text in {"ok", "success", "passed", "pass", "done", "green"}:
        return "asp-badge-ok", text or "ok"
    if text in {"failed", "failure", "error", "red"}:
        return "asp-badge-fail", text
    if text in {"warn", "warning", "drift", "stale", "amber"}:
        return "asp-badge-warn", text
    if text in {"skipped", "idle", "pending", "not recorded", ""}:
        return "asp-badge-idle", text or "not recorded"
    return "asp-badge-warn", text


def _load_status() -> Tuple[Optional[Dict[str, Any]], Optional[Path]]:
    for path in (STATUS_FILE, STATUS_FALLBACK):
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data, path
        except Exception:
            return {"__error__": f"Could not parse {path}"}, path
    return None, None


class PipelinePanel:
    def __init__(self, context: Any = None, **kwargs: Any) -> None:
        self.context = context
        self._disposed = False

        self.body = pn.Column(sizing_mode="stretch_width")
        self.refresh_button = pn.widgets.Button(
            name="Refresh status",
            button_type="default",
            width=140,
            height=32,
            margin=(8, 0, 0, 0),
        )
        self.refresh_button.on_click(lambda _event: self.render())

        self.view = pn.Column(
            _style_pane(),
            pn.pane.HTML(
                _header_html(
                    "Pipeline",
                    "Latest automated loop run: data refresh, notebook health and knowledge-graph "
                    "drift. Status is read from the research workspace status file.",
                    kicker="Automation · last run",
                ),
                sizing_mode="stretch_width",
            ),
            pn.Row(self.refresh_button, sizing_mode="stretch_width"),
            self.body,
            css_classes=["asp-panel", "asp-root"],
            sizing_mode="stretch_width",
            margin=(14, 16, 18, 16),
        )

        self.render()

    # -- rendering ----------------------------------------------------------
    def render(self) -> None:
        data, path = _load_status()

        if data is None:
            self.body[:] = [
                pn.pane.HTML(
                    _note_html(
                        "<strong>No pipeline run yet.</strong><br>"
                        "The orchestrator has not written a status file, so there is nothing to "
                        "report. Run the loops with:<br><br>"
                        f"<code>{html_lib.escape(str(ROOT / '.opencode' / 'loops' / 'orchestrator.sh'))}</code>"
                        "<br><br>"
                        "Expected status file:<br>"
                        f"<code>{html_lib.escape(str(STATUS_FILE))}</code><br>"
                        f"<code>{html_lib.escape(str(STATUS_FALLBACK))}</code>"
                    ),
                    sizing_mode="stretch_width",
                )
            ]
            return

        if "__error__" in data:
            self.body[:] = [
                pn.pane.HTML(
                    _note_html(html_lib.escape(str(data["__error__"]))),
                    sizing_mode="stretch_width",
                )
            ]
            return

        loops = data.get("loops") or {}
        if not isinstance(loops, dict):
            loops = {}

        rows: List[str] = []
        for key, label in LOOP_LABELS.items():
            raw = loops.get(key)
            detail = ""
            if isinstance(raw, dict):
                detail = str(
                    raw.get("detail") or raw.get("message") or raw.get("error") or ""
                )
                raw = raw.get("status", raw.get("state"))
            css, text = _badge_class(raw)
            if raw is None:
                text = "not recorded"
            rows.append(
                f'<div class="asp-loop-row">'
                f'<div class="asp-loop-name">{html_lib.escape(label)}'
                f"<small>{html_lib.escape(key)} · {html_lib.escape(LOOP_HINTS.get(key, ''))}</small></div>"
                f'<div><span class="asp-badge {css}">{html_lib.escape(text)}</span>'
                + (
                    f'<div class="asp-fig-meta" style="margin-top:4px;">{html_lib.escape(detail)}</div>'
                    if detail
                    else ""
                )
                + "</div></div>"
            )

        generated = (
            data.get("generatedAt") or data.get("generated_at") or data.get("timestamp")
        )
        if generated is None and path is not None:
            try:
                generated = datetime.fromtimestamp(path.stat().st_mtime).isoformat(
                    timespec="seconds"
                )
            except Exception:
                generated = None

        drift = bool(
            data.get("graphRefreshRequested") or data.get("graph_refresh_requested")
        )
        drift_badge = (
            '<span class="asp-badge asp-badge-warn">graph drift · refresh requested</span>'
            if drift
            else '<span class="asp-badge asp-badge-ok">graphs up to date</span>'
        )

        log_path = data.get("log")
        log_html = ""
        if log_path:
            log_file = Path(str(log_path))
            log_html = (
                f'<div class="k">Log</div><div class="v">'
                f'<a href="{html_lib.escape(_file_uri(log_file))}" target="_blank">'
                f"{html_lib.escape(log_file.name)}</a></div>"
            )

        status_note = ""
        if any(
            str(v).lower() in {"failed", "failure", "error"}
            for v in loops.values()
            if not isinstance(v, dict)
        ):
            status_note = (
                '<div class="asp-note" style="margin-top:12px;">'
                "At least one loop failed. The orchestrator continues with the remaining loops; "
                "open the log above for the failing step.</div>"
            )

        self.body[:] = [
            pn.pane.HTML(
                f"""
<div class="asp-section">
  <div class="asp-section-title">Loop status</div>
  {"".join(rows)}
  <div class="asp-loop-row" style="border-top:1px solid #1e2b3d;border-bottom:none;margin-top:6px;padding-top:12px;">
    <div class="asp-loop-name">Knowledge graphs<small>drift signal from .ua/refresh-requested.json</small></div>
    <div>{drift_badge}</div>
  </div>
</div>
<div class="asp-section" style="margin-top:14px;">
  <div class="asp-section-title">Run details</div>
  <div class="asp-kv">
    <div class="k">Generated</div><div class="v">{html_lib.escape(_fmt_ts(generated))}</div>
    <div class="k">Status file</div><div class="v">{html_lib.escape(str(path) if path else "unknown")}</div>
    {log_html}
    <div class="k">Research</div><div class="v">{html_lib.escape(str(data.get("researchLoop") or data.get("research_loop") or "agent-driven"))}</div>
  </div>
</div>
{status_note}
""",
                sizing_mode="stretch_width",
            )
        ]

    # -- lifecycle ----------------------------------------------------------
    def panel(self) -> pn.Column:
        return self.view

    def dispose(self) -> None:
        self._disposed = True


# ---------------------------------------------------------------------------
# factories (the plugin API calls these)
# ---------------------------------------------------------------------------


def create_overview_panel(context: Any = None, **kwargs: Any):
    apply_theme()
    controller = OverviewPanel(context=context, **kwargs)
    return controller.panel(), controller


def create_catalogs_panel(context: Any = None, **kwargs: Any):
    apply_theme()
    controller = CatalogsPanel(context=context, **kwargs)
    return controller.panel(), controller


def create_figures_panel(context: Any = None, **kwargs: Any):
    apply_theme()
    controller = FiguresPanel(context=context, **kwargs)
    return controller.panel(), controller


def create_research_panel(context: Any = None, **kwargs: Any):
    apply_theme()
    controller = ResearchPanel(context=context, **kwargs)
    return controller.panel(), controller


def create_pipeline_panel(context: Any = None, **kwargs: Any):
    apply_theme()
    controller = PipelinePanel(context=context, **kwargs)
    return controller.panel(), controller
