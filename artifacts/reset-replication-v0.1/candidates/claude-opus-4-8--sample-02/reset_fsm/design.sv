module reset_fsm(input logic clk, input logic reset_n, input logic start,
                 output logic busy, output logic done);

    // -----------------------------------------------------------------
    // Reset synchronizer:
    //   - Asynchronous assertion  : rst_n_sync follows reset_n low
    //                               immediately (async clear of the FFs)
    //   - Synchronous de-assertion: recovery/removal is timed by clk
    // No technology-specific cells are instantiated; standard inferable
    // flip-flops are used.
    // -----------------------------------------------------------------
    logic rst_sync_meta;
    logic rst_n_sync;

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n) begin
            rst_sync_meta <= 1'b0;
            rst_n_sync    <= 1'b0;
        end else begin
            rst_sync_meta <= 1'b1;
            rst_n_sync    <= rst_sync_meta;
        end
    end

    // -----------------------------------------------------------------
    // FSM
    // -----------------------------------------------------------------
    typedef enum logic [1:0] {
        IDLE  = 2'b00,
        BUSY1 = 2'b01,
        BUSY2 = 2'b10,
        DONE  = 2'b11
    } state_t;

    state_t state, next_state;

    // State register: async assert (via rst_n_sync going low), sync removal.
    always_ff @(posedge clk or negedge rst_n_sync) begin
        if (!rst_n_sync)
            state <= IDLE;
        else
            state <= next_state;
    end

    // Next-state logic
    always_comb begin
        next_state = state;
        unique case (state)
            IDLE:  next_state = start ? BUSY1 : IDLE;
            BUSY1: next_state = BUSY2;
            BUSY2: next_state = DONE;
            DONE:  next_state = IDLE;
            default: next_state = IDLE;
        endcase
    end

    // Output logic (Moore)
    always_comb begin
        busy = (state == BUSY1) || (state == BUSY2);
        done = (state == DONE);
    end

endmodule
