module reset_credits(
    input  logic       clk,
    input  logic       async_reset_n,
    input  logic       consume,
    input  logic       replenish,
    output logic [3:0] credits
);

    // -------------------------------------------------------------
    // Reset synchronizer: asserts asynchronously, releases synchronously
    // -------------------------------------------------------------
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

    // -------------------------------------------------------------
    // Credit counter: async assert, sync release via sync_reset_n
    // -------------------------------------------------------------
    always_ff @(posedge clk or negedge async_reset_n) begin
        if (!async_reset_n) begin
            credits <= 4'h0;
        end else if (!sync_reset_n) begin
            credits <= 4'h0;
        end else begin
            case ({replenish, consume})
                2'b10:   if (credits != 4'hF) credits <= credits + 4'h1; // replenish only
                2'b01:   if (credits != 4'h0) credits <= credits - 4'h1; // consume only
                default: credits <= credits;                             // hold (both or neither)
            endcase
        end
    end

endmodule
