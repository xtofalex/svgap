module reset_events(input logic clk, input logic ext_rst_n, input logic event_valid,
                    output logic [7:0] event_count);

    // Reset synchronizer:
    //   - Asserts asynchronously (clears promptly when ext_rst_n falls)
    //   - Deasserts synchronously (release is clock-aligned so no counter
    //     bit sees a raw asynchronous deassertion)
    logic rst_sync_meta;
    logic rst_n_sync;

    always_ff @(posedge clk or negedge ext_rst_n) begin
        if (!ext_rst_n) begin
            rst_sync_meta <= 1'b0;
            rst_n_sync    <= 1'b0;
        end
        else begin
            rst_sync_meta <= 1'b1;
            rst_n_sync    <= rst_sync_meta;
        end
    end

    // Event counter using the synchronized reset.
    always_ff @(posedge clk or negedge rst_n_sync) begin
        if (!rst_n_sync)
            event_count <= 8'd0;
        else if (event_valid)
            event_count <= event_count + 8'd1;
    end

endmodule
