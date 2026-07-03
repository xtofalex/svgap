module reset_counter(input logic clk, input logic arst_n, input logic enable,
                     output logic [7:0] count);

    // Two-flop reset synchronizer: asynchronous assert, synchronous deassert
    logic rst_sync_ff1, rst_sync_ff2;

    always_ff @(posedge clk or negedge arst_n) begin
        if (!arst_n) begin
            rst_sync_ff1 <= 1'b0;
            rst_sync_ff2 <= 1'b0;
        end else begin
            rst_sync_ff1 <= 1'b1;
            rst_sync_ff2 <= rst_sync_ff1;
        end
    end

    // Synchronized active-low reset applied directly to counter state
    logic arst_n_sync;
    assign arst_n_sync = rst_sync_ff2;

    always_ff @(posedge clk or negedge arst_n) begin
        if (!arst_n) begin
            count <= 8'd0;
        end else if (!arst_n_sync) begin
            count <= 8'd0;
        end else if (enable) begin
            count <= count + 8'd1;
        end
    end

endmodule
