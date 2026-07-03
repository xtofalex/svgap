module reset_timer (
    input  logic       clk,
    input  logic       por_n,
    input  logic       load,
    input  logic [3:0] load_value,
    output logic       expired
);

    (* ASYNC_REG = "TRUE" *) logic [1:0] reset_sync;
    logic [3:0] count;
    wire rst_n = reset_sync[1];

    always_ff @(posedge clk or negedge por_n) begin
        if (!por_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count   <= 4'd0;
            expired <= 1'b1;
        end else if (load) begin
            count   <= load_value;
            expired <= (load_value == 4'd0);
        end else if (count != 4'd0) begin
            count   <= count - 4'd1;
            expired <= (count == 4'd1);
        end else begin
            count   <= 4'd0;
            expired <= 1'b1;
        end
    end

endmodule
