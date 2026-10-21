"""Visual language for the Astro Science Portfolio plugin.

The CSS is intentionally namespaced under ``.asp-`` so it cannot leak into the
rest of the AstronomicAL workspace.  The only global rule is the page
background, which makes the dark panels sit on a matching canvas.
"""

from __future__ import annotations

# Palette -------------------------------------------------------------------
BG = "#070b14"
SURFACE = "#0e1522"
SURFACE_ALT = "#111a29"
BORDER = "#1e2b3d"
TEXT = "#dbe6f5"
MUTED = "#8fa3bd"
CYAN = "#4cc9f0"
AMBER = "#f4a261"
VIOLET = "#9d7bff"

MONO = "\"Times New Roman\", Times, \"Liberation Serif\", serif"
FONT = "\"Times New Roman\", Times, \"Liberation Serif\", serif"

CSS = f"""
/* ---------- global canvas (safe: background only) ---------- */
body {{
  background-color: {BG};
}}

/* ---------- root container ---------- */
.asp-root,
.asp-root .bk-panel-models-layout-Column {{
  background-color: {BG};
  color: {TEXT};
  font-family: {FONT};
}}

.asp-panel {{
  background-color: {BG};
  color: {TEXT};
  font-family: {FONT};
  padding: 4px 2px 24px 2px;
}}

.asp-panel a {{ color: {CYAN}; text-decoration: none; }}
.asp-panel a:hover {{ text-decoration: underline; }}

.asp-mono {{
  font-family: {MONO};
  font-variant-numeric: tabular-nums;
}}

.asp-muted {{ color: {MUTED}; }}

/* ---------- hero ---------- */
.asp-hero {{
  position: relative;
  padding: 26px 28px 22px 28px;
  border: 1px solid {BORDER};
  border-radius: 18px;
  background:
    radial-gradient(1200px 320px at 8% -30%, rgba(76, 201, 240, 0.18), transparent 62%),
    radial-gradient(900px 300px at 92% -10%, rgba(157, 123, 255, 0.16), transparent 60%),
    linear-gradient(165deg, #0d1727 0%, #0a1220 55%, #080e19 100%);
  overflow: hidden;
}}

.asp-hero::after {{
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(143, 163, 189, 0.055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(143, 163, 189, 0.055) 1px, transparent 1px);
  background-size: 34px 34px;
  mask-image: radial-gradient(120% 90% at 50% 0%, #000 20%, transparent 78%);
  pointer-events: none;
}}

.asp-hero > * {{ position: relative; z-index: 1; }}

.asp-kicker {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 10px;
  font-weight: 600;
  color: {CYAN};
  font-family: {MONO};
}}

.asp-kicker .asp-dot {{
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: {CYAN};
  box-shadow: 0 0 10px {CYAN};
}}

.asp-title {{
  margin: 12px 0 6px 0;
  font-size: clamp(30px, 4vw, 44px);
  line-height: 1.05;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: #f3f8ff;
}}

.asp-title .asp-accent {{
  background: linear-gradient(92deg, {CYAN} 0%, {VIOLET} 58%, {AMBER} 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}}

.asp-subtitle {{
  max-width: 860px;
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: {MUTED};
}}

.asp-hero-meta {{
  margin-top: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}}

.asp-chip {{
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid {BORDER};
  background: rgba(14, 21, 34, 0.72);
  color: {MUTED};
  font-size: 11px;
  font-family: {MONO};
}}

.asp-chip strong {{ color: {TEXT}; font-weight: 600; }}

/* ---------- metric cards ---------- */
.asp-metrics {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(158px, 1fr));
  gap: 12px;
  margin: 16px 0 4px 0;
}}

.asp-card {{
  padding: 14px 16px 15px 16px;
  border: 1px solid {BORDER};
  border-radius: 14px;
  background: linear-gradient(158deg, rgba(76, 201, 240, 0.075) 0%, {
    SURFACE
} 46%, #0b1120 100%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
}}

.asp-card-label {{
  text-transform: uppercase;
  letter-spacing: 0.13em;
  font-size: 10px;
  font-weight: 600;
  color: {MUTED};
}}

.asp-card-value {{
  margin-top: 8px;
  font-family: {MONO};
  font-variant-numeric: tabular-nums;
  font-size: 30px;
  line-height: 1.05;
  font-weight: 600;
  color: #f1f7ff;
}}

.asp-card-value.asp-v-amber {{ color: {AMBER}; }}
.asp-card-value.asp-v-violet {{ color: {VIOLET}; }}
.asp-card-value.asp-v-cyan {{ color: {CYAN}; }}

.asp-card-note {{
  margin-top: 6px;
  font-size: 11px;
  color: #6f86a3;
}}

/* ---------- sections ---------- */
.asp-grid-2 {{
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
  gap: 16px;
  margin-top: 16px;
}}

@media (max-width: 900px) {{
  .asp-grid-2 {{ grid-template-columns: minmax(0, 1fr); }}
}}

.asp-section {{
  border: 1px solid {BORDER};
  border-radius: 14px;
  background: {SURFACE};
  padding: 16px 18px 18px 18px;
}}

.asp-section-title {{
  margin: 0 0 12px 0;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: {MUTED};
}}

.asp-areas {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 8px 18px;
  margin: 0;
  padding: 0;
  list-style: none;
}}

.asp-areas li {{
  display: flex;
  align-items: baseline;
  gap: 9px;
  padding: 7px 0;
  border-bottom: 1px dashed rgba(30, 43, 61, 0.9);
  font-size: 13px;
  color: {TEXT};
}}

.asp-areas li:last-child {{ border-bottom: none; }}

.asp-areas .asp-idx {{
  font-family: {MONO};
  font-size: 10px;
  color: {CYAN};
  opacity: 0.85;
}}

.asp-kv {{
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 6px 14px;
  font-size: 12px;
  color: {MUTED};
}}

.asp-kv .k {{
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 10px;
  color: #6f86a3;
  padding-top: 1px;
}}

.asp-kv .v {{ color: {TEXT}; font-family: {MONO}; }}

.asp-footer {{
  margin-top: 18px;
  padding-top: 12px;
  border-top: 1px solid {BORDER};
  font-size: 11px;
  color: #6f86a3;
  font-family: {MONO};
}}

/* ---------- badges ---------- */
.asp-badge {{
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid {BORDER};
  font-family: {MONO};
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: {MUTED};
  background: rgba(14, 21, 34, 0.8);
  white-space: nowrap;
}}

.asp-badge::before {{
  content: "";
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: {MUTED};
}}

.asp-badge-ok {{
  color: {CYAN};
  border-color: rgba(76, 201, 240, 0.4);
  background: rgba(76, 201, 240, 0.1);
}}
.asp-badge-ok::before {{ background: {CYAN}; box-shadow: 0 0 8px {CYAN}; }}

.asp-badge-warn {{
  color: {AMBER};
  border-color: rgba(244, 162, 97, 0.4);
  background: rgba(244, 162, 97, 0.1);
}}
.asp-badge-warn::before {{ background: {AMBER}; box-shadow: 0 0 8px {AMBER}; }}

.asp-badge-fail {{
  color: #ff7a90;
  border-color: rgba(255, 122, 144, 0.42);
  background: rgba(255, 122, 144, 0.1);
}}
.asp-badge-fail::before {{ background: #ff7a90; box-shadow: 0 0 8px #ff7a90; }}

.asp-badge-idle {{
  color: {MUTED};
  border-color: {BORDER};
}}

.asp-loop-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 11px 0;
  border-bottom: 1px dashed rgba(30, 43, 61, 0.9);
}}
.asp-loop-row:last-child {{ border-bottom: none; }}
.asp-loop-name {{
  font-size: 13px;
  color: {TEXT};
}}
.asp-loop-name small {{
  display: block;
  margin-top: 3px;
  color: #6f86a3;
  font-size: 11px;
  font-family: {MONO};
}}

/* ---------- notices ---------- */
.asp-note {{
  border: 1px dashed {BORDER};
  border-radius: 14px;
  padding: 18px 20px;
  background: rgba(14, 21, 34, 0.6);
  color: {MUTED};
  font-size: 13px;
  line-height: 1.6;
}}
.asp-note strong {{ color: {TEXT}; }}
.asp-note code {{
  font-family: {MONO};
  font-size: 11px;
  color: {AMBER};
  background: rgba(0, 0, 0, 0.35);
  padding: 1px 6px;
  border-radius: 5px;
}}

/* ---------- widgets ---------- */
.asp-panel select,
.asp-panel .bk-input,
.asp-panel input[type="text"] {{
  background-color: {SURFACE} !important;
  color: {TEXT} !important;
  border: 1px solid {BORDER} !important;
  border-radius: 8px !important;
  font-family: {FONT};
  font-size: 13px;
}}
.asp-panel option {{ background-color: {SURFACE}; color: {TEXT}; }}
.asp-panel label {{
  color: {MUTED};
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}}

.asp-panel .bk-btn {{
  background-color: {SURFACE};
  color: {TEXT};
  border: 1px solid {BORDER};
  border-radius: 8px;
  font-size: 12px;
}}
.asp-panel .bk-btn:hover {{
  border-color: {CYAN};
  color: {CYAN};
}}

/* ---------- tables ---------- */
.asp-panel .tabulator {{
  background-color: {SURFACE};
  color: {TEXT};
  border: 1px solid {BORDER};
  border-radius: 12px;
  font-size: 12px;
  font-family: {FONT};
  overflow: hidden;
}}

.asp-panel .tabulator .tabulator-header {{
  background-color: #0b1220;
  border-bottom: 1px solid {BORDER};
}}

.asp-panel .tabulator .tabulator-headers {{
  position: sticky;
  top: 0;
  z-index: 3;
}}

.asp-panel .tabulator .tabulator-col {{
  background-color: #0b1220 !important;
  border-right: 1px solid #16212f !important;
  color: {MUTED} !important;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  font-size: 10px;
  font-weight: 600;
}}

.asp-panel .tabulator .tabulator-col-content {{ padding: 8px 10px; }}

.asp-panel .tabulator .tabulator-row {{
  background-color: {SURFACE};
  color: {TEXT};
  border-bottom: 1px solid #141e2c;
}}

.asp-panel .tabulator .tabulator-row.tabulator-row-even {{
  background-color: {SURFACE_ALT};
}}

.asp-panel .tabulator .tabulator-row:hover,
.asp-panel .tabulator .tabulator-row.tabulator-selectable:hover {{
  background-color: #172437 !important;
}}

.asp-panel .tabulator .tabulator-row.tabulator-selected {{
  background-color: rgba(76, 201, 240, 0.16) !important;
}}

.asp-panel .tabulator .tabulator-cell {{
  border-right: 1px solid #16212f;
  padding: 6px 10px;
  font-variant-numeric: tabular-nums;
}}

.asp-panel .tabulator .tabulator-footer {{
  background-color: #0b1220;
  border-top: 1px solid {BORDER};
  color: {MUTED};
}}
.asp-panel .tabulator .tabulator-footer .tabulator-page {{
  background-color: {SURFACE};
  color: {TEXT};
  border: 1px solid {BORDER};
  border-radius: 6px;
}}
.asp-panel .tabulator .tabulator-footer .tabulator-page.active {{
  background-color: rgba(76, 201, 240, 0.18);
  color: {CYAN};
}}

/* ---------- figure frame ---------- */
.asp-gallery .bk-btn-group {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  background: transparent;
}}

.asp-gallery .bk-btn {{
  padding: 5px 10px;
  border: 1px solid {BORDER};
  border-radius: 8px;
  background: {SURFACE};
  color: {MUTED};
  font-family: {MONO};
  font-size: 10.5px;
  letter-spacing: 0.01em;
  text-transform: none;
  line-height: 1.25;
}}

.asp-gallery .bk-btn:hover {{
  border-color: {CYAN};
  color: {TEXT};
}}

.asp-gallery .bk-btn.active,
.asp-gallery .bk-btn.bk-active {{
  border-color: {CYAN};
  background: rgba(76, 201, 240, 0.16);
  color: #eaf7ff;
}}

.asp-frame {{
  display: block;
  width: 100%;
  height: 72vh;
  min-height: 460px;
  border: 1px solid {BORDER};
  border-radius: 12px;
  background: #05080f;
}}

.asp-media {{
  display: block;
  max-width: 100%;
  margin: 0 auto;
  border: 1px solid {BORDER};
  border-radius: 12px;
  background: #05080f;
}}

.asp-fig-head {{
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin: 0 0 10px 0;
}}

.asp-fig-title {{
  font-size: 16px;
  font-weight: 600;
  color: #f1f7ff;
  letter-spacing: -0.01em;
}}

.asp-fig-meta {{
  font-family: {MONO};
  font-size: 11px;
  color: #6f86a3;
}}

.asp-link p {{
  margin: 0 0 6px 0;
  font-family: {MONO};
  font-size: 11px;
  color: #6f86a3;
}}

.asp-link a {{ color: {CYAN}; }}

.asp-link code {{
  font-family: {MONO};
  font-size: 11px;
  color: {MUTED};
  background: transparent;
}}

/* ---------- markdown viewer ---------- */
.asp-md {{
  border: 1px solid {BORDER};
  border-radius: 12px;
  background: {SURFACE};
  padding: 6px 20px 18px 20px;
  max-height: 68vh;
  overflow: auto;
}}

.asp-md h1, .asp-md h2, .asp-md h3 {{
  color: #f1f7ff;
  letter-spacing: -0.015em;
}}
.asp-md h1 {{ font-size: 22px; border-bottom: 1px solid {
    BORDER
}; padding-bottom: 8px; }}
.asp-md h2 {{ font-size: 17px; margin-top: 22px; }}
.asp-md h3 {{ font-size: 14px; color: {CYAN}; }}
.asp-md p, .asp-md li {{ color: {TEXT}; font-size: 13px; line-height: 1.65; }}
.asp-md strong {{ color: #ffffff; }}
.asp-md hr {{ border-color: {BORDER}; }}
.asp-md code {{
  font-family: {MONO};
  font-size: 11.5px;
  color: {AMBER};
  background: rgba(0, 0, 0, 0.4);
  padding: 1px 5px;
  border-radius: 5px;
}}
.asp-md pre {{
  background: #060a12;
  border: 1px solid {BORDER};
  border-radius: 10px;
  padding: 12px 14px;
}}
.asp-md pre code {{ color: {TEXT}; background: transparent; padding: 0; }}
.asp-md blockquote {{
  border-left: 2px solid {VIOLET};
  margin: 12px 0;
  padding: 2px 0 2px 14px;
  color: {MUTED};
}}
.asp-md table {{ font-size: 12px; }}
.asp-md th {{
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 10px;
  color: {MUTED};
  border-bottom: 1px solid {BORDER};
}}
.asp-md td {{ border-bottom: 1px solid #16212f; }}
"""
