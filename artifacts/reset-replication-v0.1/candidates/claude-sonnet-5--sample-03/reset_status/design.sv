module reset_status(input logic clk, input logic rst_n, input logic set_fault,
                    input logic clear_fault, output logic fault_latched);

  logic rst_n_sync_meta, rst_n_sync;

  // Asynchronous assert, synchronous deassert reset synchronizer
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      rst_n_sync_meta <= 1'b0;
      rst_n_sync      <= 1'b0;
    end else begin
      rst_n_sync_meta <= 1'b1;
      rst_n_sync      <= rst_n_sync_meta;
    end
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      fault_latched <= 1'b0;
    end else if (!rst_n_sync) begin
      fault_latched <= 1'b0;
    end else if (clear_fault) begin
      fault_latched <= 1'b0;
    end else if (set_fault) begin
      fault_latched <= 1'b1;
    end
  end

endmodule
