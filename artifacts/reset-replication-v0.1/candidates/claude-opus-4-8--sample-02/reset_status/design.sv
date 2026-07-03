module reset_status(input logic clk, input logic rst_n, input logic set_fault,
                    input logic clear_fault, output logic fault_latched);

    // Reset synchronizer: assert asynchronously, deassert synchronously
    logic rst_sync_meta;
    logic rst_sync_n;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rst_sync_meta <= 1'b0;
            rst_sync_n    <= 1'b0;
        end else begin
            rst_sync_meta <= 1'b1;
            rst_sync_n    <= rst_sync_meta;
        end
    end

    // Fault latch driven by the synchronized (glitch-free deassertion) reset
    always_ff @(posedge clk or negedge rst_sync_n) begin
        if (!rst_sync_n)
            fault_latched <= 1'b0;
        else if (clear_fault)
            fault_latched <= 1'b0;
        else if (set_fault)
            fault_latched <= 1'b1;
    end

endmodule
