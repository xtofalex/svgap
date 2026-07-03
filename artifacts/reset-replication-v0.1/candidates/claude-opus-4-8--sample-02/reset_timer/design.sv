module reset_timer
  (
   input  logic       clk,
   input  logic       por_n,        // asynchronous active-low power-on reset
   input  logic       load,         // synchronous load enable
   input  logic [3:0] load_value,   // value captured on load
   output logic       expired       // asserted when timer == 0
   );

  //--------------------------------------------------------------------------
  // Reset synchronizer:
  //   Asynchronous assert  (por_n low  -> rst_n low immediately)
  //   Synchronous  release (por_n high -> rst_n rises after 2 clk edges)
  //--------------------------------------------------------------------------
  logic rst_meta_q;   // first stage (metastability catcher)
  logic rst_sync_q;   // second stage (clean synchronized reset)

  always_ff @(posedge clk or negedge por_n) begin
    if (!por_n) begin
      rst_meta_q <= 1'b0;
      rst_sync_q <= 1'b0;
    end
    else begin
      rst_meta_q <= 1'b1;
      rst_sync_q <= rst_meta_q;
    end
  end

  // Local active-low reset used by all functional state.  Assertion is
  // asynchronous (por_n path); release is synchronous to clk.
  logic rst_n;
  assign rst_n = rst_sync_q;

  //--------------------------------------------------------------------------
  // Timer down-counter
  //--------------------------------------------------------------------------
  logic [3:0] count_q;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      count_q <= 4'd0;
      expired <= 1'b1;                 // reset state: counter at zero
    end
    else if (load) begin
      count_q <= load_value;           // capture new count
      expired <= (load_value == 4'd0); // immediate expire if loaded with 0
    end
    else if (count_q != 4'd0) begin
      count_q <= count_q - 4'd1;       // count down
      expired <= (count_q == 4'd1);    // expires as it transitions to 0
    end
    else begin
      count_q <= 4'd0;                 // hold at zero
      expired <= 1'b1;                 // remain expired until reloaded
    end
  end

endmodule
