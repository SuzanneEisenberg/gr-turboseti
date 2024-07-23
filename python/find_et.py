#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Yiwei Chai.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import logging #make sure this is here
import numpy as np
import datetime as dt
import time

from gnuradio import gr
from turboseti_stream.doppler_finder import DopplerFinder

DEBUGGING = True

class find_et(gr.sync_block):

    """
    This is the script for the DopplerFinder block, which runs an adapted version of
    turboSETI (turboseti_stream) on a numpy float32 data matrix stored in RAM.

    Part of the ATA GNU Radio pipeline. See examples folder for use in flowgraph.

    Future Work:
    - Automate plotting of hits?

    Yiwei Chai
    Last updated September 18, 2021

    """

    def __init__(self, filename, source_name, src_raj, src_dej, tsamp, f_start, f_stop,
                 n_fine_chans, n_ints_in_file, log_level_int, coarse_chan, n_coarse_chan,
                 min_drift, max_drift, snr, out_dir):
                    # flagging, obs_info, append_output, blank_dc,
                    # kernels, gpu_backend, precision, gpu_id):
                    # Removed tstart parameter

        # Define parameters which need to be passed into DopplerFinder class
        self.filename = filename
        self.source_name = source_name
        self.src_raj = src_raj
        self.src_dej = src_dej
        #self.tstart = tstart
        self.tsamp = tsamp
        self.f_start = f_start
        self.f_stop = f_stop
        self.n_fine_chans = n_fine_chans
        self.n_ints_in_file = n_ints_in_file

        if log_level_int == 0:
            self.log_level_int = logging.DEBUG
        elif log_level_int == 1:
            self.log_level_int = logging.INFO
        elif log_level_int == 2:
            self.log_level_int = logging.WARN
        else:
            raise RuntimeError("Incorrect logging level (%i)"%log_level_int)

        self.coarse_chan = coarse_chan
        self.n_coarse_chan = n_coarse_chan
        self.min_drift = min_drift
        self.max_drift = max_drift
        self.snr = snr
        self.out_dir = out_dir
        #self.set_output_multiple(60)
        # self.flagging = flagging
        # self.obs_info = obs_info
        # self.append_output = append_output
        # self.blank_dc = blank_dc
        # self.kernels = kernels
        # self.gpu_backend = gpu_backend
        # self.precision = precision
        # self.gpu_id = gpu_id

        gr.sync_block.__init__(self,
            name="find_et",
            in_sig=[(np.float32, self.n_fine_chans)],
            out_sig=None)


    def work(self, input_items, output_items):
        #self.spectra = np.empty((0, self.n_fine_chans), dtype=np.float32, order='C')
        i = 0
        for i in range(61):
            spectra[0][i] = input_items[0][i]
            i =+1

        if DEBUGGING:
            print("DEBUG findET input_items[0] shape:", input_items[0].shape) #Checks input is expected shape (60, 1e6)

        #spectra = input_items[0]
        if DEBUGGING:
            print("DEBUG Current spectra shape:", spectra.shape)
            print("DEBUG Current spectra:", spectra)

        print("Initialising Clancy...")

        tstart_utc = time.time()
        # tstart_local = str(dt.date.today()) + "_" + str(dt.datetime.now().time())

        # obs_info = {'pulsar': 0, 'pulsar_found': 0, 'pulsar_dm': 0.0, 'pulsar_snr': 0.0,
        #                'pulsar_stats': self.kernels.np.zeros(6), 'RFI_level': 0.0,
        #                'Mean_SEFD': 0.0, 'psrflux_Sens': 0.0,
        #                'SEFDs_val': [0.0], 'SEFDs_freq': [0.0], 'SEFDs_freq_up': [0.0]}

        filename_timestamped = self.source_name + "_" + self.filename + "_" + str(tstart_utc)
        if DEBUGGING:
            print("DEBUG Filename w/ timestamp:", filename_timestamped)

        clancy = DopplerFinder(filename = filename_timestamped,
                               source_name = self.source_name,
                               src_raj = self.src_raj,
                               src_dej = self.src_dej,
                               tstart = tstart_utc,
                               tsamp = self.tsamp,
                               f_start = self.f_start,
                               f_stop = self.f_stop,
                               n_fine_chans = self.n_fine_chans,
                               n_ints_in_file = self.n_ints_in_file,
                               log_level_int = self.log_level_int,
                               coarse_chan_num = self.coarse_chan,
                               n_coarse_chan = self.n_coarse_chan,
                               min_drift = self.min_drift,
                               max_drift = self.max_drift,
                               snr = self.snr,
                               out_dir = self.out_dir)
                               # flagging=False,
                               # obs_info=None,
                               # append_output=False,
                               # blank_dc=True,
                               # kernels=None,
                               # gpu_backend=False,
                               # precision=1,
                               # gpu_id=0)
        print("Clancy is looking for ET...")
        clancy.find_ET(spectra)
        print("Clancy is done.")

        # Insert a way to plot hits

        return len(spectra)
