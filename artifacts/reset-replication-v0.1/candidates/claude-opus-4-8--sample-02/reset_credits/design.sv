module reset_credits(input logic clk, input logic async_reset_n,
                     input logic consume, input logic replenish,
                     output logic [3:0] credits);

  // Reset synchronizer: assert asynchronously, release synchronously.
  logic rst_n_meta, rst_n_sync;

  always_ff @(posedge clk or negedge async_reset_n) begin
    if (!async_reset_n) begin
      rst_n_meta <= 1'b0;
      rst_n_sync <= 1'b0;
    end else begin
      rst_n_meta <= 1'b1;
      rst_n_sync <= rst_n_meta;
    end
  end

  // Ordinary state uses the synchronized reset (async assert, sync release).
  always_ff @(posedge clk or negedge rst_n_sync) begin
    if (!rst_n_sync) begin
      credits <= 4'd0;
    end else begin
      if (replenish && !consume) begin
        if (credits != 4'hF)
          credits <= credits + 4'd1;
      end else if (consume && !replenish) begin
        if (credits != 4'd0)
          credits <= credits - 4'd1;
      end
      // both asserted or neither: hold
    end
  end

endmodule
