module reset_credits(input logic clk, input logic async_reset_n,
                     input logic consume, input logic replenish,
                     output logic [3:0] credits);

    // -----------------------------------------------------------------
    // Reset synchronizer: asynchronous assertion, synchronous release.
    // async_reset_n can assert at any time (async), but its de-assertion
    // (release) is re-timed to clk so that the rest of the design sees
    // a reset that only ever de-asserts synchronously to clk, avoiding
    // reset-recovery/removal violations.
    // -----------------------------------------------------------------
    logic sync_reset_n_meta;
    logic sync_reset_n;

    always_ff @(posedge clk or negedge async_reset_n) begin
        if (!async_reset_n) begin
            sync_reset_n_meta <= 1'b0;
            sync_reset_n      <= 1'b0;
        end else begin
            sync_reset_n_meta <= 1'b1;
            sync_reset_n      <= sync_reset_n_meta;
        end
    end

    // -----------------------------------------------------------------
    // Credit counter: uses the synchronized reset signal. It still
    // asserts asynchronously (matching the original async_reset_n
    // assertion), but its de-assertion is guaranteed synchronous to
    // clk thanks to the synchronizer above.
    // -----------------------------------------------------------------
    always_ff @(posedge clk or negedge sync_reset_n) begin
        if (!sync_reset_n) begin
            credits <= 4'd0;
        end else begin
            case ({replenish, consume})
                2'b10:   credits <= (credits == 4'hF) ? credits : credits + 4'd1; // replenish only
                2'b01:   credits <= (credits == 4'd0) ? credits : credits - 4'd1; // consume only
                default: credits <= credits; // both or neither: hold
            endcase
        end
    end

endmodule
