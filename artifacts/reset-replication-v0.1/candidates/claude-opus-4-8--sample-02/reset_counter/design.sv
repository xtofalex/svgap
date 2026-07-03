module reset_counter(input logic clk, input logic arst_n, input logic enable,
                     output logic [7:0] count);

    // Reset synchronizer: asynchronous assertion, synchronous deassertion.
    logic rst_meta_n, rst_sync_n;

    always_ff @(posedge clk or negedge arst_n) begin
        if (!arst_n) begin
            rst_meta_n <= 1'b0;
            rst_sync_n <= 1'b0;
        end else begin
            rst_meta_n <= 1'b1;
            rst_sync_n <= rst_meta_n;
        end
    end

    // Counter uses the synchronized reset as its own asynchronous reset,
    // so counter state clears asynchronously on assertion and releases
    // synchronously with clk.
    always_ff @(posedge clk or negedge rst_sync_n) begin
        if (!rst_sync_n)
            count <= 8'd0;
        else if (enable)
            count <= count + 8'd1;
    end

endmodule
