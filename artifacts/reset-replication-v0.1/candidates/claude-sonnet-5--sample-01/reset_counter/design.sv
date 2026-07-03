module reset_counter(input logic clk, input logic arst_n, input logic enable,
                     output logic [7:0] count);

  logic rst_n_meta, rst_n_sync;

  always_ff @(posedge clk or negedge arst_n) begin
    if (!arst_n) begin
      rst_n_meta <= 1'b0;
      rst_n_sync <= 1'b0;
    end else begin
      rst_n_meta <= 1'b1;
      rst_n_sync <= rst_n_meta;
    end
  end

  always_ff @(posedge clk or negedge arst_n) begin
    if (!arst_n) begin
      count <= 8'h00;
    end else if (!rst_n_sync) begin
      count <= 8'h00;
    end else if (enable) begin
      count <= count + 8'h01;
    end
  end

endmodule
