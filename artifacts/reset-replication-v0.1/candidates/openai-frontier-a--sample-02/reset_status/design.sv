module reset_status (
    input  logic clk,
    input  logic rst_n,
    input  logic set_fault,
    input  logic clear_fault,
    output logic fault_latched
);

    logic [1:0] reset_sync;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    always_ff @(posedge clk or negedge reset_sync[1]) begin
        if (!reset_sync[1])
            fault_latched <= 1'b0;
        else if (clear_fault)
            fault_latched <= 1'b0;
        else if (set_fault)
            fault_latched <= 1'b1;
    end

endmodule
