module reset_status(input logic clk, input logic rst_n, input logic set_fault,
                    input logic clear_fault, output logic fault_latched);

    // Reset synchronizer: assert asynchronously, deassert synchronously
    logic rst_sync_ff1, rst_sync_ff2;
    logic rst_n_sync;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rst_sync_ff1 <= 1'b0;
            rst_sync_ff2 <= 1'b0;
        end else begin
            rst_sync_ff1 <= 1'b1;
            rst_sync_ff2 <= rst_sync_ff1;
        end
    end

    assign rst_n_sync = rst_sync_ff2;

    // Fault latch: fully synchronous, driven only by the synchronized reset
    always_ff @(posedge clk) begin
        if (!rst_n_sync)
            fault_latched <= 1'b0;
        else if (clear_fault)
            fault_latched <= 1'b0;
        else if (set_fault)
            fault_latched <= 1'b1;
    end

endmodule
