module reset_config(input logic clk, input logic global_reset_n,
                    input logic write_en, input logic [3:0] config_in,
                    output logic [3:0] config_out);

  logic rst_ff1;
  logic sync_rst_n;

  always_ff @(posedge clk or negedge global_reset_n) begin
    if (!global_reset_n) begin
      rst_ff1    <= 1'b0;
      sync_rst_n <= 1'b0;
    end else begin
      rst_ff1    <= 1'b1;
      sync_rst_n <= rst_ff1;
    end
  end

  always_ff @(posedge clk or negedge sync_rst_n) begin
    if (!sync_rst_n)
      config_out <= 4'b0000;
    else if (write_en)
      config_out <= config_in;
  end

endmodule
