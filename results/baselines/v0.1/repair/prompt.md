# Repair prompt

The model receives the unsafe module in `before/design.sv` and is instructed to
make reset assertion asynchronous and reset deassertion reaching operational
`count` state synchronized to `clk`. It must preserve the module name, ports,
behavior, and synthesizability; it may not modify the testbench or add
tool-specific waiver attributes. The safe reference is not supplied.

Model tools are disabled. The complete normalized SystemVerilog response is
stored as `after/design.sv`; raw provider transcripts are excluded.
