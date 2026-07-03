module reset_timer (
    input  logic       clk,
    input  logic       por_n,        // async assert, active-low power-on reset
    input  logic       load,
    input  logic [3:0] load_value,
    output logic       expired
);

    //--------------------------------------------------------------------------
    // Reset synchronizer:
    //   Assert  : asynchronous (follows por_n immediately)
    //   Release : synchronous  (two clk edges after por_n de-asserts)
    //--------------------------------------------------------------------------
    logic rst_meta_n;   // first synchronizer stage
    logic rst_sync_n;   // synchronized internal reset (active-low)

    always_ff @(posedge clk or negedge por_n) begin
        if (!por_n) begin
            rst_meta_n <= 1'b0;
            rst_sync_n <= 1'b0;
        end
        else begin
            rst_meta_n <= 1'b1;
            rst_sync_n <= rst_meta_n;
        end
    end

    //--------------------------------------------------------------------------
    // Functional counter, reset by the synchronized reset.
    //   Async assert (negedge rst_sync_n) clears state instantly.
    //   Release is inherently synchronous because rst_sync_n only de-asserts
    //   on a clk edge.
    //--------------------------------------------------------------------------
    logic [3:0] count;

    always_ff @(posedge clk or negedge rst_sync_n) begin
        if (!rst_sync_n) begin
            count <= 4'd0;
        end
        else if (load) begin
            count <= load_value;
        end
        else if (count != 4'd0) begin
            count <= count - 4'd1;
        end
        // else: hold at zero
    end

    //--------------------------------------------------------------------------
    // expired is asserted while the timer sits at zero.
    //--------------------------------------------------------------------------
    assign expired = (count == 4'd0);

endmodule
