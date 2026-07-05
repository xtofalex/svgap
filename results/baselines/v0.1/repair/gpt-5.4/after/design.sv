module reset_release (
    input  logic       clk,
    input  logic       arst_n,
    input  logic       enable,
    output logic [3:0] count
);
    logic arst_n_sync1;
    logic arst_n_sync2;

    always_ff @(posedge clk or negedge arst_n) begin
        if (!arst_n) begin
            arst_n_sync1 <= 1'b0;
            arst_n_sync2 <= 1'b0;
        end else begin
            arst_n_sync1 <= 1'b1;
            arst_n_sync2 <= arst_n_sync1;
        end
    end

    always_ff @(posedge clk or negedge arst_n_sync2) begin
        if (!arst_n_sync2)
            count <= 4'd0;
        else if (enable)
            count <= count + 4'd1;
    end
endmodule
