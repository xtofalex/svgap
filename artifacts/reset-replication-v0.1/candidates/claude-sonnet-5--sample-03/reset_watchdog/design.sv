module reset_watchdog(
    input  logic clk,
    input  logic system_rst_n,
    input  logic kick,
    output logic timeout
);

    // ---------------------------------------------------------------
    // Reset synchronizer: asynchronous assertion, synchronized release
    // ---------------------------------------------------------------
    logic [1:0] rst_sync;
    logic       sync_rst_n;

    always_ff @(posedge clk or negedge system_rst_n) begin
        if (!system_rst_n)
            rst_sync <= 2'b00;
        else
            rst_sync <= {rst_sync[0], 1'b1};
    end

    assign sync_rst_n = rst_sync[1];

    // ---------------------------------------------------------------
    // Watchdog counter/timeout logic
    // Async assert on system_rst_n, but operational state only resumes
    // once sync_rst_n (synchronized release) is high.
    // ---------------------------------------------------------------
    logic [1:0] count;

    always_ff @(posedge clk or negedge system_rst_n) begin
        if (!system_rst_n) begin
            count   <= 2'd0;
            timeout <= 1'b0;
        end else if (!sync_rst_n) begin
            count   <= 2'd0;
            timeout <= 1'b0;
        end else begin
            if (kick) begin
                count   <= 2'd0;
                timeout <= 1'b0;
            end else if (count == 2'd3) begin
                count   <= 2'd0;
                timeout <= 1'b1;
            end else begin
                count   <= count + 2'd1;
                timeout <= 1'b0;
            end
        end
    end

endmodule
