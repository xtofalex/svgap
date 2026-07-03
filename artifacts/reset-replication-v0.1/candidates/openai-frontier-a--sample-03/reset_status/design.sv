module reset_status(
    input  logic clk,
    input  logic rst_n,
    input  logic set_fault,
    input  logic clear_fault,
    output logic fault_latched
);

    logic [1:0] rst_sync;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            rst_sync <= 2'b00;
        else
            rst_sync <= {rst_sync[0], 1'b1};
    end

    always_ff @(posedge clk or negedge rst_sync[1]) begin
        if (!rst_sync[1])
            fault_latched <= 1'b0;
        else if (clear_fault)
            fault_latched <= 1'b0;
        else if (set_fault)
            fault_latched <= 1'b1;
    end

endmodule
