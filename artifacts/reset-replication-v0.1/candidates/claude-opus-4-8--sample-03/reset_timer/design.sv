module reset_timer
  (
    input  logic       clk,
    input  logic       por_n,        // asynchronous, active-low power-on reset
    input  logic       load,         // synchronous load enable
    input  logic [3:0] load_value,   // value captured on load
    output logic       expired       // asserted when counter is at zero
  );

  //--------------------------------------------------------------------------
  // Reset synchronizer: asynchronous assert, synchronous deassert.
  // Two flip-flops shift a constant '1' toward the output; the async reset
  // clears them immediately, and they re-arm synchronously to clk.
  //--------------------------------------------------------------------------
  logic rst_meta_n;   // first stage (potentially metastable)
  logic rst_n_sync;   // synchronized, functional reset (active-low)

  always_ff @(posedge clk or negedge por_n) begin
    if (!por_n) begin
      rst_meta_n <= 1'b0;
      rst_n_sync <= 1'b0;
    end
    else begin
      rst_meta_n <= 1'b1;
      rst_n_sync <= rst_meta_n;
    end
  end

  //--------------------------------------------------------------------------
  // Functional counter. Reset by the synchronized reset only.
  //--------------------------------------------------------------------------
  logic [3:0] count_q;

  always_ff @(posedge clk or negedge rst_n_sync) begin
    if (!rst_n_sync) begin
      count_q <= 4'd0;
    end
    else if (load) begin
      count_q <= load_value;
    end
    else if (count_q != 4'd0) begin
      count_q <= count_q - 4'd1;   // saturating decrement (no wrap)
    end
  end

  //--------------------------------------------------------------------------
  // Output: asserted while the timer has reached zero.
  //--------------------------------------------------------------------------
  assign expired = (count_q == 4'd0);

endmodule
