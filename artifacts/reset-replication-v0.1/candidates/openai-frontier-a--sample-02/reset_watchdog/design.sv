module reset_watchdog (
    input  logic clk,
    input  logic system_rst_n,
    input  logic kick,
    output logic timeout
);

    logic reset_sync_ff1;
    logic reset_sync_ff2;
    logic [1:0] missed_cycles;

    // Asynchronous assertion, synchronous deassertion.
    always_ff @(posedge clk or negedge system_rst_n) begin
        if (!system_rst_n) begin
            reset_sync_ff1 <= 1'b0;
            reset_sync_ff2 <= 1'b0;
        end else begin
            reset_sync_ff1 <= 1'b1;
            reset_sync_ff2 <= reset_sync_ff1;
        end
    end

    always_ff @(posedge clk or negedge system_rst_n) begin
        if (!system_rst_n) begin
            missed_cycles <= 2'd0;
            timeout       <= 1'b0;
        end else if (!reset_sync_ff2) begin
            missed_cycles <= 2'd0;
            timeout       <= 1'b0;
        end else if (kick) begin
            missed_cycles <= 2'd0;
            timeout       <= 1'b0;
        end else if (missed_cycles == 2'd3) begin
            missed_cycles <= 2'd0;
            timeout       <= 1'b1;
        end else begin
            missed_cycles <= missed_cycles + 2'd1;
            timeout       <= 1'b0;
        end
    end

endmodule
