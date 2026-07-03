module reset_fsm(input logic clk, input logic reset_n, input logic start,
                 output logic busy, output logic done);

  // -----------------------------------------------------------------------
  // Reset synchronizer: asynchronous assertion, synchronous de-assertion.
  // This guarantees that every state-holding element in this module sees
  // a reset release that is synchronized to clk (meeting recovery/removal
  // timing), while still reacting immediately (asynchronously) to the
  // external reset_n assertion.
  // -----------------------------------------------------------------------
  logic rst_sync_ff1, rst_sync_ff2;

  always_ff @(posedge clk or negedge reset_n) begin
    if (!reset_n) begin
      rst_sync_ff1 <= 1'b0;
      rst_sync_ff2 <= 1'b0;
    end else begin
      rst_sync_ff1 <= 1'b1;
      rst_sync_ff2 <= rst_sync_ff1;
    end
  end

  wire rst_n_sync = rst_sync_ff2;

  // -----------------------------------------------------------------------
  // FSM: IDLE -> BUSY1 -> BUSY2 -> DONE -> IDLE
  // busy asserted for two cycles (BUSY1, BUSY2), done pulses one cycle.
  // Uses the synchronized reset (async assert / sync deassert).
  // -----------------------------------------------------------------------
  typedef enum logic [1:0] {
    IDLE  = 2'b00,
    BUSY1 = 2'b01,
    BUSY2 = 2'b10,
    DONE  = 2'b11
  } state_t;

  state_t state, next_state;

  always_ff @(posedge clk or negedge rst_n_sync) begin
    if (!rst_n_sync)
      state <= IDLE;
    else
      state <= next_state;
  end

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

  assign busy = (state == BUSY1) || (state == BUSY2);
  assign done = (state == DONE);

endmodule
