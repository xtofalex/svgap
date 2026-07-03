module reset_events (
    input  logic       clk,
    input  logic       ext_rst_n,
    input  logic       event_valid,
    output logic [7:0] event_count
);

    logic [1:0] rst_sync;

    always_ff @(posedge clk or negedge ext_rst_n) begin
        if (!ext_rst_n)
            rst_sync <= 2'b00;
        else
            rst_sync <= {rst_sync[0], 1'b1};
    end

    always_ff @(posedge clk or negedge rst_sync[1]) begin
        if (!rst_sync[1])
            event_count <= 8'b0;
        else if (event_valid)
            event_count <= event_count + 8'd1;
    end

endmodule
