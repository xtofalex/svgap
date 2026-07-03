module reset_events (
    input  logic       clk,
    input  logic       ext_rst_n,
    input  logic       event_valid,
    output logic [7:0] event_count
);

    logic [1:0] reset_sync;
    logic       reset_n;

    always_ff @(posedge clk or negedge ext_rst_n) begin
        if (!ext_rst_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    assign reset_n = reset_sync[1];

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n)
            event_count <= 8'b0;
        else if (event_valid)
            event_count <= event_count + 8'd1;
    end

endmodule
