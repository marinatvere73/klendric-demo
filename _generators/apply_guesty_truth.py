#!/usr/bin/env python3
"""
Apply Guesty revenue-truth occupancy corrections to property_scores.json.

Source of truth: cro_daily_brief 2026-05-05 validate_real_occupancy() output.
PriceLabs raw occupancy is INFORMATIONAL ONLY going forward.
Guesty paying-confirmed reservations (hostPayout > 0, source != owner/manual) is authoritative.
"""
import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "_data" / "property_scores.json"

# Guesty revenue truth occupancy from cro_daily_brief 2026-05-05
# Format: code -> {"guesty_occ_60d": int, "delta_pp": int}
GUESTY_TRUTH = {
    # Critical PL/Guesty deltas (from CRO brief Properties-To-Fix table)
    "ALX1433": {"guesty_occ_60d": 13, "pl_was": 80, "delta": 67},
    "ALX322":  {"guesty_occ_60d": 12, "pl_was": 67, "delta": 44},  # CRO brief shows 12% in underperformer list
    "ALX2213": {"guesty_occ_60d": 10, "pl_was": 57, "delta": 37},  # CRO brief shows 10% in underperformer list
    "SD3902":  {"guesty_occ_60d": 17, "pl_was": 53, "delta": 36},
    "SIE1825": {"guesty_occ_60d": 10, "pl_was": 47, "delta": 27},  # CRO brief shows 10%

    # Underperformers (CRO brief occ60<30%) — already low-scored but corrected
    "SD719":   {"guesty_occ_60d": 23},
    "ALX223":  {"guesty_occ_60d": 23},
    "QUA1990": {"guesty_occ_60d": 13},

    # Top performers (CRO brief validated) — minor corrections
    "ALX1734": {"guesty_occ_60d": 100},  # 100% holds
    "ALX3131": {"guesty_occ_60d": 87},   # was 52
    "ALX2434": {"guesty_occ_60d": 80},   # was 65
    "LOS1191": {"guesty_occ_60d": 80},   # was 70
    "SIE2301": {"guesty_occ_60d": 77},   # was 52
}

STALE_FIX_OVERRIDES = {
    "ALX1433": {
        "top_fix_1": "RETRACTED 2026-05-05: Prior 'raise base on strong occupancy' rec was based on stale PriceLabs data (PL 80% vs Guesty truth 13%). Real occ is 13% — investigate listing health, channel distribution, and pricing floor. Run full audit before any pricing move.",
        "top_fix_2": "Audit Airbnb/Vrbo channel status — 67pp PL/Guesty delta indicates listing may be paused, hidden, or owner-blocked on key channels.",
        "top_fix_3": "Pull the last 60 days of inquiries vs bookings to identify conversion failure point (no inquiries = visibility issue; inquiries no bookings = listing/price issue).",
        "biggest_concern": "STALE DATA RETRACTION: prior scorecard built on PriceLabs occupancy (80%) which materially overstated actual paying-revenue occupancy (13%). Score may need full re-derivation.",
        "data_confidence": "LOW — under audit",
    },
    "ALX322": {
        "top_fix_1": "RETRACTED 2026-05-05: Prior recs assumed 63-67% occupancy (PL). Guesty truth is 12% on a 60-day window. This is an underperformer, not a stable performer.",
        "top_fix_2": "Channel distribution audit — 44pp PL/Guesty delta is symptomatic of channel-level outage or owner block.",
        "top_fix_3": "Compare against ALX223/ALX1021 clone-set siblings; if all 3 show similar Guesty truth, the issue is portfolio-level not unit-level.",
        "biggest_concern": "STALE DATA RETRACTION: prior scorecard built on PriceLabs occupancy that overstated reality by 44pp.",
        "data_confidence": "LOW — under audit",
    },
    "ALX2213": {
        "top_fix_1": "RETRACTED 2026-05-05: Prior recs assumed 53-77% occupancy (PL). Guesty truth is 10% on a 60-day window. Clone-set underperformer alongside ALX223/ALX1021/ALX322.",
        "top_fix_2": "Channel distribution audit — 37pp PL/Guesty delta is symptomatic of channel-level outage or owner block.",
        "top_fix_3": "Re-merchandise differentiation against the other Alexander 1BR units; clone-set parity is killing conversion.",
        "biggest_concern": "STALE DATA RETRACTION: prior scorecard built on PriceLabs occupancy that overstated reality by 37pp.",
        "data_confidence": "LOW — under audit",
    },
    "SD3902": {
        "top_fix_1": "RE-ANCHORED 2026-05-05: Real Guesty occupancy is 17% (PL said 53%). With $449 hard floor and high-rate market position, this is expected for SD luxury — but the gap to recommendation needs review.",
        "top_fix_2": "Hold $449 floor (PERMANENT_RULE — never below). Review weekend ADR pickup and Comic-Con (T-78d) and Hot August Nights (T-91d) windows.",
        "top_fix_3": "Pull SD719 + SD3902 head-to-head to confirm SD market structural weakness vs property-level issues.",
        "biggest_concern": "Real occupancy lower than scorecard implied. Penthouse asset must be defended on rate, not occupancy — but 17% is a watchlist signal.",
        "data_confidence": "MEDIUM — luxury floor expected to compress occupancy; verify against SD comp set",
    },
    "SIE1825": {
        "biggest_concern": "STALE DATA NOTE: prior 23% occ_30d was directionally correct but Guesty 60d truth is 10% — underperformance is more severe than scorecard showed. Existing F-grade and triage rec stands.",
        "data_confidence": "LOW — confirmed underperformer, exact severity worse than displayed",
    },
}


def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    today = date.today().isoformat()
    data["metadata"]["last_corrected"] = today
    data["metadata"]["correction_source"] = "Guesty paying-confirmed reservations via cro_daily_brief.validate_real_occupancy()"
    data["metadata"]["occupancy_truth_standard"] = "Guesty hostPayout > 0, source != owner/manual, blocked-listing filter applied"

    corrections_applied = 0
    for p in data["properties"]:
        code = p["code"]
        if code in GUESTY_TRUTH:
            truth = GUESTY_TRUTH[code]
            old_occ_60 = p.get("occ_60d")
            new_occ_60 = truth["guesty_occ_60d"]
            p["occ_60d_pl_raw"] = old_occ_60
            p["occ_60d"] = new_occ_60  # Now Guesty truth
            p["occupancy_source"] = "guesty_revenue_truth"
            if "delta" in truth:
                p["pl_guesty_delta_pp"] = truth["delta"]
            corrections_applied += 1

        if code in STALE_FIX_OVERRIDES:
            overrides = STALE_FIX_OVERRIDES[code]
            for k, v in overrides.items():
                p[k] = v

        # Default data confidence for non-overridden properties
        if "data_confidence" not in p:
            if abs(p.get("occ_60d_pl_raw", p.get("occ_60d", 0)) - p.get("occ_60d", 0)) > 10:
                p["data_confidence"] = "MEDIUM"
            else:
                p["data_confidence"] = "HIGH"

        p["occupancy_source"] = p.get("occupancy_source", "guesty_revenue_truth_or_pl_aligned")

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Applied {corrections_applied} Guesty truth corrections to {DATA_FILE}")
    print(f"Stale-fix overrides applied: {len(STALE_FIX_OVERRIDES)}")


if __name__ == "__main__":
    main()
