module reset_fsm(
    input  logic clk,
    input  logic reset_n,
    input  logic start,
    output logic busy,
    output logic done
);

    logic [1:0] reset_sync;
    logic       internal_reset_n;

    typedef enum logic [1:0] {
        IDLE,
        BUSY_CYCLE_1,
        BUSY_CYCLE_2,
        DONE_CYCLE
    } state_t;

    state_t state, next_state;

    always_ff @(posedge clk or negedge reset_n) begin
        if (!reset_n)
            reset_sync <= 2'b00;
        else
            reset_sync <= {reset_sync[0], 1'b1};
    end

    assign internal_reset_n = reset_sync[1];

    always_ff @(posedge clk or negedge internal_reset_n) begin
        if (!internal_reset_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    always_comb begin
        next_state = state;
        busy       = 1'b0;
        done       = 1'b0;

        case (state)
            IDLE: begin
                if (start)
                    next_state = BUSY_CYCLE_1;
            end

            BUSY_CYCLE_1: begin
                busy       = 1'b1;
                next_state = BUSY_CYCLE_2;
            end

            BUSY_CYCLE_2: begin
                busy       = 1'b1;
                next_state = DONE_CYCLE;
            end

            DONE_CYCLE: begin
                done       = 1'b1;
                next_state = IDLE;
            end

            default: next_state = IDLE;
        endcase
    end

endmodule
