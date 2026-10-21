# Astro Science Portfolio — AstronomicAL plugin

Read-only AstronomicAL panels over the
[astro-science](../../../Projects/astro-science) research workspace
(`/home/dawe/Projects/astro-science`).

| Panel id | Title | What it shows |
| --- | --- | --- |
| `overview` | Portfolio: Overview | Hero header, six metric cards computed from the real files, research areas, workspace paths |
| `catalogs` | Portfolio: Catalogues | 12 catalogues, first 500 rows, row/column counts, column dictionary, link to the CSV on disk |
| `figures` | Portfolio: Figures | Every premium figure (HTML/GIF/MP4, currently 30 + 7 + 7), lazy loaded one at a time |
| `research` | Portfolio: Research Index | All notebooks (26), premium theory documents (13) and reports (counted at render time) + markdown reader |
| `pipeline` | Portfolio: Pipeline | Last data-refresh / notebook-health / graph-refresh status with coloured badges |

All panels are registered under the **Astro Science** category.

## Layout

```text
~/.astronomical/plugins/astro_science_portfolio/
├── plugin.py                  # PluginManifest + register(api)
├── panels.py                  # panel factories, dataset registry, loaders
├── theme.py                   # CSS (palette, cards, tables, badges)
├── astronomical-plugin.json   # static manifest (required for ~/.astronomical/plugins)
└── README.md
```

## Enable the plugin

`~/.astronomical/plugins` is a *user* plugin root: AstronomicAL treats the
plugin as community code and only enables it when community plugins are enabled
and the plugin id is enabled in `~/.astronomical/plugin-state.json`:

```json
{
  "schema_version": 1,
  "community_plugins_enabled": true,
  "plugins": {
    "astro.science.portfolio": { "enabled": true }
  }
}
```

Then restart AstronomicAL. Expect these lines in the server log:

```text
main.py: discovered plugin id=astro.science.portfolio ...
main.py: enabling plugin id=astro.science.portfolio
main.py: enabled plugin id=astro.science.portfolio panels=['astro.science.portfolio.overview', ...]
```

The plugin can also be enabled from the bundled **Plugin Manager** panel.

## Data sources

Nothing is copied. Every panel reads the files in place:

- `research/projects/exotic-compact-objects/data/processed/*.csv`
- `research/projects/exotic-compact-objects/results/*.csv`
- `research/projects/exotic-compact-objects/data/external/**/*.csv`
- `research/projects/exotic-compact-objects/premium/figures/*`
- `research/projects/*/notebooks/*.ipynb`, `reports/*.md`, `premium/*.md`
- `.opencode/loops/latest-status.json` (falling back to `.opencode/loops/logs/latest-status.json`)

Set `ASTRO_SCIENCE_ROOT` before launching to point the plugin at another checkout.

## Adding a dataset

Append one entry to `DATASETS` in `panels.py`:

```python
{
    "key": "my_catalogue",
    "label": "My catalogue",
    "rows": 1234,                      # expected count, shown as a warning badge if it drifts
    "path": EXTERNAL / "my_catalogue.csv",
    "note": "One-line provenance",
},
```

The select box, preview, column dictionary and CSV link update automatically.
Row counts on the overview card come from the same registry.

## Performance notes

- `load_dataset()` is wrapped in `pn.cache(max_items=4)`: each CSV is read once
  and only when selected, so the 50 000-row Gaia table does not slow startup.
- Only the preview (`head(500)`) is sent to the browser.
- Figures are built on selection; HTML is inlined with `srcdoc` (so browser
  `file://` restrictions do not blank the frame) up to 12 MB. Larger documents
  such as `wormhole_traversal.html` (42 MB) fall back to a `file://` iframe with
  an "Open file" link. Plotly figures load `plotly.js` from the CDN.
- GIF/MP4 media is inlined as a data URI below 12 MB.

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| Plugin not listed at all | Missing `astronomical-plugin.json`, or the directory has no `plugin.py`. Check `[plugins] discovery errors` in the log. |
| Plugin discovered but disabled | Community plugins off, or the id missing from `plugin-state.json`. |
| `ImportError: numpy.core.multiarray failed to import` | Mismatched numpy/pyarrow wheels. `uv pip install --reinstall pyarrow==26.* numpy==2.5.*`. |
| Empty audit table / Arrow errors | pyarrow too old for pandas 3; use pyarrow ≥ 24 (26 used here). |
| Figure panel blank | Offline (Plotly CDN) or a >12 MB figure opened through `file://`. Use the "Open file" link. |
| Catalogue shows "expected N" warning | The CSV on disk changed size; update `rows` in the registry. |
