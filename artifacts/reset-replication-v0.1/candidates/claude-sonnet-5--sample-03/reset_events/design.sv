module reset_events(
    input  logic       clk,
    input  logic       ext_rst_n,
    input  logic       event_valid,
    output logic [7:0] event_count
);

    // Two-flop synchronizer: asynchronous assert, synchronous deassert.
    // This produces a reset signal that always releases aligned to clk,
    // so no downstream logic (including event_count) ever sees a raw
    // asynchronous deassertion edge.
    logic sync_rst_n_meta;
    logic sync_rst_n;

    always_ff @(posedge clk or negedge ext_rst_n) begin
        if (!ext_rst_n) begin
            sync_rst_n_meta <= 1'b0;
            sync_rst_n      <= 1'b0;
        end else begin
            sync_rst_n_meta <= 1'b1;
            sync_rst_n      <= sync_rst_n_meta;
        end
    end

    // Counter uses the synchronized reset: asserts asynchronously (prompt
    // clear) but only deasserts synchronously to clk.
    always_ff @(posedge clk or negedge sync_rst_n) begin
        if (!sync_rst_n) begin
            event_count <= 8'd0;
        end else if (event_valid) begin
            event_count <= event_count + 8'd1;
        end
    end

endmodule
