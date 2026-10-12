# -*- coding: utf-8 -*-
"""
SCCD-X — Extended Feedback Loop Diagnostics (L5-L8)
====================================================
sccd Part IV 2 specifies four loops. The two new papers describe four more
mechanisms that are loops in the same sense - a quantity whose increase
produces conditions that increase it further - and this module tests them.

  L5  Agency-Legitimacy Spiral      [DISPL 4.4]
  L6  Legibility-Extraction Spiral  [DEGROW 2.1 x DISPL 5.4]
  L7  Demographic Inversion Trap    [DEGROW Invert the Welfare Pyramid]
  L8  Youth-Surplus Discharge       [DEGROW Stages 2-3]

L6 is the one worth reading twice. Degrow and Displacement arrive at the same
failure mode from opposite ends - demography and psychology - and neither
paper mentions the other. Degrow: the late-Ming state raising rates on
centuries-stale land registers, "like continuing to milk a cow that was
already emaciated to the bone". Displacement: the base relocating into
physical metal that no register can see. The spiral is identical; only the
hiding place changed.

CAI ACCOUNTING
--------------
Two numbers are reported and they are not interchangeable:

  cai_core  L1-L4 only, scored and banded EXACTLY as sccd Part IV eq (CAI)
            specifies. Directly comparable to any v1.00 output.
  cai_ext   L1-L8, with the paper's band edges rescaled by 4/8 because they
            were set against four loops. Flagged UNCALIBRATED-EXT.

Reporting only cai_ext would silently inflate every historical comparison;
reporting only cai_core would discard the new loops. So both, always.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional

from sccd import spec as s1spec
from sccd import loops as l1
from sccd.aggregate import SubComponents, legitimacy_multiplier
from . import spec2
from .forcing import Forcing, DemoBlock, DispBlock


@dataclass
class LoopState2:
    """One loop's state. Carries i18n KEYS plus the numbers that go into
    them, never a rendered sentence - see i18n.py for why."""
    loop: str
    active: bool
    margin: float
    name_key: str              # "loop.L6.name"
    detail_key: str            # "loop.L6.detail"
    detail_args: dict          # the numbers the template formats
    source_key: str            # "loop.src.L6"
    uncalibrated: bool = True

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class LoopDiagnosis2:
    loops: Dict[str, LoopState2]          # L1..L8
    cai_core: float
    cai_ext: float
    active: List[str]
    synchronised: List[str]
    cai_core_band_key: str
    cai_core_horizon_key: str
    cai_ext_band_key: str
    cai_ext_horizon_key: str
    uncalibrated_loops: List[str]
    overlap_codes: List[tuple] = field(default_factory=list)

    def as_dict(self) -> dict:
        d = asdict(self)
        d["loops"] = {k: v.as_dict() for k, v in self.loops.items()}
        d["overlap_codes"] = [list(c) for c in self.overlap_codes]
        return d


# ===========================================================================
#  L5 - Agency-Legitimacy Spiral
# ===========================================================================
def test_L5(ap: DispBlock, sc: SubComponents, s3_drift: float,
            p: Optional[dict] = None) -> LoopState2:
    """Active when AI is at mass penetration, agency erosion is past its
    crisis level, AND legitimacy is actually drifting down.

    The third condition is what keeps this from being a restatement of the
    first two: a polity can show high a1 and high a3 while S3 holds, if
    something else is pushing legitimacy up. The loop only runs when the
    drain is winning.

    Return leg: S3 down -> lambda down -> delivery capacity down -> visible
    policy failure -> further loss of meaning and authorship. The lambda
    mechanism is sccd's own (eq 2-3); only the drain is new.
    """
    p = p or {}
    g = lambda k: p.get(k, spec2.DISP[k].value)
    a1_t, a3_t = g("a1_mass_thresh"), g("a3_crisis_thresh")

    c_pen = ap.a1 > a1_t
    c_ag = ap.a3 > a3_t
    c_dr = s3_drift < -0.005
    active = c_pen and c_ag and c_dr

    lam = legitimacy_multiplier(sc.s3)
    margin = min(ap.a1 - a1_t, ap.a3 - a3_t, -s3_drift - 0.005)
    return LoopState2(
        "L5", active, margin, "loop.L5.name", "loop.L5.detail",
        {"a1": f"{ap.a1:.2f}", "a1_t": f"{a1_t:.2f}", "c_pen": c_pen,
         "a3": f"{ap.a3:.2f}", "a3_t": f"{a3_t:.2f}", "c_ag": c_ag,
         "drift": f"{s3_drift:+.4f}", "c_dr": c_dr, "lam": f"{lam:.3f}"},
        "loop.src.L5")


# ===========================================================================
#  L6 - Legibility-Extraction Spiral   [THE CROSS-PAPER LOOP]
# ===========================================================================
def test_L6(F: Forcing, ap: DispBlock, p: Optional[dict] = None) -> LoopState2:
    """Active when the extraction squeeze exceeds its threshold AND haven
    reallocation is already past flight level.

    squeeze = tau_demanded - tau_feasible, both computed in forcing.py from
    sccd's own eq (17) rate. A positive squeeze means the fiscal programme
    needs more than the legible base can yield at any politically available
    rate. The state's only short-run move is to lean harder on what it can
    still see, which is exactly what pushes the next tranche of wealth out of
    sight.

    Note the asymmetry that makes this loop hard to exit: raising a4 is a
    private decision taken once, while lowering it requires the holder to
    trust the register again. Capital controls can close jurisdiction exit in
    a weekend; no decree recalls metal from a domestic vault.
    """
    p = p or {}
    g = lambda k: p.get(k, spec2.DISP[k].value)
    sq_t, a4_t = g("squeeze_thresh"), g("a4_flight_thresh")
    sq = F.disp.extraction_squeeze

    c_sq = sq > sq_t
    c_fl = ap.a4 > a4_t
    active = c_sq and c_fl
    margin = min(sq - sq_t, ap.a4 - a4_t)
    return LoopState2(
        "L6", active, margin, "loop.L6.name", "loop.L6.detail",
        {"sq": f"{sq:+.4f}", "sq_t": f"{sq_t:.2f}", "c_sq": c_sq,
         "dem": f"{F.disp.tau_demanded:.4f}",
         "feas": f"{F.disp.tau_feasible:.4f}",
         "a4": f"{ap.a4:.2f}", "a4_t": f"{a4_t:.2f}", "c_fl": c_fl,
         "phys": f"{F.disp.physical_share:.2f}"},
        "loop.src.L6")


# ===========================================================================
#  L7 - Demographic Inversion Trap
# ===========================================================================
def test_L7(dm: DemoBlock, p: Optional[dict] = None) -> LoopState2:
    """Active when dependency inversion and the expectation trap are both
    past threshold AND the polity is in voluntary adjustment mode.

    The d3 condition matters: in a society without voluntary instruments, the
    expectation trap does not convert into fertility refusal, so this loop
    cannot close. It is specifically a rich-aging-society trap. Degrow states
    both arms - the inverting welfare pyramid, and the expectation trap - but
    never joins them; joining them is what makes it a loop.
    """
    p = p or {}
    g = lambda k: p.get(k, spec2.DEMO[k].value)
    d4_t, d2_t, d3_t = (g("d4_inversion_thresh"), g("d2_trap_thresh"),
                        g("d3_voluntary_thresh"))
    c4_, c2_, c3_ = dm.d4 > d4_t, dm.d2 > d2_t, dm.d3 > d3_t
    active = c4_ and c2_ and c3_
    margin = min(dm.d4 - d4_t, dm.d2 - d2_t, dm.d3 - d3_t)
    return LoopState2(
        "L7", active, margin, "loop.L7.name", "loop.L7.detail",
        {"d4": f"{dm.d4:.2f}", "d4_t": f"{d4_t:.2f}", "c4": c4_,
         "d2": f"{dm.d2:.2f}", "d2_t": f"{d2_t:.2f}", "c2": c2_,
         "d3": f"{dm.d3:.2f}", "d3_t": f"{d3_t:.2f}", "c3": c3_},
        "loop.src.L7")


# ===========================================================================
#  L8 - Youth-Surplus Discharge
# ===========================================================================
def test_L8(dm: DemoBlock, sc: SubComponents, F: Forcing,
            p: Optional[dict] = None) -> LoopState2:
    """Active when surplus youth is past threshold, voluntary instruments are
    absent, AND the coercive monopoly is weak enough to be contested.

    The S2 condition uses sccd's own L1 threshold (0.60, PAPER) as the mark of
    a contestable monopoly. Below it the reserve army has somewhere to go.

    This is the loop that lets the engine read the young half of the world.
    L5-L7 are all rich-aging-society loops; without L8 the instrument would
    be blind to precisely the polities where Degrow's ancient mechanism is
    the live one.
    """
    p = p or {}
    gd = lambda k: p.get(k, spec2.DEMO[k].value)
    d5_t, d3_t = gd("d5_violent_thresh"), gd("d3_voluntary_thresh")
    s2_t = p.get("L1_s2_thresh", s1spec.LOOPS["L1_s2_thresh"].value)

    c5_, c3_, cs2 = dm.d5 > d5_t, dm.d3 < d3_t, sc.s2 < s2_t
    active = c5_ and c3_ and cs2
    margin = min(dm.d5 - d5_t, d3_t - dm.d3, s2_t - sc.s2)
    return LoopState2(
        "L8", active, margin, "loop.L8.name", "loop.L8.detail",
        {"d5": f"{dm.d5:.2f}", "d5_t": f"{d5_t:.2f}", "c5": c5_,
         "d3": f"{dm.d3:.2f}", "d3_t": f"{d3_t:.2f}", "c3": c3_,
         "s2": f"{sc.s2:.2f}", "s2_t": f"{s2_t:.2f}", "cs2": cs2,
         "pv": f"{F.demo.pressure_violent:.3f}"},
        "loop.src.L8")


# ===========================================================================
#  CAI
# ===========================================================================
def _band_core(cai: float) -> tuple[str, str]:
    """sccd Part IV eq (CAI) bands, verbatim. Returns i18n KEYS."""
    if cai <= 0.0:
        return "cai.damped", "cai.h.damped"
    if cai <= 2.0:
        return "cai.manageable", "cai.h.manageable"
    if cai <= 3.0:
        return "cai.compounding", "cai.h.compounding"
    return "cai.imminent", "cai.h.imminent"


def _band_ext(cai_ext: float) -> tuple[str, str]:
    """Same edges, rescaled for eight loops instead of four."""
    return _band_core(cai_ext * spec2.CAI_EXT_SCALE.value)


def diagnose_loops2(F: Forcing, dm: DemoBlock, ap: DispBlock,
                    revenue_polarisation: float = 0.0,
                    p: Optional[dict] = None) -> LoopDiagnosis2:
    """Run L1-L4 (sccd, on the EFFECTIVE components) plus L5-L8."""
    p = p or {}
    sc = F.effective

    # sccd decides ACTIVATION for L1-L4 so v1 parity is exact; the detail
    # strings are rebuilt here from the same values as i18n keys, because
    # v1's are English prose and this engine must not emit prose.
    base = l1.diagnose(sc, revenue_polarisation=revenue_polarisation, p=p)
    gp = lambda k, grp: p.get(k, grp[k].value)

    c1_t = gp("L1_c1_thresh", s1spec.LOOPS)
    s2_t = gp("L1_s2_thresh", s1spec.LOOPS)
    s3_t = gp("L2_s3_thresh", s1spec.LOOPS)
    lam_t = gp("L2_lambda_thresh", s1spec.LOOPS)
    c5_t = gp("L3_c5_thresh", s1spec.LOOPS)
    rp_t = gp("L3_revpol_thresh", s1spec.LOOPS)
    c4_t = gp("L4_c4_thresh", s1spec.LOOPS)
    c1_t4 = gp("L4_c1_thresh", s1spec.LOOPS)
    lam = legitimacy_multiplier(sc.s3, p.get("lambda_min"),
                                p.get("lambda_max"), p.get("k"),
                                p.get("s3_mid"))

    l2_status = ("loop.L2.explosive" if base.loops["L2"].active
                 else ("loop.L2.approaching" if sc.s3 < s3_t + 0.10
                       else "loop.L2.damped"))

    args14 = {
        "L1": {"c1": f"{sc.c1:.2f}", "c1_t": f"{c1_t:.2f}",
               "c1_s": "loop.L1.over" if sc.c1 > c1_t else "loop.L1.under",
               "s2": f"{sc.s2:.2f}", "s2_t": f"{s2_t:.2f}",
               "s2_s": "loop.L1.below" if sc.s2 < s2_t else "loop.L1.above"},
        "L2": {"s3": f"{sc.s3:.2f}", "s3_t": f"{s3_t:.2f}",
               "lam": f"{lam:.3f}", "lam_t": f"{lam_t:.2f}",
               "status": l2_status},
        "L3": {"c5": f"{sc.c5:.2f}", "c5_t": f"{c5_t:.2f}",
               "rp": f"{revenue_polarisation:.2f}", "rp_t": f"{rp_t:.2f}"},
        "L4": {"c4": f"{sc.c4:.2f}", "c4_t": f"{c4_t:.2f}",
               "c1": f"{sc.c1:.2f}", "c1_t": f"{c1_t4:.2f}"},
    }

    loops: Dict[str, LoopState2] = {}
    for k, st in base.loops.items():
        loops[k] = LoopState2(
            loop=k, active=st.active, margin=st.margin,
            name_key=f"loop.{k}.name", detail_key=f"loop.{k}.detail",
            detail_args=args14[k], source_key="loop.src.sccd",
            uncalibrated=st.uncalibrated)

    loops["L5"] = test_L5(ap, sc, F.drifts.get("s3", 0.0), p)
    loops["L6"] = test_L6(F, ap, p)
    loops["L7"] = test_L7(dm, p)
    loops["L8"] = test_L8(dm, sc, F, p)

    def score(keys) -> float:
        tot = 0.0
        for k in keys:
            if not loops[k].active:
                continue
            if k in ("L1", "L2", "L3", "L4"):
                cw = p.get(f"coupling_{k}", s1spec.LOOP_COUPLING_WEIGHT[k].value)
                sp = p.get(f"speed_{k}", s1spec.LOOP_SPEED[k].value)
            else:
                cw = p.get(f"coupling_{k}", spec2.LOOP2_COUPLING_WEIGHT[k].value)
                sp = p.get(f"speed_{k}", spec2.LOOP2_SPEED[k].value)
            tot += cw * sp
        return tot

    cai_core = score(("L1", "L2", "L3", "L4"))
    cai_ext = score(loops.keys())
    cb, ch = _band_core(cai_core)
    eb, eh = _band_ext(cai_ext)

    active = [k for k in sorted(loops) if loops[k].active]
    sync = [k for k in active
            if any(t in active for t in spec2.CROSS_COUPLING2.get(k, []))]

    warn: List[tuple] = []
    if "L8" in active and "L2" in active:
        warn.append(("warn.overlap_L8_L2", {}))
    if "L6" in active and "L4" in active:
        warn.append(("warn.overlap_L6_L4", {}))

    return LoopDiagnosis2(
        loops=loops,
        cai_core=cai_core, cai_core_band_key=cb, cai_core_horizon_key=ch,
        cai_ext=cai_ext, cai_ext_band_key=eb, cai_ext_horizon_key=eh,
        active=active, synchronised=sync,
        uncalibrated_loops=[k for k in sorted(loops) if loops[k].uncalibrated],
        overlap_codes=warn,
    )
