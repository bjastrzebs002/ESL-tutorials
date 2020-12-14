from pygmyhdl import *

initialize()


@chunk
def blinker(clk_i, led_o, length):
    cnt = Bus(length, name='cnt')

    @seq_logic(clk_i.posedge)
    def counter_logic():
        cnt.next = cnt + 1

    @comb_logic
    def output_logic():
        led_o.next = cnt[length - 1]


clk = Wire(name='clk')
led = Wire(name='led')

blinker(clk_i=clk, led_o=led, length=3)

clk_sim(clk, num_cycles=16)

show_waveforms()
show_text_table()

toVerilog(blinker, clk_i=clk, led_o=led, length=22)

with open('blinker.pcf', 'w') as pcf:
    pcf.write(
        '''
        set_io led_o 99
        set_io clk_i 21
        '''
    )
