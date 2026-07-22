"""Long-form text corpus content, kept separate so corpus_gen stays small.

OISD_TEXT is the regulatory excerpt cited by hero question 3; VETERAN_MD is the
tacit-knowledge interview cited by hero question 1.
"""

OISD_TEXT = """OISD-105 — Work Permit System and Confined Space Entry (Excerpt)

Section 3 — Confined Space Entry Requirements

3.1 Permit-to-Work
No person shall enter a confined space without a valid entry permit issued
and signed by the designated issuing authority. The permit shall record the
vessel identity, the scope of work, the validity window, and the names of the
issuing and performing authorities. The permit is valid for a single shift.

3.2 Atmospheric Gas Testing
Before entry, the atmosphere shall be tested for oxygen (19.5 to 23.5 percent),
flammable gas (LEL below 5 percent), hydrogen sulphide, and carbon monoxide.
Readings shall be logged with the time of measurement. Testing shall be
repeated at defined intervals and the results retained with the permit.

3.3 Standby Attendant
A trained standby attendant shall be assigned by name and stationed at the
entry point for the entire duration of the entry. The attendant maintains a
headcount and continuous communication with the entrants.

3.4 Continuous Monitoring and Rescue Readiness
Continuous atmosphere monitoring shall be maintained throughout the entry.
Any interruption in monitoring is a reportable deviation and must be
investigated. Rescue equipment, including retrieval and breathing apparatus,
shall be staged and its checklist signed before entry begins.

3.5 Closure
On completion, the performing authority verifies the headcount, withdraws all
entrants, and returns the permit to the issuing authority for closure and
sign-off. Closed permits are retained for audit.
"""


VETERAN_MD = """# Veteran Interview — R.K. Sharma (Retiring, 22 years on rotating equipment)

Recorded 2024-10-30. Knowledge capture session before retirement.

## Pumps

**Interviewer:** Any tricks on P-204 that are not in the manual?

**R.K. Sharma:** On P-204 specifically, if you feel a low-frequency thud at
the discharge flange, it is almost always the coupling bolts, not the bearing.
Torque check first, it saves an hour of chasing the wrong fault. The bearing
gives you a higher, grinding note; the coupling gives you a dull thud you feel
more than you hear.

Second thing on P-204: watch the housing temperature, not just the vibration.
The pump tells you it is unhappy through heat a full shift before the number on
the vibration meter moves.

## Compressors

**Interviewer:** And C-11, the one that keeps failing?

**R.K. Sharma:** C-11 is seasonal. Every monsoon the inlet filter loads up
with moisture and dust and the discharge temperature climbs. People blame the
valves, but nine times out of ten it is the filter. Shorten the filter change
in the wet months and the problem disappears.

## Three tricks not in any manual

1. On any single mechanical seal, a faint steam wisp at start-up that clears in
   two minutes is normal thermal lift-off, not a failure. Do not stop the pump.
2. Grease colour tells you more than grease smell. Grey means metal, and metal
   means you are already late.
3. Keep one spare coupling insert per pump family in the shift box. The store
   never has the right one at 3 AM.
"""
