module reset_credits(input logic clk, input logic async_reset_n,
                     input logic consume, input logic replenish,
                     output logic [3:0] credits);

    // -----------------------------------------------------------------
    // Reset synchronizer: assert asynchronously (follows async_reset_n
    // immediately), release synchronously (staged through two flops so
    // the deassertion edge is aligned to clk before state exits reset).
    // -----------------------------------------------------------------
    logic rst_meta;
    logic rst_sync_n;

    always_ff @(posedge clk or negedge async_reset_n) begin
        if (!async_reset_n) begin
            rst_meta   <= 1'b0;
            rst_sync_n <= 1'b0;
        end else begin
            rst_meta   <= 1'b1;
            rst_sync_n <= rst_meta;
        end
    end

    // -----------------------------------------------------------------
    // Credit counter. Uses the synchronized reset: asynchronous at
    // assertion, synchronous at release.
    // -----------------------------------------------------------------
    always_ff @(posedge clk or negedge rst_sync_n) begin
        if (!rst_sync_n) begin
            credits <= 4'd0;
        end else begin
            unique case ({replenish, consume})
                2'b11: credits <= credits;                                   // hold
                2'b10: credits <= (credits == 4'hF) ? credits : credits + 4'd1; // increment
                2'b01: credits <= (credits == 4'h0) ? credits : credits - 4'd1; // decrement
                default: credits <= credits;                                 // idle
            endcase
        end
    end

endmodule
