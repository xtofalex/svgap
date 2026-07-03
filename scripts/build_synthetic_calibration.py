#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "review_packets/synthetic-calibration-v0.1"
MAPPING = ROOT / "reports/generated/synthetic-calibration-v0.1-mapping.json"


CASES = [
    ("yes", "Direct raw reset on counter", """module c(input logic clk, input logic rst_n, output logic [3:0] count);
always_ff @(posedge clk or negedge rst_n) begin
  if (!rst_n) count <= 0; else count <= count + 1'b1;
end
endmodule"""),
    ("yes", "Synchronizer plus raw-reset operational state", """module c(input logic clk, input logic rst_n, input logic en, output logic q);
logic m, s;
always_ff @(posedge clk or negedge rst_n)
  if (!rst_n) begin m <= 0; s <= 0; end else begin m <= 1; s <= m; end
always_ff @(posedge clk or negedge rst_n)
  if (!rst_n) q <= 0; else if (!s) q <= 0; else if (en) q <= ~q;
endmodule"""),
    ("yes", "Combined synchronizer and data state", """module c(input logic clk, input logic arst_n, output logic [7:0] data);
logic [1:0] rs;
always_ff @(posedge clk or negedge arst_n) begin
  if (!arst_n) begin rs <= 0; data <= 0; end
  else begin rs <= {rs[0],1'b1}; if (!rs[1]) data <= 0; else data <= data + 1'b1; end
end
endmodule"""),
    ("yes", "Active-high direct reset", """module c(input logic clk, input logic arst, output logic state);
always_ff @(posedge clk or posedge arst)
  if (arst) state <= 0; else state <= ~state;
endmodule"""),
    ("yes", "Raw reset on FSM state", """module c(input logic clk, input logic reset_n, input logic go, output logic busy);
logic sync1, sync2; logic [1:0] state;
always_ff @(posedge clk or negedge reset_n)
  if (!reset_n) begin sync1<=0; sync2<=0; end else begin sync1<=1; sync2<=sync1; end
always_ff @(posedge clk or negedge reset_n)
  if (!reset_n) state<=0; else if (!sync2) state<=0; else state<=go ? 1 : 0;
assign busy = |state;
endmodule"""),
    ("yes", "Raw-reset alias on operational state", """module c(input logic clk, input logic por_n, output logic q);
wire raw_alias_n = por_n;
always_ff @(posedge clk or negedge raw_alias_n)
  if (!raw_alias_n) q <= 0; else q <= 1;
endmodule"""),
    ("no", "Derived local reset using synchronized release", """module c(input logic clk, input logic rst_n, output logic [3:0] count);
logic m, s; wire local_rst_n = rst_n & s;
always_ff @(posedge clk or negedge rst_n)
  if (!rst_n) begin m<=0; s<=0; end else begin m<=1; s<=m; end
always_ff @(posedge clk or negedge local_rst_n)
  if (!local_rst_n) count<=0; else count<=count+1'b1;
endmodule"""),
    ("no", "Synchronizer only uses raw reset", """module c(input logic clk, input logic arst_n, output logic q);
logic [1:0] rs;
always_ff @(posedge clk or negedge arst_n)
  if (!arst_n) rs<=0; else rs<={rs[0],1'b1};
always_ff @(posedge clk)
  if (!rs[1]) q<=0; else q<=1;
endmodule"""),
    ("no", "Separate derived asynchronous local reset", """module c(input logic clk, input logic ext_n, input logic d, output logic q);
logic a,b; wire domain_n = ext_n & b;
always_ff @(posedge clk or negedge ext_n)
  if(!ext_n) begin a<=0;b<=0;end else begin a<=1;b<=a;end
always_ff @(posedge clk or negedge domain_n)
  if(!domain_n) q<=0; else q<=d;
endmodule"""),
    ("no", "Active-high derived local reset", """module c(input logic clk, input logic arst, output logic q);
logic m,s; wire local_arst = arst | s;
always_ff @(posedge clk or posedge arst)
  if(arst) begin m<=1;s<=1;end else begin m<=0;s<=m;end
always_ff @(posedge clk or posedge local_arst)
  if(local_arst) q<=0; else q<=~q;
endmodule"""),
    ("no", "Operational state uses synchronized reset edge", """module c(input logic clk, input logic reset_n, output logic [1:0] state);
logic m, sync_n;
always_ff @(posedge clk or negedge reset_n)
  if(!reset_n) begin m<=0;sync_n<=0;end else begin m<=1;sync_n<=m;end
always_ff @(posedge clk or negedge sync_n)
  if(!sync_n) state<=0; else state<=state+1'b1;
endmodule"""),
    ("no", "Two independent operational registers behind local reset", """module c(input logic clk, input logic rst_n, output logic a, b);
logic r1,r2; wire local_n=rst_n&r2;
always_ff @(posedge clk or negedge rst_n)
  if(!rst_n) begin r1<=0;r2<=0;end else begin r1<=1;r2<=r1;end
always_ff @(posedge clk or negedge local_n)
  if(!local_n) begin a<=0;b<=0;end else begin a<=~a;b<=a;end
endmodule"""),
]


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite {OUTPUT}")
    cases_dir = OUTPUT / "cases"
    cases_dir.mkdir(parents=True)
    mapping = []
    manifest = []
    for label, description, rtl in CASES:
        case_id = "CAL-" + secrets.token_hex(8).upper()
        prompt = (
            "The external reset must assert asynchronously and release synchronously. "
            "Determine whether ordinary operational state directly uses the external raw "
            "asynchronous reset; reset synchronizer stages are exempt."
        )
        text = f"# {case_id}\n\n## Task specification\n\n{prompt}\n\n## Candidate RTL\n\n```systemverilog\n{rtl}\n```\n"
        (cases_dir / f"{case_id}.md").write_text(text, encoding="utf-8")
        digest = hashlib.sha256(text.encode()).hexdigest()
        manifest.append({"case_id": case_id, "sha256": digest})
        mapping.append(
            {"case_id": case_id, "expected": label, "description": description}
        )
    (OUTPUT / "manifest.json").write_text(
        json.dumps({"schema_version": "1.0", "case_count": len(CASES), "cases": manifest}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    MAPPING.parent.mkdir(parents=True, exist_ok=True)
    MAPPING.write_text(
        json.dumps({"schema_version": "1.0", "cases": mapping}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"cases      {len(CASES)}")
    print(f"packet     {OUTPUT}")
    print(f"mapping    {MAPPING}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
