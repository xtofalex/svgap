module reset_watchdog(input logic clk, input logic system_rst_n, input logic kick,
                      output logic timeout);

  // ---------------------------------------------------------------
  // Reset synchronizer: asynchronous assertion, synchronous release.
  // rst_n_sync drops immediately (async) with system_rst_n, but only
  // returns high after being clocked through two flops.
  // ---------------------------------------------------------------
  logic rst_sync_ff1, rst_n_sync;

  always_ff @(posedge clk or negedge system_rst_n) begin
    if (!system_rst_n) begin
      rst_sync_ff1 <= 1'b0;
      rst_n_sync   <= 1'b0;
    end else begin
      rst_sync_ff1 <= 1'b1;
      rst_n_sync   <= rst_sync_ff1;
    end
  end

  // ---------------------------------------------------------------
  // Watchdog counter. Uses the synchronized reset so that assertion
  // is asynchronous while operational state only resumes on a
  // clk-synchronized reset release.
  // ---------------------------------------------------------------
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
      timeout <= 1'b1;   // pulse after 4 consecutive cycles w/o kick
    end else begin
      count   <= count + 2'd1;
      timeout <= 1'b0;
    end
  end

endmodule
