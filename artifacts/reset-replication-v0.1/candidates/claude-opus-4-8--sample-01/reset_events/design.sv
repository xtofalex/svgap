module reset_events(input  logic       clk,
                    input  logic       ext_rst_n,
                    input  logic       event_valid,
                    output logic [7:0] event_count);

  // -----------------------------------------------------------------------
  // Reset synchronizer:
  //   - Asynchronous assertion  : when ext_rst_n falls, rst_n_sync clears
  //                                immediately (async reset input on FFs).
  //   - Synchronous release      : deassertion propagates through two flops
  //                                so the counter never sees a raw async edge.
  // -----------------------------------------------------------------------
  logic rst_meta, rst_n_sync;

  always_ff @(posedge clk or negedge ext_rst_n) begin
    if (!ext_rst_n) begin
      rst_meta   <= 1'b0;
      rst_n_sync <= 1'b0;
    end
    else begin
      rst_meta   <= 1'b1;      // shift a '1' in on each clock after release
      rst_n_sync <= rst_meta;  // clock-aligned deassertion to the design
    end
  end

  // -----------------------------------------------------------------------
  // Event counter.  Uses the synchronized reset so every counter bit's
  // reset release is aligned to the clock edge.  Assertion is still async
  // (through rst_n_sync) so reset clears promptly.
  // -----------------------------------------------------------------------
  always_ff @(posedge clk or negedge rst_n_sync) begin
    if (!rst_n_sync)
      event_count <= 8'd0;
    else if (event_valid)
      event_count <= event_count + 8'd1;
  end

endmodule
