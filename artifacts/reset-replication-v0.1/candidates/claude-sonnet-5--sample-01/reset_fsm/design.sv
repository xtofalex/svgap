module reset_fsm(input logic clk, input logic reset_n, input logic start,
                 output logic busy, output logic done);

    // ---------------------------------------------------------------
    // Internal reset synchronizer
    // Assertion of reset_n (going low) takes effect asynchronously
    // because it directly drives the async reset of these flops.
    // De-assertion (going high) is synchronized to clk via the
    // two-stage synchronizer, so downstream logic sees a
    // synchronously released, asynchronously assertable reset.
    // ---------------------------------------------------------------
    logic sync_rst_ff1, sync_rst_ff2;

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin
            sync_rst_ff1 <= 1'b0;
            sync_rst_ff2 <= 1'b0;
        end else begin
            sync_rst_ff1 <= 1'b1;
            sync_rst_ff2 <= sync_rst_ff1;
        end
    end

    logic sync_reset_n;
    assign sync_reset_n = sync_rst_ff2;

    // ---------------------------------------------------------------
    // FSM states
    // ---------------------------------------------------------------
    typedef enum logic [1:0] {
        IDLE  = 2'b00,
        BUSY1 = 2'b01,
        BUSY2 = 2'b10,
        DONE  = 2'b11
    } state_t;

    state_t state, next_state;

    // State register: async assert (via sync_reset_n), sync deassert
    // is inherently guaranteed since sync_reset_n itself is released
    // synchronously to clk.
    always_ff @(posedge clk or negedge sync_reset_n) begin
        if (!sync_reset_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    // Next-state logic
    always_comb begin
        next_state = state;
        case (state)
            IDLE:  next_state = start ? BUSY1 : IDLE;
            BUSY1: next_state = BUSY2;
            BUSY2: next_state = DONE;
            DONE:  next_state = IDLE;
            default: next_state = IDLE;
        endcase
    end

    // Output logic
    always_comb begin
        busy = (state == BUSY1) || (state == BUSY2);
        done = (state == DONE);
    end

endmodule
