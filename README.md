# A turboSETI block for GNU Radio

Update, fork by Suzanne Eisenberg as part of SETI REU 2024: the find_ET block now combines the functionality of the previous find_ET and find_ET_buffer blocks. The matrix output is 60 by FFT size. 

Orginal Read Me: 

This is a GNU Radio Out of Tree (OOT) module for the `findET` blocks. The aim is to create a GNU Radio block that can perform turboSETI analysis on a `numpy.float32` data matrix stored in RAM.

The module currently consists of 3 blocks:
- [findET](https://github.com/youais/gr-turboseti/blob/master/python/find_et.py)
- [findET Buffer](https://github.com/youais/gr-turboseti/blob/master/python/find_et_buffer.py)
- [findET Sink](https://github.com/youais/gr-turboseti/blob/master/python/find_et_sync.py)

The `findET Sink` block seeks to combine the functions of both `findET Buffer` and `findET`. For a good example of the intended output of `findET Sink`, refer to [`turboseti_multiprocessing_test.py`](https://github.com/youais/gr-turboseti/blob/master/examples/turboseti_multiprocessing_test.py). 

This code has been tested on a Linux installation of GNU Radio version 3.8.


### Dependencies

- [turboseti-stream](https://github.com/luigifcruz/turboseti-stream)
- [turboSETI](https://github.com/UCBerkeleySETI/turbo_seti/tree/e9dbcd8319cf332858ed95e3090ae1feeebab25d)
- [blimpy](https://github.com/UCBerkeleySETI/blimpy)
- [GNU Radio version 3.8](https://wiki.gnuradio.org/index.php/InstallingGR)
- [gr-ata OOT module](https://github.com/SETIatHCRO/gr-ata) (not necessary for this module, but needed to run ATA observations)


### Installing `gr-turboseti`

```
git clone https://github.com/youais/gr-turboseti.git
cd gr-turboseti
mkdir build
cd build
cmake ../
sudo make install
sudo ldconfig #for Linux users
```
You may need to specify the install path when running `cmake`.


### Navigating this Github Repo

- [`/python`](https://github.com/youais/gr-turboseti/tree/master/python) -- Python source code for blocks
- [`/grc`](https://github.com/youais/gr-turboseti/tree/master/grc) -- `.yml` code for blocks' appearance in GNU Radio Companion (GRC)
- [`/lib`](https://github.com/youais/gr-turboseti/tree/master/lib) -- C++ source code for blocks (not used in this module)
- [`/examples`](https://github.com/youais/gr-turboseti/tree/master/examples) -- Examples of flowgraph and `turboseti_stream` output, as well as observation planning code


### Background

This project was undertaken as part of the Berkeley SETI Research Center 2021 summer REU. My mentors were Dr. Wael Farah (SETI Institute), and Dr. Steve Croft (Breakthrough Listen, UC Berkeley).

The aim of my project is to develop a SETI data processing pipeline for the Allen Telescope Array (ATA), using GNU Radio. The ATA is a radio interferometer operated by the SETI Institute at the Hat Creek Radio Observatory in California, and consists of 42 fully-steerable antennae, each 6.1m in diameter. Its main science goal is to perform searches for technosignatures, which appear as narrowband signals 'drifting' in frequency. 

Currently, the existing data-processing pipeline for the ATA uses custom hardware unavailable to those not on-site. GNU Radio is a free open-source software for developing signal-processing routines, and is used by a large community of amateur radio astronomers and enthusiasts. The implementation of a GNU Radio SETI pipeline will make the search for extraterrestrial intelligence more accesible to smaller radio observatories and citizen scientists.


### Pipeline Details

The GNU Radio SETI pipeline is outlined as follows:
1. Radio telescope data from the ATA streams in through a USRP source
2. The data is 'channelised' through a polyphase filterbank (PFB), followed by a Fast Fourier Transform (FFT). This creates a high-resolution spectral product on the order of ~1MHz
3. This product accumulates in findET Buffer for ~60s, to create a data matrix of shape (60, 1e6)
4. The data matrix is then passed to findET, which uses an adapted version of turboSETI (i.e. [turboseti_stream](https://github.com/luigifcruz/turboseti-stream/blob/main/main.py)) to analyses it for potential technosignatures

Example flowgraph (refer to examples folder for .grc file):
![ts_1chn_filesrc_ex](https://user-images.githubusercontent.com/54188486/134052409-abc0caf0-8d9a-4973-b642-cd8f5d6db0f4.jpg)



### Outcome (as of September 19, 2021)

Working:
- `findET` block
- `findET Buffer` block
- 1 channel USRP/File Source flowgraph up to 1 MHz sample rate
- 4 channel USRP/File Source flowgraph up to 4 MHz sample rate

Issues:
- `findET Sink` block -- current issue: `TypeError: cannot pickle 'SwigPyObject' object`

### Future Work

1. Automate plotting of dynamic spectra of hits (adapt turboSETI's `find_event_pipeline` and `plot_event_pipeline` functions)
2. Increase maximum sample rate at which the flowgraphs can run (using multiprocessing?)
3. Observe known technosignature source (e.g. Chang'e 5) with the ATA using the GNU Radio SETI pipeline
4. Turn `gr-turboseti` into PyPi package
5. Begin ATA observations of interesting stars using the GNU Radio SETI pipeline

I plan to continue working on this project into the academic year.


### Acknowledgements

Richard Elkins and Luigi Cruz did a significant amount of work on developing `turboseti_stream`. Luigi also helped greatly with the structure of the flowgraph, particularly the polyphase filterbank and FFT components. Daniel Estévez and Derek Kozel answered many, many questions about GNU Radio, OOT modules, and using Python multiprocessing. Lastly, Wael Farah was very patient while helping me wade through hordes upon hordes of bugs.

Thank you all!

This project was made possible by funding from Breakthrough Listen.


### References

Theory:
- Sheikh et al. 2019, [_Choosing a Maximum Drift Rate in a SETI Search: Astrophysical Considerations_](https://arxiv.org/abs/1910.01148)

GNU Radio:
- [GNU Radio OOT Modules](https://wiki.gnuradio.org/index.php/OutOfTreeModules)
- [Types of GNU Radio Blocks](https://wiki.gnuradio.org/index.php/Types_of_Blocks)
- [Guided GNU Radio Tutorial for Python Blocks (depreciated for v3.8, but still helpful)](https://wiki.gnuradio.org/index.php/Guided_Tutorial_GNU_Radio_in_Python)
- [Using GNU Radio at the ATA](https://wiki.gnuradio.org/index.php/GNURadio@theATA)

