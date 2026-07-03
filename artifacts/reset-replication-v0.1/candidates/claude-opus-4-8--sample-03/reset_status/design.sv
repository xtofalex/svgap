module reset_status(input logic clk, input logic rst_n, input logic set_fault,
                    input logic clear_fault, output logic fault_latched);

    // Reset synchronizer: asynchronous assertion, synchronous deassertion.
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

    // Fault latch uses the synchronized (async-assert, sync-deassert) reset.
    always_ff @(posedge clk or negedge rst_sync_n) begin
        if (!rst_sync_n) begin
            fault_latched <= 1'b0;
        end else if (clear_fault) begin
            fault_latched <= 1'b0;   // clear takes priority
        end else if (set_fault) begin
            fault_latched <= 1'b1;
        end
    end

endmodule
