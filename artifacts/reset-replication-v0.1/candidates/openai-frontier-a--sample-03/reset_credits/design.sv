module reset_credits (
    input  logic       clk,
    input  logic       async_reset_n,
    input  logic       consume,
    input  logic       replenish,
    output logic [3:0] credits
);

    logic [1:0] reset_sync;

    always_ff @(posedge clk or negedge async_reset_n) begin
        if (!async_reset_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    always_ff @(posedge clk or negedge reset_sync[1]) begin
        if (!reset_sync[1])
            credits <= 4'b0000;
        else begin
            case ({replenish, consume})
                2'b10: credits <= credits + 4'b0001;
                2'b01: if (credits != 4'b0000)
                           credits <= credits - 4'b0001;
                default: credits <= credits;
            endcase
        end
    end

endmodule
