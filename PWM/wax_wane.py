from pygmyhdl import *
import math


@chunk
def pwm_simple(clk_i, pwm_o, threshold):
    cnt = Bus(len(threshold), name='cnt')

    @seq_logic(clk_i.posedge)
    def cntr_logic():
        cnt.next = cnt + 1

    @comb_logic
    def output_logic():
        pwm_o.next = cnt < threshold


initialize()

clk = Wire(name='clk')
pwm = Wire(name='pwm')
threshold = Bus(3, init_val=3)
pwm_simple(clk, pwm, threshold)

clk_sim(clk, num_cycles=24)
show_waveforms(start_time=13, tock=True)


@chunk
def pwm_less_simple(clk_i, pwm_o, threshold, duration):
    length = math.ceil(math.log(duration, 2))
    cnt = Bus(length, name='cnt')

    @seq_logic(clk_i.posedge)
    def cntr_logic():
        cnt.next = cnt + 1

        if cnt == duration - 1:
            cnt.next = 0

    @comb_logic
    def output_logic():
        pwm_o.next = cnt < threshold


initialize()
clk = Wire(name='clk')
pwm = Wire(name='pwm')
pwm_less_simple(clk, pwm, threshold=3, duration=5)
clk_sim(clk, num_cycles=15)
show_waveforms()

initialize()
clk = Wire(name='clk')
pwm = Wire(name='pwm')
threshold = Bus(4, name='threshold')
pwm_less_simple(clk, pwm, threshold, 10)


def test_bench(num_cycles):
    clk.next = 0
    threshold.next = 3
    yield delay(1)
    for cycle in range(num_cycles):
        clk.next = 0

        if cycle >= 14:
            threshold.next = 8
        yield delay(1)
        clk.next = 1
        yield delay(1)


simulate(test_bench(20))
show_waveforms(tick=True, start_time=19)


@chunk
def pwm_glitchless(clk_i, pwm_o, threshold, interval):
    import math
    length = math.ceil(math.log(interval, 2))
    cnt = Bus(length)

    threshold_r = Bus(length, name='threshold_r')

    @seq_logic(clk_i.posedge)
    def cntr_logic():
        cnt.next = cnt + 1
        if cnt == interval - 1:
            cnt.next = 0
            threshold_r.next = threshold

    @comb_logic
    def output_logic():
        pwm_o.next = cnt < threshold_r


initialize()
clk = Wire(name='clk')
pwm = Wire(name='pwm')
threshold = Bus(4, name='threshold')
pwm_glitchless(clk, pwm, threshold, 10)

simulate(test_bench(22))
show_waveforms(tick=True, start_time=19)


@chunk
def ramp(clk_i, ramp_o):
    delta = Bus(len(ramp_o))

    @seq_logic(clk_i.posedge)
    def logic():

        ramp_o.next = ramp_o + delta

        if ramp_o == 1:
            delta.next = 1


        elif ramp_o == ramp_o.max - 2:
            delta.next = -1

        elif delta == 0:
            delta.next = 1
            ramp_o.next = 1


@chunk
def wax_wane(clk_i, led_o, length):
    rampout = Bus(length, name='ramp')
    ramp(clk_i, rampout)
    pwm_simple(clk_i, led_o, rampout.o[length:length - 4])


initialize()
clk = Wire(name='clk')
led = Wire(name='led')
wax_wane(clk, led, 6)

clk_sim(clk, num_cycles=180)
t = 110
show_waveforms(tick=True, start_time=t, stop_time=t + 40)

toVerilog(wax_wane, clk, led, 23)

with open('wax_wane.pcf', 'w') as pcf:
    pcf.write(
        '''
        set_io clk_i  21
        set_io led_o  99
        '''
    )
