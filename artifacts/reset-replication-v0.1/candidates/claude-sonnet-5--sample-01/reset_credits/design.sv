module reset_credits(input logic clk, input logic async_reset_n,
                     input logic consume, input logic replenish,
                     output logic [3:0] credits);

    // Two-flop synchronizer for reset release.
    // Reset assertion is asynchronous (immediate), but release is
    // re-synchronized to clk before it is allowed to affect the
    // main state machine, avoiding recovery/removal violations.
    logic rst_sync_ff1, rst_sync_ff2;

    always_ff @(posedge clk or negedge async_reset_n) begin
        if (!async_reset_n) begin
            rst_sync_ff1 <= 1'b0;
            rst_sync_ff2 <= 1'b0;
        end else begin
            rst_sync_ff1 <= 1'b1;
            rst_sync_ff2 <= rst_sync_ff1;
        end
    end

    // Synchronized, active-low reset for the credit counter
    wire sync_reset_n = rst_sync_ff2;

    always_ff @(posedge clk or negedge async_reset_n) begin
        if (!async_reset_n) begin
            // Asynchronous assertion path
            credits <= 4'd0;
        end else if (!sync_reset_n) begin
            // Held in reset until release has been synchronized
            credits <= 4'd0;
        end else begin
            unique case ({replenish, consume})
                2'b10:   credits <= credits + 4'd1;                     // replenish only
                2'b01:   credits <= (credits != 4'd0) ? credits - 4'd1 : credits; // consume only
                default: credits <= credits;                             // both or neither: hold
            endcase
        end
    end

endmodule
