module reset_timer (
    input  logic       clk,
    input  logic       por_n,       // asynchronous power-on reset, active low
    input  logic       load,
    input  logic [3:0] load_value,
    output logic        expired
);

    //--------------------------------------------------------------------
    // Reset synchronizer: assert asynchronously (on por_n falling edge),
    // release synchronously to clk using a 2-flop synchronizer chain.
    // The 'ASYNC_REG' attribute hints synthesis/place-and-route tools to
    // keep these flops close together and avoid optimizing away the
    // metastability-hardened chain (portable across most toolchains that
    // recognize it; ignored harmlessly otherwise).
    //--------------------------------------------------------------------
    (* ASYNC_REG = "TRUE" *) logic rst_n_meta;
    (* ASYNC_REG = "TRUE" *) logic rst_n_sync;

    always_ff @(posedge clk or negedge por_n) begin
        if (!por_n) begin
            rst_n_meta <= 1'b0;
            rst_n_sync <= 1'b0;
        end else begin
            rst_n_meta <= 1'b1;
            rst_n_sync <= rst_n_meta;
        end
    end

    //--------------------------------------------------------------------
    // Countdown timer logic, using the synchronously-released,
    // asynchronously-asserted reset (rst_n_sync).
    //--------------------------------------------------------------------
    logic [3:0] count;

    always_ff @(posedge clk or negedge rst_n_sync) begin
        if (!rst_n_sync) begin
            count   <= 4'd0;
            expired <= 1'b0;
        end else if (load) begin
            count   <= load_value;
            expired <= (load_value == 4'd0);
        end else if (count != 4'd0) begin
            count   <= count - 4'd1;
            expired <= (count == 4'd1);
        end else begin
            expired <= 1'b1;
        end
    end

endmodule
