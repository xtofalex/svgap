module reset_status(input logic clk, input logic rst_n, input logic set_fault,
                    input logic clear_fault, output logic fault_latched);

    // Reset synchronizer: asynchronous assert, synchronous deassert.
    // The two-flop chain itself is the only place rst_n's async
    // release is observed; everything downstream sees a reset
    // signal whose deassertion is aligned to clk.
    logic rst_n_meta;
    logic rst_n_sync;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rst_n_meta <= 1'b0;
            rst_n_sync <= 1'b0;
        end else begin
            rst_n_meta <= 1'b1;
            rst_n_sync <= rst_n_meta;
        end
    end

    // Fault latch: async assert via synchronized reset (which only
    // ever deasserts synchronously to clk), clear takes priority
    // over set.
    always_ff @(posedge clk or negedge rst_n_sync) begin
        if (!rst_n_sync) begin
            fault_latched <= 1'b0;
        end else if (clear_fault) begin
            fault_latched <= 1'b0;
        end else if (set_fault) begin
            fault_latched <= 1'b1;
        end
    end

endmodule
