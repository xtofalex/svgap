module reset_config(input logic clk, input logic global_reset_n,
                    input logic write_en, input logic [3:0] config_in,
                    output logic [3:0] config_out);

    logic rst_sync_meta;
    logic rst_sync_n;

    always_ff @(posedge clk or negedge global_reset_n) begin
        if (!global_reset_n) begin
            rst_sync_meta <= 1'b0;
            rst_sync_n    <= 1'b0;
        end else begin
            rst_sync_meta <= 1'b1;
            rst_sync_n    <= rst_sync_meta;
        end
    end

    always_ff @(posedge clk or negedge rst_sync_n) begin
        if (!rst_sync_n) begin
            config_out <= 4'b0000;
        end else if (write_en) begin
            config_out <= config_in;
        end
    end

endmodule
