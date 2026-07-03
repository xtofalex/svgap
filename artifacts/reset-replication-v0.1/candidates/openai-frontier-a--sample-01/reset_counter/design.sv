module reset_counter(input logic clk, input logic arst_n, input logic enable,
                     output logic [7:0] count);

    logic [1:0] reset_sync;

    always_ff @(posedge clk or negedge arst_n) begin
        if (!arst_n) begin
            reset_sync <= 2'b00;
            count      <= 8'b0;
        end else begin
            reset_sync <= {reset_sync[0], 1'b1};

            if (!reset_sync[1])
                count <= 8'b0;
            else if (enable)
                count <= count + 8'b1;
        end
    end

endmodule
