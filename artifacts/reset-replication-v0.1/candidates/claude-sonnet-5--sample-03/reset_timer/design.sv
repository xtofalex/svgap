module reset_timer (
    input  logic       clk,
    input  logic       por_n,
    input  logic       load,
    input  logic [3:0] load_value,
    output logic       expired
);

    //--------------------------------------------------------------------
    // Reset synchronizer: asynchronous assertion, synchronous release.
    // Only the raw por_n (async source) is allowed to hit an asynchronous
    // reset pin. All other sequential state in the design is reset by
    // rst_n_sync below, which is asserted immediately (async) but
    // de-asserted only on a clk edge (synchronous release), avoiding
    // reset-removal timing/metastability issues on functional logic.
    //--------------------------------------------------------------------
    logic rst_n_meta;
    logic rst_n_sync;

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
    // Functional countdown timer.
    // Uses the synchronized reset (rst_n_sync): asynchronous assert,
    // synchronous release, as required for functional sequential state.
    //--------------------------------------------------------------------
    logic [3:0] count_q;

    always_ff @(posedge clk or negedge rst_n_sync) begin
        if (!rst_n_sync) begin
            count_q <= 4'h0;
        end else if (load) begin
            count_q <= load_value;
        end else if (count_q != 4'h0) begin
            count_q <= count_q - 4'h1;
        end
    end

    assign expired = (count_q == 4'h0);

endmodule
