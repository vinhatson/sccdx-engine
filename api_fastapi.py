# -*- coding: utf-8 -*-
"""
SCCD-X — optional FastAPI adapter
==================================
serve.py is the primary server and needs nothing but numpy. Use this instead
when you want OpenAPI docs, request validation, or an ASGI deployment:

    pip install fastapi uvicorn
    uvicorn api_fastapi:app --port 8777

It mounts the same web form at / and exposes the same six endpoints, so the
front end does not care which one is running. The handler bodies are imported
from serve.py rather than duplicated - there is one implementation of the
request contract, not two that can drift apart.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import serve as S                      # the single source of request handling
from sccd import spec as s1spec
from sccdx import spec2
from sccdx import i18n as I18N
from sccdx import i18n_render as LOC
from sccdx.events import catalogue
from sccdx.presets import preset_json
import sys

# --- UTF-8 console (a default Windows cp1252 console would otherwise abort on
#     the first Vietnamese or Greek character this script prints) ---
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):      # non-TTY or already wrapped
        pass

LangQ = Query("vi", pattern="^(vi|en)$",
              description="vi | en. Selects the language of EVERY string in "
                          "the response. There is no bilingual mode: the "
                          "engine emits codes and one language is rendered.")

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, "web")

app = FastAPI(
    title="SCCD-X Engine",
    version=f"{s1spec.SPEC_VERSION}+{spec2.SPEC2_VERSION}",
    description=(
        "Qualitative world-politics structural engine. sccd v1.00 "
        "(Sovereign-Civilian Capacity Dynamics) extended with two forcing "
        "blocks: Block D from 'The Wheel of Fate' and Block A from 'The "
        "Displacement Hypothesis'.\n\n"
        "**Read before using any number.** 36 of 83 v1 parameters carry a "
        "value stated in the source paper; 46 do not. All 46 v2 parameters "
        "are ANALYST - the two new papers are qualitative and state no "
        "coefficients. Every output is ORDINAL: a ranking and a "
        "threshold-crossing map, not a level. The source paper's own "
        "standard (Part V 1) is 'qualitative-structural'; this engine is "
        "weaker again. Call /api/v2/audit for the full provenance census."),
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])


# ---------------------------------------------------------------------------
# Request models. Permissive by design: every field is optional, `preset`
# fills a whole row, and anything supplied overrides it.
# ---------------------------------------------------------------------------
class EventIn(BaseModel):
    id: str
    intensity: float = Field(1.0, ge=0.0, le=1.0)
    weight: float = Field(1.0, ge=0.0, le=5.0)
    enabled: bool = True


class PolityIn(BaseModel):
    preset: Optional[str] = Field(
        None, description="Preset code: US CN EU JP KR IN RU BR GB NG")
    code: Optional[str] = None
    name: Optional[str] = None
    state_type: Optional[str] = Field(
        None, description="liberal_democracy | developmental_autocracy | "
                          "extractive_patrimonial | failed_state")
    weight: Optional[float] = Field(None, ge=0.0, le=1.0,
                                    description="systemic weight for Psi_G")
    sub: Optional[Dict[str, float]] = Field(
        None, description="s1..s5, c1..c5, each in [0,1]")
    demo: Optional[Dict[str, float]] = Field(
        None, description="Block D: d1..d5, each in [0,1]")
    disp: Optional[Dict[str, float]] = Field(
        None, description="Block A: a1..a6, plus luxury_contraction and "
                          "physical_share")
    revenue_polarisation: Optional[float] = Field(None, ge=0.0, le=1.0)
    security_pressure: Optional[float] = Field(None, ge=0.0, le=1.0)
    base_revenue_demand: Optional[float] = Field(None, ge=0.0, le=1.0)
    g_shock: Optional[float] = Field(None, ge=0.0, le=1.0)
    ret: Optional[float] = None
    opportunity: Optional[float] = None
    capital_controls: Optional[float] = None
    skilled_supply: Optional[float] = None
    events: List[EventIn] = []


class DiagnoseIn(PolityIn):
    year: int = 2026
    horizon_years: float = Field(15.0, ge=1.0, le=40.0)
    router_mode: str = Field("conserve", description="conserve | discount")
    haven_single_channel: bool = False
    d_delta_dt: Optional[float] = Field(
        None, description="Override the momentum term of sccd eq (23). Leave "
                          "null and the engine measures it off the "
                          "trajectory instead of asking you for it.")
    params: Optional[Dict[str, float]] = Field(
        None, description="Override any spec or spec2 parameter by name.")
    sigma: Optional[Dict[str, float]] = Field(
        None, description="Per-component measurement SD for the Monte Carlo "
                          "pass (sccd Part III eq 5.4).")
    mc_draws: Optional[int] = Field(None, ge=50, le=20000)
    with_trajectory: bool = True
    with_sensitivity: bool = True
    traj_stride: int = Field(6, ge=1, le=50)
    lang: str = Field("vi", description="vi | en. Selects the language "
                                      "of every string in the response.")


class WorldIn(BaseModel):
    year: int = 2026
    codes: Optional[List[str]] = Field(
        None, description="Preset codes to include. Defaults to all ten.")
    polities: Optional[List[PolityIn]] = Field(
        None, description="Full rows, used instead of `codes`.")
    horizon_years: float = Field(15.0, ge=1.0, le=40.0)
    sync_risk_prior: Optional[float] = Field(
        None, ge=0.0, le=0.95,
        description="sccd's historical Sync_Risk prior. The engine adds an "
                    "endogenous haven term on top and reports both parts.")
    router_mode: str = "conserve"
    params: Optional[Dict[str, float]] = None
    sigma: Optional[Dict[str, float]] = None
    mc_draws: Optional[int] = Field(None, ge=50, le=20000)
    with_trajectory: bool = True
    with_sensitivity: bool = False
    lang: str = "vi"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/v2/health", tags=["meta"])
def health() -> Dict[str, Any]:
    from sccdx.integrate import best_solver
    _, label = best_solver()
    return {"ok": True, "engine": "SCCD-X", "server": "fastapi",
            "langs": list(I18N.LANGS),
            "sccd_spec": s1spec.SPEC_VERSION,
            "sccdx_spec": spec2.SPEC2_VERSION, "ode_backend": label}


@app.get("/api/v2/schema", tags=["meta"])
def schema(lang: str = LangQ) -> Dict[str, Any]:
    """Every input field with its definition, default and data-availability
    status. Drives the web form; also the quickest way to see which
    components sccd's own api_readiness() marks BLOCKED."""
    return S._schema(lang)


@app.get("/api/v2/events", tags=["meta"])
def events(lang: str = LangQ) -> Dict[str, Any]:
    """The event catalogue: 50 named events across 11 groups, each with its
    declared per-component effect. All magnitudes are ANALYST."""
    return LOC.localize_events(catalogue(), lang)


@app.get("/api/v2/presets", tags=["meta"])
def presets(lang: str = LangQ) -> Dict[str, Any]:
    """2026 baseline rows for ten polities. Analyst priors, with four
    exceptions stated in the source paper (US s3, c5, c1, s2)."""
    return LOC.localize_presets(preset_json(), lang)


@app.get("/api/v2/audit", tags=["meta"])
def audit(lang: str = LangQ) -> Dict[str, Any]:
    """Parameter provenance census, the v2 open-problem register, and sccd's
    own nine known inconsistencies. Read this before quoting any output."""
    return S._audit(lang)


@app.post("/api/v2/diagnose", tags=["engine"])
def diagnose(body: DiagnoseIn) -> Dict[str, Any]:
    """Diagnose one polity.

    Returns the qualitative triple (Delta band, coherence tier, adjustment
    mode), the theta25 gate projections, L1-L8 loop activation, the
    bifurcation test, a structural trajectory, an OAT fragility table and a
    bilingual narrative."""
    try:
        return S._do_diagnose(body.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"bad input: {e}")


@app.post("/api/v2/world", tags=["engine"])
def world(body: WorldIn) -> Dict[str, Any]:
    """Diagnose a set of polities and the system they form.

    Adds Psi_G with its two-part Sync_Risk, the Thucydides test between the
    two systemically heaviest polities, R_B,G, the adjustment-mode split and
    the talent-pressure gradient."""
    try:
        return S._do_world(body.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"bad input: {e}")


# ---------------------------------------------------------------------------
# Static form
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join(WEB, "index.html"))


if os.path.isdir(WEB):
    app.mount("/web", StaticFiles(directory=WEB), name="web")
