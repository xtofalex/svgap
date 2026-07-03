module reset_config(
    input  logic       clk,
    input  logic       global_reset_n,
    input  logic       write_en,
    input  logic [3:0] config_in,
    output logic [3:0] config_out
);

    // Two-flop synchronizer for reset release.
    // Asynchronous assertion is allowed to propagate immediately,
    // but deassertion (release) is synchronized to clk.
    logic sync_reset_n_meta;
    logic sync_reset_n;

    always_ff @(posedge clk or negedge global_reset_n) begin
        if (!global_reset_n) begin
            sync_reset_n_meta <= 1'b0;
            sync_reset_n      <= 1'b0;
        end else begin
            sync_reset_n_meta <= 1'b1;
            sync_reset_n      <= sync_reset_n_meta;
        end
    end

    // Configuration register uses only the synchronized reset,
    // never the raw asynchronous reset pin directly.
    always_ff @(posedge clk or negedge sync_reset_n) begin
        if (!sync_reset_n) begin
            config_out <= 4'b0000;
        end else if (write_en) begin
            config_out <= config_in;
        end
    end

endmodule
