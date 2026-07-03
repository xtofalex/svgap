module reset_watchdog (
    input  logic clk,
    input  logic system_rst_n,
    input  logic kick,
    output logic timeout
);

    logic [1:0] reset_sync;
    logic [1:0] no_kick_count;

    always_ff @(posedge clk or negedge system_rst_n) begin
        if (!system_rst_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    always_ff @(posedge clk or negedge reset_sync[1]) begin
        if (!reset_sync[1]) begin
            no_kick_count <= 2'd0;
            timeout       <= 1'b0;
        end else if (kick) begin
            no_kick_count <= 2'd0;
            timeout       <= 1'b0;
        end else if (no_kick_count == 2'd3) begin
            no_kick_count <= 2'd0;
            timeout       <= 1'b1;
        end else begin
            no_kick_count <= no_kick_count + 2'd1;
            timeout       <= 1'b0;
        end
    end

endmodule
