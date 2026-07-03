module reset_counter(input logic clk, input logic arst_n, input logic enable,
                     output logic [7:0] count);

    // Reset synchronizer: asserts asynchronously, deasserts synchronously
    logic sync_ff1, sync_ff2;
    logic rst_n_sync;

    always_ff @(posedge clk or negedge arst_n) begin
        if (!arst_n) begin
            sync_ff1 <= 1'b0;
            sync_ff2 <= 1'b0;
        end else begin
            sync_ff1 <= 1'b1;
            sync_ff2 <= sync_ff1;
        end
    end

    assign rst_n_sync = sync_ff2;

    // Counter uses the same async-assert/sync-deassert reset for its state
    always_ff @(posedge clk or negedge rst_n_sync) begin
        if (!rst_n_sync)
            count <= 8'd0;
        else if (enable)
            count <= count + 8'd1;
    end

endmodule
