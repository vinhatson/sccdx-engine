# -*- coding: utf-8 -*-
"""
SCCD-X API server
==================
Serves the engine and the web form. Pure standard library plus numpy, so:

    python serve.py
    -> http://127.0.0.1:8777

ENDPOINTS
---------
  GET  /                      the web form
  GET  /api/v2/health         version + solver backend
  GET  /api/v2/schema         every input field, with definition and source
  GET  /api/v2/events         the event catalogue (50 events, 11 groups)
  GET  /api/v2/presets        2026 baseline rows for 10 polities
  GET  /api/v2/audit          parameter provenance, open problems,
                              sccd's own known inconsistencies
  POST /api/v2/diagnose       one polity   -> Diagnosis2
  POST /api/v2/world          many polities -> WorldDiagnosis

Both POST bodies accept partial input: any component you leave out takes its
default, and `preset: "US"` fills the whole row from presets.py before your
own fields are applied on top.

CORS is wide open (*). This is a local analysis tool; if you put it on a
network, put a reverse proxy and auth in front of it first.
"""
from __future__ import annotations

import json
import os
import sys

# --- UTF-8 console (a default Windows cp1252 console would otherwise abort on
#     the first Vietnamese or Greek character this script prints) ---
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):      # non-TTY or already wrapped
        pass
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sccd import spec as s1spec
from sccd.aggregate import SubComponents
from sccdx import spec2
from sccdx import i18n as I18N
from sccdx import i18n_render as LOC
from sccdx.i18n_ui import ui as ui_strings
from sccdx.events import EventInput, catalogue
from sccdx.engine2 import diagnose2
from sccdx.forcing import DemoBlock, DispBlock
from sccdx.integrate import best_solver
from sccdx.narrative import narrate, narrate_world
from sccdx.presets import BY_CODE, preset_json
from sccdx.world import PolityInput, diagnose_world

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, "web")

_DEF_SUB = dict(s1=0.50, s2=0.60, s3=0.50, s4=0.55, s5=0.40,
                c1=0.60, c2=0.50, c3=0.55, c4=0.50, c5=0.50)


# ---------------------------------------------------------------------------
# Input parsing
# ---------------------------------------------------------------------------
def _f(d: dict, k: str, default: float) -> float:
    v = d.get(k, default)
    if v is None:
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        raise ValueError(f"field {k!r} must be a number, got {v!r}")


def _polity_from_body(b: dict) -> Dict[str, Any]:
    """Build one polity's arguments. `preset` fills the row first."""
    base: Dict[str, Any] = {}
    pre = b.get("preset")
    if pre:
        if pre not in BY_CODE:
            raise ValueError(f"unknown preset {pre!r}; "
                             f"have {sorted(BY_CODE)}")
        p = BY_CODE[pre]
        base = dict(
            code=p["code"], name=p["name"], state_type=p["state_type"],
            weight=p["weight"], sub=p["sub"].as_dict(),
            demo=p["demo"].as_dict(), disp=p["disp"].as_dict(),
            revenue_polarisation=p["revenue_polarisation"],
            security_pressure=p["security_pressure"],
            base_revenue_demand=p["base_revenue_demand"],
            ret=p["ret"], opportunity=p["opportunity"],
            capital_controls=p["capital_controls"],
            skilled_supply=p["skilled_supply"],
            provenance=p["provenance"], confidence=p["confidence"])
    else:
        base = dict(code=b.get("code", "XX"), name=b.get("name", "Unnamed"),
                    state_type="liberal_democracy", weight=1.0,
                    sub=dict(_DEF_SUB), demo={}, disp={},
                    revenue_polarisation=0.0, security_pressure=0.0,
                    base_revenue_demand=0.0, ret=0.0, opportunity=0.0,
                    capital_controls=0.0, skilled_supply=0.0,
                    provenance="caller-supplied", confidence="unknown")

    for k in ("code", "name", "state_type", "provenance", "confidence"):
        if b.get(k) is not None:
            base[k] = b[k]
    for k in ("weight", "revenue_polarisation", "security_pressure",
              "base_revenue_demand", "ret", "opportunity",
              "capital_controls", "skilled_supply"):
        if b.get(k) is not None:
            base[k] = _f(b, k, base[k])

    sub = dict(base["sub"])
    for k, v in (b.get("sub") or {}).items():
        if k in sub and v is not None:
            sub[k] = float(v)
    if base["state_type"] not in s1spec.STATE_TYPE_WEIGHTS:
        raise ValueError(f"unknown state_type {base['state_type']!r}; "
                         f"have {sorted(s1spec.STATE_TYPE_WEIGHTS)}")

    dm = DemoBlock(**{k: v for k, v in (base["demo"] or {}).items()})
    for k, v in (b.get("demo") or {}).items():
        if hasattr(dm, k) and v is not None:
            setattr(dm, k, float(v))

    ap = DispBlock(**{k: v for k, v in (base["disp"] or {}).items()})
    for k, v in (b.get("disp") or {}).items():
        if hasattr(ap, k) and v is not None:
            setattr(ap, k, float(v))

    events: List[EventInput] = []
    for e in (b.get("events") or []):
        if isinstance(e, str):
            events.append(EventInput(id=e))
        else:
            events.append(EventInput(
                id=e["id"], intensity=float(e.get("intensity", 1.0)),
                weight=float(e.get("weight", 1.0)),
                enabled=bool(e.get("enabled", True))))

    return dict(base, sub=SubComponents(**sub), demo=dm, disp=ap,
                events=events)


def _do_diagnose(body: dict) -> dict:
    p = _polity_from_body(body)
    D = diagnose2(
        p["name"], int(body.get("year", 2026)), p["sub"],
        demo=p["demo"], disp=p["disp"], state_type=p["state_type"],
        revenue_polarisation=p["revenue_polarisation"],
        security_pressure=p["security_pressure"],
        base_revenue_demand=p["base_revenue_demand"],
        g_shock=_f(body, "g_shock", 0.0),
        d_delta_dt=(float(body["d_delta_dt"])
                    if body.get("d_delta_dt") is not None else None),
        params=body.get("params") or None,
        sigma=body.get("sigma") or None,
        mc_draws=(int(body["mc_draws"]) if body.get("mc_draws") else None),
        events=p["events"] or None,
        horizon_years=_f(body, "horizon_years", 15.0),
        router_mode=body.get("router_mode", "conserve"),
        haven_single_channel=bool(body.get("haven_single_channel", False)),
        with_trajectory=bool(body.get("with_trajectory", True)),
        with_sensitivity=bool(body.get("with_sensitivity", True)))
    lang = I18N.norm_lang(body.get("lang"))
    out = D.as_dict(traj_stride=int(body.get("traj_stride", 6)))
    # Localise FIRST, then narrate: the narrative reads the localised dict, so
    # one language in means one language out, with nothing to drift.
    out = LOC.localize_diagnosis(out, lang)
    out["narrative"] = narrate(out, lang)
    return out


def _do_world(body: dict) -> dict:
    rows = body.get("polities")
    if not rows:
        codes = body.get("codes") or list(BY_CODE)
        rows = [{"preset": c} for c in codes]
    polities: List[PolityInput] = []
    for r in rows:
        p = _polity_from_body(r)
        polities.append(PolityInput(**p))
    W = diagnose_world(
        polities, int(body.get("year", 2026)),
        params=body.get("params") or None,
        horizon_years=_f(body, "horizon_years", 15.0),
        sync_risk_prior=(float(body["sync_risk_prior"])
                         if body.get("sync_risk_prior") is not None else None),
        router_mode=body.get("router_mode", "conserve"),
        with_trajectory=bool(body.get("with_trajectory", True)),
        with_sensitivity=bool(body.get("with_sensitivity", False)),
        sigma=body.get("sigma") or None,
        mc_draws=(int(body["mc_draws"]) if body.get("mc_draws") else None))
    lang = I18N.norm_lang(body.get("lang"))
    out = LOC.localize_world(W.as_dict(), lang)
    out["narrative"] = narrate_world(out, lang)
    return out


# ---------------------------------------------------------------------------
# Schema - drives the web form
# ---------------------------------------------------------------------------
# Which of the ten core components sccd's own api_readiness() marks BLOCKED:
# S3 legitimacy, S4 administrative penetration and C5 fragmentation have no
# multi-country machine-readable source. Those three are also the ones that
# drive lambda, S and the C denominator - the blocked components are the
# decisive ones, which is the structural data problem sccd Part III 5
# documents rather than an accident of this file.
_BLOCKED = ("s3", "s4", "c5")
_CORE_KEYS = ("s1", "s2", "s3", "s4", "s5", "c1", "c2", "c3", "c4", "c5")


def _schema(lang: str = "vi") -> dict:
    lang = I18N.norm_lang(lang)
    return {
        "versions": {"sccd": s1spec.SPEC_VERSION,
                     "sccdx": spec2.SPEC2_VERSION},
        "state_types": {k: {"w1": v[0], "w4": v[1], "omega25": v[2]}
                        for k, v in s1spec.STATE_TYPE_WEIGHTS.items()},
        "core": [{"key": k,
                  "label": I18N.t(f"comp.{k}.label", lang),
                  "help": I18N.t(f"comp.{k}.help", lang),
                  "data_status": "BLOCKED" if k in _BLOCKED else "PAPER proxy",
                  "default": _DEF_SUB[k], "min": 0.0, "max": 1.0}
                 for k in _CORE_KEYS],
        "demo": [{"key": k,
                  "label": I18N.t(f"comp.{k}.label", lang),
                  "help": I18N.t(f"comp.{k}.help", lang),
                  "default": getattr(DemoBlock(), k), "min": 0.0, "max": 1.0}
                 for k in spec2.DEMO_COMPONENTS],
        "disp": [{"key": k,
                  "label": I18N.t(f"comp.{k}.label", lang),
                  "help": I18N.t(f"comp.{k}.help", lang),
                  "default": getattr(DispBlock(), k), "min": 0.0, "max": 1.0}
                 for k in spec2.DISP_COMPONENTS],
        "scalars": [{"key": k,
                     "label": I18N.t(f"scal.{k}.label", lang),
                     "help": I18N.t(f"scal.{k}.help", lang),
                     "default": dflt, "min": lo, "max": hi}
                    for k, dflt, lo, hi in (
                        ("revenue_polarisation", 0.0, 0.0, 1.0),
                        ("security_pressure", 0.0, 0.0, 1.0),
                        ("base_revenue_demand", 0.0, 0.0, 0.4),
                        ("g_shock", 0.0, 0.0, 1.0),
                        ("luxury_contraction", 0.0, 0.0, 1.0),
                        ("physical_share",
                         spec2.DISP["physical_share_default"].value,
                         0.0, 1.0))],
        "options": {
            "router_mode": {
                "values": ["conserve", "discount"],
                "value_labels": {v: I18N.t(f"router.{v}", lang)
                                 for v in ("conserve", "discount")},
                "default": "conserve",
                "help": I18N.t("op.router.help", lang)},
            "haven_single_channel": {
                "values": [False, True], "default": False,
                "help": I18N.t("op.haven.help", lang)},
            "horizon_years": {"default": 15.0, "min": 1.0, "max": 40.0,
                              "help": I18N.t("op.horizon.help", lang)},
        },
        "thresholds_paper": {
            "s2_crit": s1spec.THETA["s2_crit"].value,
            "s5_crit": s1spec.THETA["s5_crit"].value,
            "c1_crit": s1spec.CAPTURE["c1_crit"].value,
            "psi_crit": s1spec.COHERENCE["psi_crit"].value,
            "delta_crit": s1spec.COHERENCE["delta_crit"].value,
            "delta_c": s1spec.COHERENCE["delta_c"].value,
            "L2_s3_thresh": s1spec.LOOPS["L2_s3_thresh"].value,
            "L1_c1_thresh": s1spec.LOOPS["L1_c1_thresh"].value,
            "L1_s2_thresh": s1spec.LOOPS["L1_s2_thresh"].value,
            "psi_G_crit": s1spec.NETWORK["psi_G_crit"].value,
            "CAI_G_crit": s1spec.NETWORK["CAI_G_crit"].value,
        },
        "regime_bands": [{"name": n, "label": I18N.regime(n, lang),
                          "lo": lo, "hi": hi,
                          "stability": I18N.stability(st, lang)}
                         for n, lo, hi, st in s1spec.REGIME_BANDS],
        "coherence_tiers": [{"name": n, "label": I18N.tier(n, lang),
                             "lo": lo, "hi": hi}
                            for n, lo, hi in spec2.COHERENCE_TIERS],
        "loops": {k: {"name": I18N.t(f"loop.{k}.name", lang),
                      "source": I18N.t(
                          "loop.src.sccd" if k in ("L1", "L2", "L3", "L4")
                          else f"loop.src.{k}", lang),
                      "description": I18N.t(f"loop.{k}.desc", lang,
                                            strict=False)}
                  for k in ("L1", "L2", "L3", "L4",
                            "L5", "L6", "L7", "L8")},
        "adjustment_modes": {k: {"label": I18N.mode(k, lang),
                                 "desc": I18N.t(f"mode.{k}.desc", lang)}
                             for k in spec2.ADJUSTMENT_MODES},
        "ui": ui_strings(lang),
        "lang": lang,
    }


def _audit(lang: str = "vi") -> dict:
    lang = I18N.norm_lang(lang)
    return {
        "combined": LOC.localize_audit_headline(spec2.combined_audit(), lang),
        "v1_rows": s1spec.audit()["rows"],
        "v2_rows": LOC.localize_param_rows(spec2.audit2()["rows"], lang),
        "open_problems_v2": LOC.localize_open_problems(
            spec2.OPEN_PROBLEMS_V2, lang),
        "known_inconsistencies_v1": LOC.localize_inconsistencies(
            s1spec.KNOWN_INCONSISTENCIES, lang),
        "degrow_anchors": spec2.DEGROW_HISTORICAL_ANCHORS,
        "displacement_numbers": spec2.DISPL_STATED_NUMBERS,
        "theta25_gate_note": I18N.t("theta25.gate_note", lang),
        "level_vs_drift": {
            "level_targets": list(spec2.LEVEL_TARGETS),
            "drift_targets": list(spec2.DRIFT_TARGETS),
            "note": I18N.t("level_drift.note", lang,
                           level=", ".join(spec2.LEVEL_TARGETS),
                           drift=", ".join(spec2.DRIFT_TARGETS))},
        "ui": ui_strings(lang),
        "lang": lang,
    }


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "SCCD-X/2.00"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s - %s\n" % (self.address_string(), fmt % args))

    # -- helpers --
    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, obj: Any, code: int = 200):
        body = json.dumps(obj, ensure_ascii=False, allow_nan=False,
                          default=str).encode("utf-8")
        self._send(code, body, "application/json; charset=utf-8")

    def _err(self, code: int, msg: str, detail: str = ""):
        self._json({"error": msg, "detail": detail}, code)

    def _static(self, rel: str):
        path = os.path.normpath(os.path.join(WEB, rel.lstrip("/")))
        if not path.startswith(WEB) or not os.path.isfile(path):
            return self._err(404, f"not found: {rel}")
        ext = os.path.splitext(path)[1].lower()
        ctype = {".html": "text/html; charset=utf-8",
                 ".js": "text/javascript; charset=utf-8",
                 ".css": "text/css; charset=utf-8",
                 ".json": "application/json; charset=utf-8",
                 ".svg": "image/svg+xml"}.get(ext, "application/octet-stream")
        with open(path, "rb") as fh:
            self._send(200, fh.read(), ctype)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0:
            return {}
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception as e:
            raise ValueError(f"body is not valid JSON: {e}")

    # -- verbs --
    def do_OPTIONS(self):
        self._send(204, b"", "text/plain")

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        u = urlparse(self.path)
        p = u.path
        q = parse_qs(u.query or "")
        lang = I18N.norm_lang((q.get("lang") or [None])[0])
        try:
            if p in ("/", "/index.html"):
                return self._static("index.html")
            if p == "/api/v2/health":
                _, label = best_solver()
                return self._json({
                    "ok": True, "engine": "SCCD-X", "langs": list(I18N.LANGS),
                    "sccd_spec": s1spec.SPEC_VERSION,
                    "sccdx_spec": spec2.SPEC2_VERSION,
                    "ode_backend": label,
                    "python": sys.version.split()[0],
                    "endpoints": ["/api/v2/schema", "/api/v2/events",
                                  "/api/v2/presets", "/api/v2/audit",
                                  "POST /api/v2/diagnose",
                                  "POST /api/v2/world"]})
            if p == "/api/v2/schema":
                return self._json(_schema(lang))
            if p == "/api/v2/events":
                return self._json(LOC.localize_events(catalogue(), lang))
            if p == "/api/v2/presets":
                return self._json(LOC.localize_presets(preset_json(), lang))
            if p == "/api/v2/audit":
                return self._json(_audit(lang))
            if p.startswith("/api/"):
                return self._err(404, f"no such endpoint: {p}")
            return self._static(p)
        except Exception as e:
            traceback.print_exc()
            self._err(500, str(e), traceback.format_exc(limit=3))

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            body = self._body()
        except ValueError as e:
            return self._err(400, str(e))
        try:
            if p == "/api/v2/diagnose":
                return self._json(_do_diagnose(body))
            if p == "/api/v2/world":
                return self._json(_do_world(body))
            return self._err(404, f"no such endpoint: {p}")
        except ValueError as e:
            return self._err(400, f"bad input: {e}")
        except Exception as e:
            traceback.print_exc()
            self._err(500, str(e), traceback.format_exc(limit=4))


def main():
    # Line-buffer stdout so the startup banner appears immediately even when
    # output is redirected to a file or a pipe. It is the first thing a user
    # sees, and it carries the parameter census they need before reading any
    # result; a buffered banner shows up only after the server exits.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    host = os.environ.get("SCCDX_HOST", "127.0.0.1")
    port = int(os.environ.get("SCCDX_PORT", "8777"))
    _, label = best_solver()
    srv = ThreadingHTTPServer((host, port), Handler)
    print(f"SCCD-X engine  sccd v{s1spec.SPEC_VERSION} / "
          f"sccdx v{spec2.SPEC2_VERSION}")
    print(f"ODE backend : {label}"
          + ("" if label == "scipy" else
             "   (install scipy for the stiff solver Part IV 8.1 asks for)"))
    a = spec2.combined_audit()
    print(f"parameters  : v1 {a['v1']['counts']}  |  v2 {a['v2']['counts']}")
    print(f"listening   : http://{host}:{port}")
    print("Ctrl-C to stop.\n")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
        srv.server_close()


if __name__ == "__main__":
    main()
