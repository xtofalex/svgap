module reset_watchdog (
    input  logic clk,
    input  logic system_rst_n,
    input  logic kick,
    output logic timeout
);

    logic [1:0] reset_sync;
    logic [1:0] idle_count;

    always_ff @(posedge clk or negedge system_rst_n) begin
        if (!system_rst_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    always_ff @(posedge clk or negedge reset_sync[1]) begin
        if (!reset_sync[1]) begin
            idle_count <= 2'd0;
            timeout    <= 1'b0;
        end else begin
            timeout <= 1'b0;

            if (kick) begin
                idle_count <= 2'd0;
            end else if (idle_count == 2'd3) begin
                idle_count <= 2'd0;
                timeout    <= 1'b1;
            end else begin
                idle_count <= idle_count + 2'd1;
            end
        end
    end

endmodule
