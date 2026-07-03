module reset_fsm(input logic clk, input logic reset_n, input logic start,
                 output logic busy, output logic done);

    // -----------------------------------------------------------------
    // Reset synchronizer:
    //   - Asynchronous assertion  (follows reset_n falling immediately)
    //   - Synchronous  de-assertion (release aligned to clk, protecting
    //     recovery/removal timing of every state element downstream)
    // Built only from generic flip-flops (no technology cells).
    // -----------------------------------------------------------------
    logic rst_meta_n;
    logic rst_sync_n;

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin
            rst_meta_n <= 1'b0;
            rst_sync_n <= 1'b0;
        end else begin
            rst_meta_n <= 1'b1;
            rst_sync_n <= rst_meta_n;
        end
    end

    // -----------------------------------------------------------------
    // FSM
    // -----------------------------------------------------------------
    typedef enum logic [1:0] {
        IDLE  = 2'd0,
        BUSY1 = 2'd1,
        BUSY2 = 2'd2,
        DONE_S = 2'd3
    } state_t;

    state_t state, next_state;

    // Next-state logic
    always_comb begin
        next_state = state;
        unique case (state)
            IDLE  : next_state = start ? BUSY1 : IDLE;
            BUSY1 : next_state = BUSY2;
            BUSY2 : next_state = DONE_S;
            DONE_S: next_state = IDLE;
            default: next_state = IDLE;
        endcase
    end

    // State register: asynchronous assert via synchronized reset,
    // whose de-assertion is clock-synchronous.
    always_ff @(posedge clk or negedge rst_sync_n) begin
        if (!rst_sync_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    // Outputs
    assign busy = (state == BUSY1) || (state == BUSY2);
    assign done = (state == DONE_S);

endmodule
