#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Sep 30 23:11:02 2019
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import mascon__decode_module
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.offset_freq = offset_freq = -320000
        self.frequency = frequency = 40.68e6
        self.decimation = decimation = 50

        ##################################################
        # Blocks
        ##################################################
        self._frequency_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.frequency,
        	callback=self.set_frequency,
        	label='frequency',
        	converter=forms.float_converter(),
        )
        self.Add(self._frequency_text_box)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=24000,
        	v_scale=1,
        	v_offset=0,
        	t_scale=0.01,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Detect Bit',
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='',
        	minval=0,
        	maxval=12,
        	factor=1.0,
        	decimal_places=0,
        	ref_level=0,
        	sample_rate=24000,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label='Super Hikari Mascon State',
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Add(self.wxgui_numbersink2_0.win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate*decimation)
        self.osmosdr_source_0.set_center_freq(frequency - offset_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(0, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.mascon__decode_module_masdec_ii_0 = mascon__decode_module.masdec_ii(81, 12)
        self.low_pass_filter_0 = filter.fir_filter_ccf(decimation, firdes.low_pass(
        	1, samp_rate * decimation, 50e3, 10e3, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (32, ), offset_freq, samp_rate*decimation)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(1, 2, 0)
        self.blocks_int_to_float_0 = blocks.int_to_float(1, 1)
        self.blocks_float_to_int_0 = blocks.float_to_int(1, 1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=samp_rate ,
        	audio_decim=1,
        	audio_pass=3000,
        	audio_stop=4000,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_am_demod_cf_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_float_to_int_0, 0), (self.mascon__decode_module_masdec_ii_0, 0))
        self.connect((self.blocks_int_to_float_0, 0), (self.wxgui_numbersink2_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_int_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.mascon__decode_module_masdec_ii_0, 0), (self.blocks_int_to_float_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate*self.decimation)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate * self.decimation, 50e3, 10e3, firdes.WIN_HAMMING, 6.76))

    def get_offset_freq(self):
        return self.offset_freq

    def set_offset_freq(self, offset_freq):
        self.offset_freq = offset_freq
        self.osmosdr_source_0.set_center_freq(self.frequency - self.offset_freq, 0)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.offset_freq)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self._frequency_text_box.set_value(self.frequency)
        self.osmosdr_source_0.set_center_freq(self.frequency - self.offset_freq, 0)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.osmosdr_source_0.set_sample_rate(self.samp_rate*self.decimation)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate * self.decimation, 50e3, 10e3, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
