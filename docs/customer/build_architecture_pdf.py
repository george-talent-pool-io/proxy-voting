"""Build the customer architecture brief; no product code or model is executed.

Rebuild with the isolated document environment:
  uv venv artifacts/customer-document-venv
  uv pip install --python artifacts/customer-document-venv/bin/python \
      reportlab==4.4.10 pypdf==6.1.3
  artifacts/customer-document-venv/bin/python docs/customer/build_architecture_pdf.py

Source Sans 3 is embedded under the adjacent SIL Open Font License.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfdoc import PDFString
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Voting_Intelligence_Framework_Architecture.pdf"
W, H = A4
M = 44
CW = W - M * 2
NAVY = "#142C44"
INK = "#20364A"
MUTED = "#53677A"
TEAL = "#117D78"
LINE = "#D5DEE6"
PALE = "#F2F6F8"
GREEN = "#EAF4F2"
AMBER = "#99612C"
WARM = "#FAF3E9"
WHITE = "#FFFFFF"
VERSION = "1.1"
DATE = "19 October 2026"


class Brief:
    def __init__(self):
        for family, filename in (("Source", "SourceSans3-Regular.ttf"),
                                 ("SourceSemi", "SourceSans3-Semibold.ttf"),
                                 ("SourceBold", "SourceSans3-Bold.ttf")):
            pdfmetrics.registerFont(TTFont(family, str(ROOT / "assets/fonts" / filename)))
        pdfmetrics.registerFontFamily("Source", normal="Source", bold="SourceBold")
        self.c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1, invariant=1,
                               initialFontName="Source", initialFontSize=11)
        self.c.setTitle("Voting Intelligence Framework | Layered Classification, Confidence & Learning")
        self.c.setAuthor("Voting Intelligence Framework")
        self.c.setSubject("Customer-controlled proxy-voting classification, learning, calibration and qualification")
        self.c.setKeywords("ISO 15022, proxy voting, layered classification, learning, calibration, qualification, human review")
        self.c.setCreator(f"Customer architecture document generator v{VERSION}")
        self.c._doc.Catalog.Lang = PDFString("en-GB")
        self.page = 0
        self.blocks = []

    def rect(self, x, top, width, height, fill=WHITE, stroke=None, line_width=0.7):
        self.c.setFillColor(colors.HexColor(fill))
        self.c.setLineWidth(line_width)
        if stroke:
            self.c.setStrokeColor(colors.HexColor(stroke))
        self.c.rect(x, H - top - height, width, height, fill=1, stroke=bool(stroke))

    def line(self, x1, top1, x2, top2, color=LINE, width=0.7):
        self.c.setStrokeColor(colors.HexColor(color))
        self.c.setLineWidth(width)
        self.c.line(x1, H - top1, x2, H - top2)

    def p(self, text, x, top, width, size=11, leading=None, color=INK,
          font="Source", align=TA_LEFT, max_height=None, name=None):
        style = ParagraphStyle("text", fontName=font, fontSize=size,
                               leading=leading or size * 1.30,
                               textColor=colors.HexColor(color), alignment=align,
                               spaceBefore=0, spaceAfter=0, allowWidows=0,
                               allowOrphans=0, splitLongWords=False)
        para = Paragraph(text, style)
        _, height = para.wrap(width, H)
        if max_height is not None and height > max_height + .05:
            raise ValueError(f"Page {self.page}: text exceeds allocated height ({height:.1f}>{max_height}): {text}")
        if top + height > H - 19 or x < 25 or x + width > W - 25:
            raise ValueError(f"Page {self.page}: text outside print area: {text}")
        para.drawOn(self.c, x, H - top - height)
        self.blocks.append({"page": self.page, "text": text, "x": x, "top": top,
                            "width": width, "height": height, "name": name})
        return height

    def label(self, text, x, top, width=CW, color=TEAL, size=8.3, align=TA_LEFT):
        return self.p(text, x, top, width, size, size * 1.2, color, "SourceSemi", align)

    def arrow(self, points, color=MUTED, width=1.05, head=4.4):
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            self.line(x1, y1, x2, y2, color, width)
        x, y = points[-1]
        px, py = points[-2]
        theta = math.atan2(y - py, x - px)
        for offset in (-.48, .48):
            self.line(x, y, x - head * math.cos(theta + offset),
                      y - head * math.sin(theta + offset), color, width)

    def box(self, x, top, width, height, title, body="", fill=PALE,
            accent=TEAL, title_size=11.7, body_size=10, centered=False):
        self.rect(x, top, width, height, fill, LINE)
        self.rect(x, top, 3, height, accent)
        align = TA_CENTER if centered else TA_LEFT
        title_height = self.p(title, x + 13, top + 9, width - 26, title_size,
                              title_size * 1.2, INK, "SourceSemi", align,
                              max_height=height - 17)
        if body:
            self.p(body, x + 13, top + 13 + title_height, width - 26,
                   body_size, body_size * 1.20, MUTED, align=align,
                   max_height=height - 22 - title_height)

    def start(self, slug, eyebrow, title, subtitle):
        self.page += 1
        self.c.bookmarkPage(slug)
        self.c.addOutlineEntry(title, slug, level=0, closed=False)
        self.label("VOTING INTELLIGENCE FRAMEWORK", M, 29, 270, NAVY, 9)
        self.label("CUSTOMER ARCHITECTURE", W - M - 180, 29, 180, MUTED, 8, TA_RIGHT)
        self.line(M, 50, W - M, 50)
        self.label(eyebrow.upper(), M, 69)
        self.p(title, M, 88, CW, 28, 31.5, NAVY, "SourceSemi", max_height=34)
        self.p(subtitle, M, 132, CW, 11.2, 14.5, MUTED, max_height=31)

    def end(self):
        self.line(M, 802, W - M, 802)
        self.p(f"Architecture & qualification workflow  /  v{VERSION}", M, 811, 290,
               8, 9.5, MUTED)
        self.p(f"{DATE}     {self.page:02d} / 07", W - M - 190, 811, 190,
               8, 9.5, MUTED, align=TA_RIGHT)
        self.c.showPage()

    def cover(self):
        self.page = 1
        self.c.bookmarkPage("overview")
        self.c.addOutlineEntry("Overview", "overview", level=0, closed=False)
        self.rect(0, 0, W, 384, NAVY)
        self.rect(M, 86, 38, 3, "#61C3B1")
        self.label("VOTING INTELLIGENCE FRAMEWORK", M, 40, 300, WHITE, 10)
        self.label("ARCHITECTURE BRIEF", W - M - 160, 41, 160, "#B8CEDD", 8, TA_RIGHT)
        self.p("Voting Intelligence", M, 118, CW, 43, 48, WHITE, "SourceSemi")
        self.p("Framework", M, 170, CW, 43, 48, WHITE, "SourceSemi")
        self.p("Layered classification. Calibrated confidence.<br/>Continuous learning, qualified for your corpus.", M, 248,
               CW, 17.5, 23, "#D9E6EF", max_height=55)
        self.p("ISO 15022 and narrative notices  /  Customer-controlled processing", M, 341,
               CW, 11, 14, "#B8CEDD")

        self.label("ONE CONTROLLED QUALIFICATION LIFECYCLE", M, 416)
        self.p("Learn from reviewed examples. Validate independently.<br/>Release only within a measured operating policy.",
               M, 437, CW, 13.6, 18, INK, max_height=39)
        gap = 7
        cell = (CW - gap * 6) / 7
        names = ["Frozen<br/>foundation", "Customer<br/>training", "Validation<br/>selection",
                 "Model<br/>freeze", "Confidence<br/>calibration", "Independent<br/>qualification",
                 "Monitored<br/>release"]
        for i, title in enumerate(names):
            x = M + i * (cell + gap)
            self.line(x, 502, x + cell, 502, TEAL, 2)
            self.p(f"0{i+1}", x, 513, cell, 12, 15, TEAL, "SourceSemi")
            self.p(title, x, 536, cell + 1, 9.6, 12, INK, "SourceSemi", max_height=26)

        col = (CW - 32) / 2
        self.p("A framework that learns", M, 609, col, 14, 17, NAVY, "SourceSemi")
        self.p("Frozen foundations, customer-specific training and a repeatable path to release qualification.",
               M, 637, col, 11, 14.8, MUTED, max_height=48)
        self.p("Decisions that remain accountable", M + col + 32, 609, col, 14, 17,
               NAVY, "SourceSemi", max_height=35)
        self.p("Source evidence, scoped confidence, human review and versioned learning from operational feedback.",
               M + col + 32, 637, col, 11, 14.8, MUTED, max_height=48)
        self.rect(M, 730, CW, 48, GREEN)
        self.p("<b>Automation starts disabled.</b> Customer-specific qualification and explicit deployment approval are required before automated processing.",
               M + 13, 742, CW - 26, 10.6, 13.2, NAVY, max_height=29)
        self.end()

    def architecture(self):
        self.start("architecture", "01 / Runtime architecture", "From notice to decision",
                   "A layered classification pipeline. Models and routing are qualified for each deployment.")
        self.box(M + 99, 170, CW - 198, 48, "Normalise & detect input type",
                 "Raw notices retained; a normalised copy is routed.",
                 title_size=11.4, body_size=9, centered=True)
        xs = [M, M + (CW + 12) / 3, M + 2 * (CW + 12) / 3]
        bw = (CW - 24) / 3
        center = W / 2
        for x in xs:
            self.arrow([(center, 218), (center, 232), (x + bw / 2, 232), (x + bw / 2, 246)])
        self.box(xs[0], 246, bw, 65, "SWIFT FIN / ISO 15022", "Prowide Core<br/>Structure + narrative", title_size=10.3, body_size=9.8)
        self.box(xs[1], 246, bw, 65, "Partial / damaged ISO-like", "Lenient recovery scanner<br/>Context + warnings", fill=WARM, accent=AMBER, title_size=10.3, body_size=9.8)
        self.box(xs[2], 246, bw, 65, "Unstructured notice", "Semantic path<br/>No ISO parser required", title_size=10.3, body_size=9.8)
        for x in xs:
            self.arrow([(x + bw / 2, 311), (x + bw / 2, 327), (center, 327), (center, 342)])
        self.box(M, 342, CW, 53, "Normalised event & deterministic facts",
                 "Preserve source and history. Resolve linked terms, controlling dates and event state.", body_size=10)
        self.arrow([(center, 395), (center, 420)])
        self.box(M, 420, CW, 57, "Laya — fast semantic predicates",
                 "Votability, share blocking, power of attorney (POA) and other restrictions; source evidence.", fill=GREEN, body_size=10)
        gate_w = 230
        qx = M + 270
        qw = CW - 270
        self.arrow([(center, 477), (center, 490), (M + gate_w / 2, 490), (M + gate_w / 2, 507)])
        self.box(M, 507, gate_w, 66, "Trust & escalation policy",
                 "Supported calibration, evidence,<br/>context coverage and consistency.", title_size=11.4, body_size=9.6)
        self.box(qx, 507, qw, 66, "Qwen — local semantic fallback",
                 "Resolve uncertain or conflicting facts.<br/>Preserve the earlier Laya result.", title_size=11.2, body_size=9.6)
        self.arrow([(M + gate_w, 542), (qx, 542)], TEAL)
        self.label("ESCALATE", M + gate_w + 3, 524, 36, TEAL, 6.6, TA_CENTER)
        self.arrow([(M + gate_w / 2, 573), (M + gate_w / 2, 597), (center, 597), (center, 615)])
        self.arrow([(qx + qw / 2, 573), (qx + qw / 2, 597), (center, 597), (center, 615)])
        self.label("Retain supported facts", M + 3, 585, 150, MUTED, 8)
        self.label("Reconcile new evidence", qx + 8, 585, qw - 8, MUTED, 8)
        self.box(M, 615, CW, 56, "Reconciliation, decision rules & final confidence",
                 "Structured authority remains visible. Unresolved conflicts and unsupported trust route to review.", body_size=10)
        outw = (CW - 18) / 2
        for x in [M, M + outw + 18]:
            self.arrow([(center, 671), (center, 685), (x + outw / 2, 685), (x + outw / 2, 703)])
        self.box(M, 703, outw, 47, "Qualified decision", "Only within an approved deployment policy.", fill=GREEN, title_size=11, body_size=9)
        self.box(M + outw + 18, 703, outw, 47, "Human review", "Low trust, ambiguity or a failed control.", fill=WARM, accent=AMBER, title_size=11, body_size=9)
        self.p("Outputs: votable / not votable / restricted / deadline passed / review. Source, model, evidence and timing remain traceable. Parser success is not full conformance validation.",
               M, 763, CW, 9.4, 11.4, MUTED, max_height=25)
        self.end()

    def workflow(self):
        self.start("workflow", "02 / Executable customer qualification", "Seven stages. Recorded evidence.",
                   "Each stage produces a durable artefact. A failed gate retains review-only operation.")
        steps = [
            ("Frozen foundation", "Verify pinned weights, runtime, semantic criteria and source hashes. Provision model files separately from the application.", "Foundation manifest<br/>Verified model identity"),
            ("Customer training", "Import and review the corpus. Train Laya or a compatible local LLM using only the approved TRAIN role.", "Dataset + job manifest<br/>Checkpoint + lineage"),
            ("Validation selection", "Compare candidates on VALIDATION: critical recall, complete-output correctness, evidence, coverage and latency.", "Selection receipt<br/>Candidate configuration"),
            ("Model freeze", "Freeze weights, normalisation, prompts, criteria, rules and runtime. A change creates a new candidate identity.", "Immutable model bundle<br/>Reload verification"),
            ("Confidence calibration", "Fit and check calibration on separate groups. Select the operating policy on development data; seal the full release.", "Calibrator + support report<br/>Frozen operating policy"),
            ("Independent qualification", "Persist predictions before opening protected test answers. Check the fixed policy, critical recall and accepted-output precision.", "Qualification receipt<br/>Passed / not met + reasons"),
            ("Monitored release", "Apply independent approval and the deployment permission. Start under observation; retain review, audits and rollback.", "Approved release identity<br/>Operational monitoring plan"),
        ]
        start, row_h = 181, 76
        self.label("STAGE & ACTION", M + 39, 170, 268)
        self.label("RECORDED OUTPUT", M + 334, 170, CW - 334)
        self.line(M + 12, start + 18, M + 12, start + row_h * 6 + 18, LINE, 1.2)
        for i, (title, desc, receipt) in enumerate(steps):
            top = start + i * row_h
            self.c.setFillColor(colors.HexColor(TEAL))
            self.c.circle(M + 12, H - top - 17, 11, fill=1, stroke=0)
            self.p(str(i + 1), M + 2, top + 9, 20, 10.8, 13, WHITE, "SourceSemi", TA_CENTER)
            self.p(title, M + 39, top + 2, 268, 13, 16, NAVY, "SourceSemi")
            self.p(desc, M + 39, top + 24, 268, 10.3, 13.2, MUTED, max_height=43)
            self.p(receipt, M + 334, top + 11, CW - 334, 10, 14, INK, max_height=45)
            if i < 6:
                self.line(M + 39, top + 70, W - M, top + 70)
        self.rect(M, 735, CW, 43, GREEN)
        self.p("<b>Before independent testing:</b> weights, prompt, preprocessing, rules, routing, calibrator and acceptance thresholds are fixed. Test outcomes never select these settings.",
               M + 12, 746, CW - 24, 10.2, 12.8, NAVY, max_height=27)
        self.end()

    def data_gates(self):
        self.start("data", "03 / Data isolation & release gates", "Independent data. Explicit permission.",
                   "Near-duplicates, linked messages and amendment chains remain in the same partition.")
        self.rect(M, 180, CW, 28, NAVY)
        self.label("DATA ROLE", M + 12, 189, 125, WHITE, 8.3)
        self.label("PERMITTED USE", M + 150, 189, CW - 162, WHITE, 8.3)
        roles = [
            ("TRAIN", "Update model weights or adapters. Calibration and frozen-test answers are excluded."),
            ("VALIDATION", "Select candidates, training settings and the operating policy. These results are development evidence."),
            ("CALIBRATION", "Fit correctness estimates and check them on disjoint groups. Never use these labels to update model weights."),
            ("FROZEN TEST", "Independently qualify the sealed release. Predictions are saved before protected answers are accessed."),
        ]
        for i, (role, desc) in enumerate(roles):
            top = 208 + i * 54
            if i % 2 == 0:
                self.rect(M, top, CW, 54, PALE)
            self.p(role, M + 12, top + 15, 125, 11.4, 14, NAVY, "SourceSemi")
            self.p(desc, M + 150, top + 10, CW - 162, 10.5, 13.8, INK, max_height=38)
            self.line(M, top + 54, W - M, top + 54)
        self.p("<b>Labels retain their provenance.</b> AI-authored data qualifies engineering mechanics. Representative, independently expert-reviewed customer labels are required for customer performance and automation qualification.",
               M, 442, CW, 11, 14.5, MUTED, max_height=47)
        self.label("THE DEPLOYMENT GATE CHECKS", M, 513)
        gates = [
            ("Accepted-output precision", "Supported lower bounds for the full requested output, not just average field accuracy."),
            ("Critical-positive recall", "Explicit support and missed-positive counts for voting and material restrictions."),
            ("Measured review volume", "Coverage and review rates meet the agreed operational policy."),
            ("Evidence & input scope", "Supported language, complete context and trustworthy source evidence."),
            ("Installation qualification", "The exact model, runtime and server pass capacity, recovery and load checks."),
            ("Independent promotion", "Authorised approval, a current qualification and the deployment permission."),
        ]
        col = (CW - 26) / 2
        for i, (title, desc) in enumerate(gates):
            x = M + (i % 2) * (col + 26)
            top = 539 + (i // 2) * 62
            self.line(x, top, x + col, top, LINE)
            self.p(title, x, top + 7, col, 11.5, 14, NAVY, "SourceSemi")
            self.p(desc, x, top + 27, col, 9.7, 12.5, MUTED, max_height=28)
        self.rect(M, 745, CW, 33, WARM)
        self.p("<b>Any gate not met → review-only.</b> Targets are customer-agreed business policies, not regulatory guarantees.",
               M + 12, 754, CW - 24, 10, 12.5, INK, max_height=16)
        self.end()

    def confidence(self):
        self.start("confidence", "04 / Confidence & operational review", "Trust is measured, not asserted.",
                   "Confidence is specific to the model, release configuration and declared customer population.")
        definitions = [
            ("01", "Native model score", "A Laya class score or an available token-level model probability. Useful as an input signal; it is not automatically a probability of correctness.", PALE),
            ("02", "Calibrated predicate confidence", "A held-out estimate of whether a particular predicate prediction is correct within its supported population. Unsupported conditions retain unavailable confidence.", GREEN),
            ("03", "Final-decision confidence", "A separately evaluated correctness estimate for the decision. It does not establish that every restriction is correct; all requested operational fields still need support.", PALE),
        ]
        for i, (num, title, desc, fill) in enumerate(definitions):
            top = 181 + i * 91
            self.rect(M, top, CW, 80, fill)
            self.p(num, M + 12, top + 12, 32, 15, 18, TEAL, "SourceSemi")
            self.p(title, M + 55, top + 11, CW - 70, 13, 16, NAVY, "SourceSemi")
            self.p(desc, M + 55, top + 34, CW - 70, 10.5, 13.6, MUTED, max_height=42)
        self.p("A high score does not promise a correct answer.", M, 474, CW,
               17, 21, NAVY, "SourceSemi")
        self.p("Operating thresholds are chosen on development data, then checked independently. The customer sees measured coverage, errors and review volume with sample support and uncertainty bounds.",
               M, 508, CW, 11.3, 15.3, MUTED, max_height=47)
        self.label("ROUTE TO REVIEW WHEN", M, 580)
        reasons = [
            ("Trust is insufficient", "Low or unavailable calibration support; an unknown critical fact."),
            ("Evidence is unresolved", "Conflicting current terms, weak support or an unverified quotation."),
            ("The input is outside scope", "Unsupported language, incomplete context or a materially different input population."),
            ("An execution control fails", "Schema failure, deterministic conflict or an unavailable qualified runtime."),
        ]
        col = (CW - 30) / 2
        for i, (title, desc) in enumerate(reasons):
            x = M + (i % 2) * (col + 30)
            top = 608 + (i // 2) * 65
            self.p(title, x, top, col, 11.7, 15, NAVY, "SourceSemi")
            self.p(desc, x, top + 23, col, 10.3, 13.5, MUTED, max_height=41)
        self.line(M, 754, W - M, 754, LINE)
        self.p("No universal confidence threshold, guaranteed zero-error rate or fixed low review percentage is promised. High-confidence decisions remain subject to audit.",
               M, 765, CW, 9.6, 12, MUTED, max_height=25)
        self.end()

    def feedback(self):
        self.start("feedback", "05 / Monitored release & continuous learning", "Review the uncertain. Audit the accepted.",
                   "A required operating model: targeted review and random audits provide complementary feedback.")
        self.box(M + 69, 180, CW - 138, 51, "Qualified, approved release",
                 "Versioned policy + a current deployment permission.", fill=GREEN, body_size=9.8, centered=True)
        col = (CW - 28) / 2
        left, right = M, M + col + 28
        for x in [left, right]:
            self.arrow([(W / 2, 231), (W / 2, 251), (x + col / 2, 251), (x + col / 2, 272)])
        self.box(left, 272, col, 75, "Low-confidence review queue",
                 "Unsupported trust, unknown facts,<br/>conflicts and failed controls.", fill=WARM, accent=AMBER, title_size=11.3, body_size=10)
        self.box(right, 272, col, 75, "Accepted decisions",
                 "Only within the qualified policy;<br/>the original model result is retained.", fill=GREEN, title_size=11.3, body_size=10)
        self.arrow([(left + col / 2, 347), (left + col / 2, 386)])
        self.arrow([(right + col / 2, 347), (right + col / 2, 386)])
        self.box(left, 386, col, 87, "Blind, revisioned human review",
                 "Record verified facts, exact evidence,<br/>reviewer, time and notes.<br/>Preserve previous labels and predictions.", title_size=11.1, body_size=9.8)
        self.box(right, 386, col, 87, "Random audit of accepted decisions",
                 "Select independently of confidence.<br/>Agree sampling and critical-case coverage;<br/>record inclusion and review outcomes.", title_size=10.7, body_size=9.8)
        self.arrow([(right, 430), (left + col, 430)], TEAL)
        for x in [left, right]:
            self.arrow([(x + col / 2, 473), (x + col / 2, 494), (W / 2, 494), (W / 2, 514)])
        self.box(M, 514, CW, 61, "Feedback ledger & risk monitoring",
                 "Track errors, disagreement, review outcomes and input shifts. A confirmed accepted error can suspend qualification and return processing to review.", body_size=10.2)
        for x in [left, right]:
            self.arrow([(W / 2, 575), (W / 2, 594), (x + col / 2, 594), (x + col / 2, 614)])
        self.box(left, 614, col, 68, "Protect current operations",
                 "Suspend or roll back under the<br/>agreed operational policy.", fill=WARM, accent=AMBER, title_size=11.4, body_size=10)
        self.box(right, 614, col, 68, "Start the next learning round",
                 "New version, new validation,<br/>new calibration and qualification.", title_size=11.4, body_size=10)
        self.p("<b>No silent online learning.</b> Operational corrections become versioned candidates. They do not alter active weights or frozen test labels in place.",
               M, 706, CW, 11, 14.3, NAVY, max_height=32)
        self.p("Automated random-audit sampling is a planned control to implement and verify during acceptance. Existing review, revision history and error-triggered suspension provide the underlying feedback path.",
               M, 754, CW, 9.5, 11.8, MUTED, max_height=26)
        self.end()

    def delivery(self):
        self.start("delivery", "06 / Deployment boundary & customer acceptance", "Your framework. Your data.",
                   "Single-tenant Linux container deployment in the customer environment; exact hardware is qualified separately.")
        col = (CW - 24) / 2
        right = M + col + 24
        self.rect(M, 181, col, 164, PALE, LINE)
        self.rect(right, 181, col, 164, GREEN, LINE)
        self.p("Framework delivery", M + 13, 192, col - 26, 14, 17, NAVY, "SourceSemi")
        self.p("Customer workspace", right + 13, 192, col - 26, 14, 17, NAVY, "SourceSemi")
        self.p("Application and container recipes<br/>Prowide + lenient recovery adapter<br/>Laya / local-LLM interfaces<br/>Training, evaluation and calibration<br/>Review, evidence and audit workflows<br/>Pinned foundation installation manifests",
               M + 13, 224, col - 26, 10.3, 17, MUTED, max_height=108)
        self.p("Raw notices and event history<br/>Reviewed labels and protected splits<br/>Customer checkpoints / adapters<br/>Customer-specific calibrators<br/>Predictions and review revisions<br/>Qualification and operational receipts",
               right + 13, 224, col - 26, 10.3, 17, MUTED, max_height=108)
        self.p("Foundation weights are provisioned separately and verified by revision and file hash. Model inference requires no external generative API; installation downloads are a separate provisioning step.",
               M, 364, CW, 10.6, 14, MUTED, max_height=43)
        self.rect(M, 422, CW, 57, NAVY)
        self.label("EXCLUDED FROM THE SHIPPED PRODUCT", M + 13, 433, CW - 26, "#A9DAD1", 8.1)
        self.p("AI-authored qualification corpora, protected answer keys, test-trained models, test calibrators and research-run artefacts.",
               M + 13, 451, CW - 26, 10.6, 13.3, WHITE, max_height=28)
        self.label("IMPLEMENTATION & ACCEPTANCE STATUS", M, 504)
        statuses = [
            ("Learning, checkpoint and review workflows", "Implemented; controlled-data verification"),
            ("Customer confidence and performance", "Customer-specific qualification required"),
            ("Exact Linux model / hardware profile", "Installation qualification required"),
            ("Random audits of accepted decisions", "Automated sampling is a planned control"),
            ("Automated operational classification", "Disabled until deployment gate + approval"),
        ]
        for i, (title, state) in enumerate(statuses):
            top = 527 + i * 36
            if i % 2 == 0:
                self.rect(M, top, CW, 36, PALE)
            self.p(title, M + 10, top + 10, 245, 10.2, 13, INK, max_height=15)
            self.p(state, M + 269, top + 10, CW - 279, 9.9, 12.8,
                   TEAL if i == 0 else MUTED, max_height=15)
            self.line(M, top + 36, W - M, top + 36)
        self.p("Customer onboarding begins with corpus/profile review, an agreed risk policy and a supported deployment profile.",
               M, 727, CW, 12.4, 16, NAVY, "SourceSemi", max_height=34)
        self.p("This brief describes the architecture and qualification operating model. It is not an accuracy certificate or completed production acceptance. Customer accuracy remains unestablished until representative independent evaluation.",
               M, 769, CW, 9, 11.3, MUTED, max_height=24)
        self.end()

    def finish(self):
        collisions = []
        for i, a in enumerate(self.blocks):
            for b in self.blocks[i+1:]:
                if a['page'] != b['page']:
                    continue
                ox = min(a['x']+a['width'], b['x']+b['width']) - max(a['x'], b['x'])
                oy = min(a['top']+a['height'], b['top']+b['height']) - max(a['top'], b['top'])
                if ox > 1.5 and oy > 1.5:
                    collisions.append({'page':a['page'], 'a':a['text'], 'b':b['text'],
                                       'intersection':[round(ox,2),round(oy,2)]})
        if collisions:
            raise ValueError(json.dumps({'text_collisions':collisions}, indent=2))
        self.c.save()
        receipt = {
            'document': OUTPUT.name, 'document_version': VERSION, 'document_date': DATE,
            'pages': self.page, 'page_size': 'A4 portrait', 'fonts': 'Embedded Source Sans 3 / SIL OFL',
            'vector_diagrams': True, 'text_blocks': len(self.blocks), 'text_overlap_check': 'PASSED',
            'text_bounds_check': 'PASSED', 'sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
            'scope': 'Customer architecture and qualification operating model; no customer performance claims',
            'source': Path(__file__).name,
        }
        (ROOT / 'architecture-document-build.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    brief = Brief()
    brief.cover()
    brief.architecture()
    brief.workflow()
    brief.data_gates()
    brief.confidence()
    brief.feedback()
    brief.delivery()
    brief.finish()
