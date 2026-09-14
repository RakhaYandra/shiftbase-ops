#!/usr/bin/env python3
"""Generate Shiftbase-Tickets.xlsx dari tickets.yaml (pola QA track)."""
import yaml
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import PieChart, Reference

ROOT = Path(__file__).resolve().parent.parent
HDR = Font(bold=True, color="FFFFFF")
HDR_FILL = PatternFill("solid", fgColor="0F172A")
THIN = Border(*(Side(style="thin", color="CBD5E1") for _ in range(4)))


def main():
    tickets = yaml.safe_load(open(ROOT / "tickets.yaml"))
    wb = Workbook()

    ws = wb.active
    ws.title = "Cover"
    ws["A1"] = "Shiftbase Support Tickets"
    ws["A1"].font = Font(bold=True, size=20)
    ws["A3"] = f"{len(tickets)} tiket simulasi + 2 insiden nyata (T-001, T-002)"
    ws.column_dimensions["A"].width = 60

    ws = wb.create_sheet("Tickets")
    cols = ["ID", "Judul", "Severity", "Status", "Opened", "Closed",
            "Timeline", "Diagnosis", "Resolusi", "Pencegahan"]
    ws.append(cols)
    for t in tickets:
        ws.append([t["id"], t["title"], t["severity"], t["status"],
                   t.get("opened", ""), t.get("closed", ""),
                   "\n".join(f"{i+1}. {s}" for i, s in enumerate(t.get("timeline", []))),
                   t.get("diagnosis", ""), t.get("resolution", ""), t.get("prevention", "")])
    for c, w in zip("ABCDEFGHIJ", [8, 40, 10, 10, 12, 12, 45, 35, 40, 40]):
        ws.column_dimensions[c].width = w
    for c in range(1, 11):
        cell = ws.cell(row=1, column=c)
        cell.font = HDR
        cell.fill = HDR_FILL
    for row in ws.iter_rows():
        for cell in row:
            cell.border = THIN
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    ws = wb.create_sheet("SLA")
    ws["A1"] = "SLA compliance (COUNTIF hidup)"
    ws["A1"].font = Font(bold=True, size=14)
    n = len(tickets) + 1
    ws.append([])
    ws.append(["Metrik", "Nilai"])
    ws.append(["Total tiket", len(tickets)])
    ws.append(["Closed", f"=COUNTIF(Tickets!D2:D{n},\"Closed\")"])
    ws.append(["Open", f"=COUNTIF(Tickets!D2:D{n},\"Open\")"])
    ws.append(["High severity", f"=COUNTIF(Tickets!C2:C{n},\"High\")"])
    ws.append(["Closed rate", f"=IF(B4>0,B5/B4,0)"])
    ws["B8"].number_format = "0%"
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 30
    pie = PieChart()
    pie.title = "Status tiket"
    pie.add_data(Reference(ws, min_col=2, min_row=5, max_row=6))
    pie.set_categories(Reference(ws, min_col=1, min_row=5, max_row=6))
    ws.add_chart(pie, "D3")

    out = ROOT / "Shiftbase-Tickets.xlsx"
    wb.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
