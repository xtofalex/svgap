module reset_config (
    input  logic       clk,
    input  logic       global_reset_n,
    input  logic       write_en,
    input  logic [3:0] config_in,
    output logic [3:0] config_out
);

    logic [1:0] reset_sync;
    logic       reset_n;

    always_ff @(posedge clk or negedge global_reset_n) begin
        if (!global_reset_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    assign reset_n = reset_sync[1];

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n)
            config_out <= 4'b0000;
        else if (write_en)
            config_out <= config_in;
    end

endmodule
