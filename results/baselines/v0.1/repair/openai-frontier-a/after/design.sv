module reset_release (
    input  logic       clk,
    input  logic       arst_n,
    input  logic       enable,
    output logic [3:0] count
);
    logic [1:0] reset_sync;

    always_ff @(posedge clk or negedge arst_n) begin
        if (!arst_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    always_ff @(posedge clk or negedge arst_n) begin
        if (!arst_n)
            count <= 4'b0000;
        else if (!reset_sync[1])
            count <= 4'b0000;
        else if (enable)
            count <= count + 4'b0001;
    end
endmodule
