module reset_events (
    input  logic       clk,
    input  logic       ext_rst_n,
    input  logic       event_valid,
    output logic [7:0] event_count
);

    // Two-stage reset synchronizer:
    // - Assertion of ext_rst_n propagates asynchronously (fast, glitch-free clear)
    // - Deassertion is re-timed through two flip-flops so rst_n_sync only
    //   ever changes value on a clock edge (no raw async release reaches logic)
    logic rst_n_meta;
    logic rst_n_sync;

    always_ff @(posedge clk or negedge ext_rst_n) begin
        if (!ext_rst_n) begin
            rst_n_meta <= 1'b0;
            rst_n_sync <= 1'b0;
        end else begin
            rst_n_meta <= 1'b1;
            rst_n_sync <= rst_n_meta;
        end
    end

    // Event counter uses the synchronized reset:
    // asynchronous assert (clears promptly), synchronous deassert
    // (rst_n_sync only transitions on clk edges).
    always_ff @(posedge clk or negedge rst_n_sync) begin
        if (!rst_n_sync) begin
            event_count <= 8'd0;
        end else if (event_valid) begin
            event_count <= event_count + 8'd1;
        end
    end

endmodule
