# Repair starter

Repair the supplied unsafe `reset_release` module so reset assertion remains
asynchronous while reset deassertion reaching operational `count` state is
synchronized to `clk`. Preserve the module name, ports, intended counter
behavior, and synthesizability. Do not modify the testbench or add tool-specific
waiver attributes. The safe reference is not supplied.

Return only the complete SystemVerilog module, fenced or bare.
