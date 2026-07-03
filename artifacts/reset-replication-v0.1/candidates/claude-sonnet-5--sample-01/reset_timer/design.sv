module reset_timer (
    input  logic       clk,
    input  logic       por_n,
    input  logic       load,
    input  logic [3:0] load_value,
    output logic        expired
);

    //--------------------------------------------------------------------
    // Reset synchronizer: assert asynchronously (tied to por_n), release
    // synchronously to clk. This produces a clean, glitch-free reset for
    // use by the downstream sequential logic.
    //--------------------------------------------------------------------
    logic sync_rst_n_meta;
    logic sync_rst_n;

    always_ff @(posedge clk or negedge por_n) begin
        if (!por_n) begin
            sync_rst_n_meta <= 1'b0;
            sync_rst_n      <= 1'b0;
        end else begin
            sync_rst_n_meta <= 1'b1;
            sync_rst_n      <= sync_rst_n_meta;
        end
    end

    //--------------------------------------------------------------------
    // Countdown counter: reset asynchronously by the synchronized reset
    // (whose deassertion edge is already aligned to clk), loads
    // load_value on 'load', and decrements once per clock otherwise.
    //--------------------------------------------------------------------
    logic [3:0] count;

    always_ff @(posedge clk or negedge sync_rst_n) begin
        if (!sync_rst_n) begin
            count <= 4'd0;
        end else if (load) begin
            count <= load_value;
        end else if (count != 4'd0) begin
            count <= count - 4'd1;
        end
    end

    assign expired = (count == 4'd0);

endmodule
