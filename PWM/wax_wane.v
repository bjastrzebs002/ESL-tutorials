// File: wax_wane.v
// Generated by MyHDL 0.11
// Date: Tue Dec 15 00:24:43 2020


`timescale 1ns/10ps

module wax_wane (
    clk_i,
    led_o
);


input clk_i;
output led_o;
wire led_o;

reg [22:0] rampout;
reg [3:0] chunk_insts_0_cnt;
reg [22:0] k_delta;




assign led_o = (chunk_insts_0_cnt < rampout[23-1:19]);


always @(posedge clk_i) begin: WAX_WANE_LOC_INSTS_CHUNK_INSTS_0_LOC_INSTS_CHUNK_INSTS_K
    chunk_insts_0_cnt <= (chunk_insts_0_cnt + 1);
end


always @(posedge clk_i) begin: WAX_WANE_LOC_INSTS_CHUNK_INSTS_K_LOC_INSTS_CHUNK_INSTS_K
    rampout <= (rampout + k_delta);
    if ((rampout == 1)) begin
        k_delta <= 1;
    end
    else if (($signed({1'b0, rampout}) == (8388608 - 2))) begin
        k_delta <= (-1);
    end
    else if ((k_delta == 0)) begin
        k_delta <= 1;
        rampout <= 1;
    end
end

endmodule
