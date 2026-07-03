module reset_watchdog(
    input  logic clk,
    input  logic system_rst_n,
    input  logic kick,
    output logic timeout
);

    //--------------------------------------------------------------
    // Reset synchronizer: asynchronous assertion, synchronous release
    //--------------------------------------------------------------
    logic sync_rst_n_ff1;
    logic sync_rst_n;

    always_ff @(posedge clk or negedge system_rst_n) begin
        if (!system_rst_n) begin
            sync_rst_n_ff1 <= 1'b0;
            sync_rst_n     <= 1'b0;
        end else begin
            sync_rst_n_ff1 <= 1'b1;
            sync_rst_n     <= sync_rst_n_ff1;
        end
    end

    //--------------------------------------------------------------
    // Watchdog counter / timeout pulse logic
    // Uses the synchronized reset (async assert, sync release) so
    // that operational state only resumes from a clk-synchronized
    // reset release, while still reacting instantly to reset assertion.
    //--------------------------------------------------------------
    logic [1:0] cnt;
    logic       timeout_r;

    always_ff @(posedge clk or negedge sync_rst_n) begin
        if (!sync_rst_n) begin
            cnt       <= 2'd0;
            timeout_r <= 1'b0;
        end else begin
            if (kick) begin
                cnt       <= 2'd0;
                timeout_r <= 1'b0;
            end else if (cnt == 2'd3) begin
                cnt       <= 2'd0;
                timeout_r <= 1'b1;
            end else begin
                cnt       <= cnt + 2'd1;
                timeout_r <= 1'b0;
            end
        end
    end

    assign timeout = timeout_r;

endmodule
