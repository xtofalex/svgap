module reset_events (
    input  logic       clk,
    input  logic       ext_rst_n,
    input  logic       event_valid,
    output logic [7:0] event_count
);

    // Two-stage synchronizer providing an asynchronous-assert,
    // synchronous-deassert reset signal (rst_sync_n).
    // This ensures the reset release is aligned to clk edges
    // throughout the rest of the design.
    logic rst_meta_n;
    logic rst_sync_n;

    always_ff @(posedge clk or negedge ext_rst_n) begin
        if (!ext_rst_n) begin
            rst_meta_n <= 1'b0;
            rst_sync_n <= 1'b0;
        end else begin
            rst_meta_n <= 1'b1;
            rst_sync_n <= rst_meta_n;
        end
    end

    // Event counter using the synchronized reset.
    // Assertion is asynchronous (prompt clear), but deassertion
    // is already clock-aligned by the synchronizer above, so this
    // flop never sees a raw asynchronous deassertion.
    always_ff @(posedge clk or negedge rst_sync_n) begin
        if (!rst_sync_n) begin
            event_count <= 8'd0;
        end else if (event_valid) begin
            event_count <= event_count + 8'd1;
        end
    end

endmodule
