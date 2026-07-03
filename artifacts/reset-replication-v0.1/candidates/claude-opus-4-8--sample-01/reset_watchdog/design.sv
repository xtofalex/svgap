module reset_watchdog(input logic clk, input logic system_rst_n, input logic kick,
                      output logic timeout);

  // ------------------------------------------------------------------
  // Reset synchronizer:
  //   - assertion is asynchronous (flops cleared immediately on
  //     system_rst_n low)
  //   - de-assertion (release) is synchronized to clk through two flops
  // ------------------------------------------------------------------
  logic rst_sync_ff1, rst_sync_ff2;
  logic rst_n_sync;

  always_ff @(posedge clk or negedge system_rst_n) begin
    if (!system_rst_n) begin
      rst_sync_ff1 <= 1'b0;
      rst_sync_ff2 <= 1'b0;
    end else begin
      rst_sync_ff1 <= 1'b1;
      rst_sync_ff2 <= rst_sync_ff1;
    end
  end

  assign rst_n_sync = rst_sync_ff2;

  // ------------------------------------------------------------------
  // Watchdog counter:
  //   - counts clock cycles since the last kick
  //   - timeout pulses for one cycle after four consecutive
  //     cycles without a kick
  //   - a kick restarts the interval
  // Driven by the synchronized reset so operational state only
  // resumes from a synchronized release, while still asserting
  // asynchronously (rst_n_sync drops asynchronously on system_rst_n).
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
