module reset_watchdog(
    input  logic clk,
    input  logic system_rst_n,
    input  logic kick,
    output logic timeout
);

    // ------------------------------------------------------------------
    // Reset synchronizer: assertion is asynchronous (mirrors system_rst_n
    // immediately), but release is synchronized to clk via a 2-FF chain.
    // ------------------------------------------------------------------
    logic rst_meta;
    logic sync_rst_n;

    always_ff @(posedge clk or negedge system_rst_n) begin
        if (!system_rst_n) begin
            rst_meta   <= 1'b0;
            sync_rst_n <= 1'b0;
        end else begin
            rst_meta   <= 1'b1;
            sync_rst_n <= rst_meta;
        end
    end

    // ------------------------------------------------------------------
    // Watchdog counter / timeout logic.
    // Uses sync_rst_n as an asynchronous reset so that assertion of
    // system_rst_n immediately propagates (async assert), while the
    // logic only resumes operation once sync_rst_n has been released
    // synchronously to clk.
    // ------------------------------------------------------------------
    logic [2:0] count;

    always_ff @(posedge clk or negedge sync_rst_n) begin
        if (!sync_rst_n) begin
            count   <= 3'd0;
            timeout <= 1'b0;
        end else if (kick) begin
            count   <= 3'd0;
            timeout <= 1'b0;
        end else if (count == 3'd4) begin
            // Interval already timed out; hold until next kick.
            timeout <= 1'b0;
        end else begin
            count   <= count + 3'd1;
            timeout <= (count + 3'd1 == 3'd4);
        end
    end

endmodule
