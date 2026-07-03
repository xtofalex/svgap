module reset_credits (
    input  logic       clk,
    input  logic       async_reset_n,
    input  logic       consume,
    input  logic       replenish,
    output logic [3:0] credits
);

    (* ASYNC_REG = "TRUE" *) logic [1:0] reset_sync;
    logic reset_n;

    always_ff @(posedge clk or negedge async_reset_n) begin
        if (!async_reset_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    assign reset_n = reset_sync[1];

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n)
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
