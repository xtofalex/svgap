module reset_fsm(input logic clk, input logic reset_n, input logic start,
                 output logic busy, output logic done);

  // -------------------------------------------------------------------------
  // Reset synchronizer:
  //   - Asynchronous assertion: when reset_n drops, both flops clear at once,
  //     so rst_n_sync falls immediately (independent of clk).
  //   - Synchronous de-assertion: on release, the '1' propagates through two
  //     flops, guaranteeing removal is aligned to clk and that recovery/removal
  //     timing is met for every downstream state element.
  // -------------------------------------------------------------------------
  logic sync_ff1, sync_ff2;
  logic rst_n_sync;

  always_ff @(posedge clk or negedge reset_n) begin
    if (!reset_n) begin
      sync_ff1 <= 1'b0;
      sync_ff2 <= 1'b0;
    end else begin
      sync_ff1 <= 1'b1;
      sync_ff2 <= sync_ff1;
    end
  end

  assign rst_n_sync = sync_ff2;

  // -------------------------------------------------------------------------
  // FSM
  // -------------------------------------------------------------------------
  typedef enum logic [1:0] {
    IDLE   = 2'd0,
    BUSY1  = 2'd1,
    BUSY2  = 2'd2,
    DONEST = 2'd3
  } state_t;

  state_t state, next_state;

  // State register uses the synchronized reset. Asynchronous assertion is
  // preserved (negedge rst_n_sync); de-assertion is already synchronized.
  always_ff @(posedge clk or negedge rst_n_sync) begin
    if (!rst_n_sync)
      state <= IDLE;
    else
      state <= next_state;
  end

  // Next-state logic
  always_comb begin
    next_state = state;
    case (state)
      IDLE   : next_state = start ? BUSY1 : IDLE;
      BUSY1  : next_state = BUSY2;   // busy cycle 1
      BUSY2  : next_state = DONEST;  // busy cycle 2
      DONEST : next_state = IDLE;    // done pulse
      default: next_state = IDLE;
    endcase
  end

  // Outputs
  always_comb begin
    busy = (state == BUSY1) || (state == BUSY2);
    done = (state == DONEST);
  end

endmodule
