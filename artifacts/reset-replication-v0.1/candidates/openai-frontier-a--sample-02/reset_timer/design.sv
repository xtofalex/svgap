module reset_timer (
    input  logic       clk,
    input  logic       por_n,
    input  logic       load,
    input  logic [3:0] load_value,
    output logic       expired
);

    (* ASYNC_REG = "TRUE" *) logic [1:0] reset_sync;
    logic reset_n;
    logic [3:0] count;

    always_ff @(posedge clk or negedge por_n) begin
        if (!por_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    assign reset_n = reset_sync[1];

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n)
            count <= 4'b0000;
        else if (load)
            count <= load_value;
        else if (count != 4'b0000)
            count <= count - 4'b0001;
    end

    always_comb begin
        expired = (count == 4'b0000);
    end

endmodule
