"""Generate the LegacyLoop sample industrial corpus into data/raw/.

Every document is synthetic but internally consistent so that the three hero
questions cite real pages that actually contain the claimed facts.
"""
from __future__ import annotations

import csv
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from corpus_text import OISD_TEXT, VETERAN_MD

WIDTH, HEIGHT = A4


def _draw_page(c: canvas.Canvas, title: str, blocks: list, page_no: int, doc_id: str) -> None:
    """Render one PDF page: a title, wrapped text blocks, and a numbered footer."""
    y = HEIGHT - 28 * mm
    c.setFont("Helvetica-Bold", 15)
    c.drawString(22 * mm, y, title)
    y -= 4 * mm
    c.setLineWidth(0.6)
    c.line(22 * mm, y, WIDTH - 22 * mm, y)
    y -= 9 * mm
    for kind, text in blocks:
        if kind == "h":
            c.setFont("Helvetica-Bold", 11)
            y -= 2 * mm
        elif kind == "mono":
            c.setFont("Courier", 9.5)
        else:
            c.setFont("Helvetica", 10.5)
        for line in text.split("\n"):
            if y < 24 * mm:
                break
            c.drawString(24 * mm, y, line)
            y -= 5.4 * mm
        y -= 2.4 * mm
    c.setFont("Courier", 8)
    c.setFillGray(0.45)
    c.drawString(22 * mm, 14 * mm, doc_id)
    c.drawRightString(WIDTH - 22 * mm, 14 * mm, f"Page {page_no}")
    c.setFillGray(0)
    c.showPage()


def _write_pdf(path: str, doc_id: str, pages: list) -> None:
    """Write a multi-page PDF where pages is a list of (title, blocks)."""
    c = canvas.Canvas(path, pagesize=A4)
    for i, (title, blocks) in enumerate(pages, start=1):
        _draw_page(c, title, blocks, i, doc_id)
    c.save()


def make_mo_p204(raw: str) -> None:
    """3-page Kirloskar P-204 centrifugal pump maintenance manual excerpt."""
    p1 = [
        ("h", "1. Scope"),
        ("p", "This manual covers preventive and corrective maintenance for\n"
              "centrifugal pump P-204 (Kirloskar KDS-model, end-suction).\n"
              "It applies to reliability technicians and shift operators."),
        ("h", "2. Nameplate"),
        ("mono", "Tag        : P-204\nDuty       : Boiler feed transfer\n"
                 "Bearing    : DE 6309 / NDE 6209\nSeal       : Mechanical, single, balanced\n"
                 "PM interval: 1500 running hours (revised 2023)"),
        ("p", "For vibration limits and bearing criteria see Page 2."),
    ]
    p2 = [
        ("h", "3. Vibration Limits (per ISO 10816)"),
        ("mono", "Band       Velocity (mm/s)   Action\n"
                 "Normal     <= 4.5            Routine monitoring\n"
                 "Alert      4.5 - 7.1         Investigate, do not stop\n"
                 "Shutdown   >= 7.1            Trip and isolate"),
        ("p", "Continued operation above 5.5 mm/s in the alert band risks\n"
              "bearing damage and must be investigated the same shift."),
        ("h", "4. Bearing Housing Temperature"),
        ("p", "Record bearing housing temperature at every reading. A delta\n"
              "above 15 C from the commissioning baseline indicates\n"
              "lubrication failure and precedes most bearing trips on P-204."),
        ("h", "5. Bearing Inspection Checklist"),
        ("mono", "[ ] Housing temp delta vs baseline\n[ ] Grease colour / consistency\n"
                 "[ ] Audible thud or grinding\n[ ] Axial / radial end play"),
    ]
    p3 = [
        ("h", "6. Mechanical Seal Condition Matrix"),
        ("mono", "Symptom            Likely cause        Action\n"
                 "Weeping at gland   Face wear           Schedule replace\n"
                 "Flush press drop   Clogged orifice     Clean flush line\n"
                 "Steam/vapour       Face lift-off       Stop, inspect"),
        ("p", "P-204 has a recorded history of seal-related trips at vibration\n"
              "levels in the 5.5 - 6.5 mm/s range. Inspect the seal before\n"
              "attributing high vibration solely to the bearing."),
        ("h", "7. Coupling"),
        ("p", "Check coupling bolt torque (spec 45 Nm) during any high-vibration\n"
              "investigation. Loose coupling bolts mimic bearing symptoms."),
    ]
    _write_pdf(os.path.join(raw, "MO-P204-2024.pdf"), "MO-P204-2024", [
        ("Maintenance Manual — Pump P-204", p1),
        ("Maintenance Manual — Pump P-204", p2),
        ("Maintenance Manual — Pump P-204", p3),
    ])


def make_sop_vib(raw: str) -> None:
    """2-page SOP for high-vibration response, references OISD-105."""
    p1 = [
        ("h", "Purpose"),
        ("p", "Standard operating procedure SOP-VIB-A defines the field response\n"
              "to a high-vibration alarm on rotating equipment. Compliant with\n"
              "OISD-105 general safe-operating requirements."),
        ("h", "Procedure"),
        ("p", "1. Acknowledge the alarm and record the velocity reading (mm/s).\n"
              "2. Classify the band per the equipment vibration table.\n"
              "3. Inspect bearing housing temperature and grease condition.\n"
              "4. Inspect the mechanical seal and coupling bolt torque.\n"
              "5. Cross-check the last three trend readings for rate of rise.\n"
              "6. If in the alert band, continue with monitoring every 30 min.\n"
              "7. If shutdown band is reached, trip and isolate immediately."),
    ]
    p2 = [
        ("h", "Escalation"),
        ("p", "If velocity rises more than 1.0 mm/s within one shift, escalate to\n"
              "the reliability engineer regardless of absolute band. Log the\n"
              "escalation in the shift handover under OISD-105 record-keeping."),
        ("h", "Records"),
        ("p", "Retain the vibration log, the inspection checklist, and any\n"
              "corrective work order for a minimum of two years."),
    ]
    _write_pdf(os.path.join(raw, "SOP-VIB-A.pdf"), "SOP-VIB-A", [
        ("SOP-VIB-A — High-Vibration Response", p1),
        ("SOP-VIB-A — High-Vibration Response", p2),
    ])


def make_incident(raw: str) -> None:
    """1-page incident report for the 2023-04-17 P-204 bearing trip."""
    p1 = [
        ("mono", "Incident No : INC-2023-04-17\nEquipment   : P-204\n"
                 "Date        : 2023-04-17\nDetected at : 6.2 mm/s (shutdown band)"),
        ("h", "Event"),
        ("p", "Pump P-204 tripped on high vibration at 6.2 mm/s. Bearing failure\n"
              "confirmed on strip-down. A minor seal weep was noted prior to the\n"
              "trip, consistent with the pump's seal-related trip history."),
        ("h", "Root Cause"),
        ("p", "Lubrication interval exceeded. Grease had degraded past service\n"
              "limit, raising bearing housing temperature before failure."),
        ("h", "Corrective Action"),
        ("p", "Revised preventive maintenance schedule from 2000 hrs to 1500 hrs.\n"
              "Added bearing housing temperature to the daily operator round."),
    ]
    _write_pdf(os.path.join(raw, "Incident-2023-04-17.pdf"), "Incident-2023-04-17", [
        ("Incident Report — Pump P-204", p1),
    ])


def make_permit(raw: str) -> None:
    """3-page confined-space permit for the 2024-11-08 entry (OISD-105)."""
    p1 = [
        ("mono", "Permit No   : PTW-2024-11-08\nType        : Confined Space Entry\n"
                 "Vessel      : Surge drum V-401A\nDate        : 2024-11-08"),
        ("h", "3.1 Permit-to-Work"),
        ("p", "Permit issued 13:40 and signed by the issuing authority and the\n"
              "performing authority. Valid for one shift only."),
        ("h", "3.3 Standby Attendant"),
        ("p", "Standby attendant assigned by name: S. Deshmukh. Stationed at the\n"
              "manway for the full duration of the entry."),
    ]
    p2 = [
        ("h", "3.2 Gas Test Log"),
        ("mono", "Time    O2%    LEL%   H2S ppm  CO ppm\n"
                 "13:50   20.9   0      0        0\n"
                 "14:10   20.9   0      0        0\n"
                 "14:22   20.8   0      0        0\n"
                 "  --- monitoring gap 14:22 to 14:47 ---\n"
                 "14:47   20.9   0      0        0\n"
                 "15:05   20.9   0      0        0"),
        ("h", "3.4 Continuous Monitoring"),
        ("p", "Continuous atmosphere monitoring required throughout entry. A gap\n"
              "of 25 minutes (14:22 to 14:47) was recorded due to a monitor\n"
              "battery swap and is flagged as a deviation."),
    ]
    p3 = [
        ("h", "3.4 Rescue Equipment Checklist"),
        ("mono", "[x] Tripod and winch rigged\n[x] SCBA sets x2 staged\n"
                 "[x] Rescue harness donned\n[x] Communications tested"),
        ("h", "3.5 Post-Entry Closure"),
        ("p", "Entry completed 15:20. Headcount verified. Permit closed and\n"
              "signed off by the issuing authority at 15:28."),
    ]
    _write_pdf(os.path.join(raw, "Permit-2024-11-08.pdf"), "Permit-2024-11-08", [
        ("Confined Space Entry Permit — V-401A", p1),
        ("Confined Space Entry Permit — V-401A", p2),
        ("Confined Space Entry Permit — V-401A", p3),
    ])


def make_c11_csv(raw: str) -> None:
    """24-row C-11 compressor maintenance history with a 4-month failure cycle."""
    header = ["date", "work_order", "equipment_tag", "symptom",
              "action_taken", "technician", "downtime_hrs"]
    # Failures (~every 4 months) land on rows 4, 8, 12, 16, 20, 24 (1-indexed data rows).
    fail = ("high discharge temp, filter dP high",
            "inlet-filter replacement", "8.0")
    routine = ("routine PM", "greasing and inspection", "1.0")
    rows = []
    dates = [
        "2022-01-12", "2022-02-15", "2022-03-20", "2022-04-18",   # 1-4 (fail@4, monsoon pre-season humidity)
        "2022-05-22", "2022-06-25", "2022-07-14", "2022-08-16",   # 5-8 (fail@8, monsoon)
        "2022-09-19", "2022-10-21", "2022-11-23", "2022-12-14",   # 9-12 (fail@12)
        "2023-01-17", "2023-02-19", "2023-03-22", "2023-04-15",   # 13-16 (fail@16)
        "2023-05-18", "2023-06-20", "2023-07-13", "2023-08-15",   # 17-20 (fail@20, monsoon)
        "2023-09-18", "2023-10-20", "2023-11-22", "2023-12-12",   # 21-24 (fail@24)
    ]
    techs = ["A. Rao", "M. Iyer", "S. Deshmukh", "P. Nair"]
    for i, d in enumerate(dates, start=1):
        wo = f"WO-{2200 + i:04d}"
        if i % 4 == 0:
            sym, act, dt = fail
        else:
            sym, act, dt = routine
        rows.append([d, wo, "C-11", sym, act, techs[i % 4], dt])
    with open(os.path.join(raw, "compressor-C11-history.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def make_text_files(raw: str) -> None:
    """Write the OISD excerpt and the veteran interview transcript."""
    with open(os.path.join(raw, "OISD-105-confined-space.txt"), "w") as f:
        f.write(OISD_TEXT)
    with open(os.path.join(raw, "veteran-interview-RK-Sharma.md"), "w") as f:
        f.write(VETERAN_MD)


def build_corpus(raw_dir: str) -> list:
    """Generate all seven corpus files into raw_dir and return their names."""
    os.makedirs(raw_dir, exist_ok=True)
    make_mo_p204(raw_dir)
    make_sop_vib(raw_dir)
    make_incident(raw_dir)
    make_permit(raw_dir)
    make_c11_csv(raw_dir)
    make_text_files(raw_dir)
    return sorted(os.listdir(raw_dir))
