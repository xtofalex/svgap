module reset_watchdog(input logic clk, input logic system_rst_n, input logic kick,
                      output logic timeout);

  // ------------------------------------------------------------------
  // Reset synchronizer: asynchronous assert, synchronous (clk) release.
  // system_rst_n asserts the local reset immediately, but the operational
  // logic only leaves reset on a clk edge after system_rst_n is high.
  // ------------------------------------------------------------------
  logic rst_meta, rst_n_sync;
  always_ff @(posedge clk or negedge system_rst_n) begin
    if (!system_rst_n) begin
      rst_meta   <= 1'b0;
      rst_n_sync <= 1'b0;
    end else begin
      rst_meta   <= 1'b1;
      rst_n_sync <= rst_meta;
    end
  end

  // ------------------------------------------------------------------
  // Watchdog counter. Counts clocks since the last kick; pulses timeout
  // after four consecutive cycles without a kick. A kick restarts it.
  // Operational state uses the synchronized reset release.
  // ------------------------------------------------------------------
  logic [1:0] count;
  always_ff @(posedge clk or negedge rst_n_sync) begin
    if (!rst_n_sync) begin
      count   <= 2'd0;
      timeout <= 1'b0;
    end else if (kick) begin
      count   <= 2'd0;
      timeout <= 1'b0;
    end else if (count == 2'd3) begin
      count   <= 2'd0;
      timeout <= 1'b1;
    end else begin
      count   <= count + 2'd1;
      timeout <= 1'b0;
    end
  end

endmodule
