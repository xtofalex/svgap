module reset_events(input logic clk, input logic ext_rst_n, input logic event_valid,
                    output logic [7:0] event_count);

  // Reset synchronizer: asynchronous assertion, synchronous deassertion.
  // ext_rst_n falling clears the flops immediately (async assert).
  // On release, the '1' is clocked through two stages so the internal
  // reset (rst_sync_n) deasserts aligned to clk. No counter bit ever
  // observes the raw asynchronous release of ext_rst_n.
  logic rst_meta_n;
  logic rst_sync_n;

  always_ff @(posedge clk or negedge ext_rst_n) begin
    if (!ext_rst_n) begin
      rst_meta_n <= 1'b0;
      rst_sync_n <= 1'b0;
    end else begin
      rst_meta_n <= 1'b1;
      rst_sync_n <= rst_meta_n;
    end
  end

  // Counter uses the synchronized reset. Asynchronous assert clears promptly,
  // release is clock-aligned via the synchronizer above.
  always_ff @(posedge clk or negedge rst_sync_n) begin
    if (!rst_sync_n)
      event_count <= 8'd0;
    else if (event_valid)
      event_count <= event_count + 8'd1;
  end

endmodule
