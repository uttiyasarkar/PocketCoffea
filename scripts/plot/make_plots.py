import os
import sys
import time
import json
import argparse

# Include PocketCoffea to python paths (needed if running from outside PocketCoffea)
PATH_TO_SCRIPT = '/'.join(sys.argv[0].split('/')[:-1])
PATH_TO_MODULE = os.path.abspath(os.path.join(os.path.abspath(PATH_TO_SCRIPT), "../.."))
if not PATH_TO_MODULE in sys.path:
    sys.path.append(PATH_TO_MODULE)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

import math
import mplhep as hep
from coffea.util import load
from coffea.hist import plot
import coffea.hist as hist

from multiprocessing import Pool
from PocketCoffea.parameters.allhistograms import histogram_settings
from PocketCoffea.parameters.lumi import lumi, femtobarn

from PocketCoffea.utils.Configurator import Configurator

parser = argparse.ArgumentParser(description='Plot histograms from coffea file')
parser.add_argument('--cfg', default=os.getcwd() + "/config/test.json", help='Config file with parameters specific to the current run', required=False)
parser.add_argument('-v', '--version', type=str, default=None, help='Version of output (e.g. `v01`, `v02`, etc.)')

args = parser.parse_args()
config = Configurator(args.cfg, plot=True, plot_version=args.version)

finalstate = config.finalstate

print("Starting ", end='')
print(time.ctime())
start = time.time()

if os.path.isfile( config.outfile ): accumulator = load(config.outfile)
else: sys.exit("Input file does not exist")

data_err_opts = {
    'linestyle': 'none',
    'marker': '.',
    'markersize': 10.,
    'color': 'k',
    'elinewidth': 1,
}

qcd_opts = {
    #'facecolor': 'None',
    'edgecolor': 'black',
    #'linestyle': '-',
    #'linewidth': 2,
    'alpha': 1.0
}

signal_opts = {
    'facecolor': 'None',
    'edgecolor': ['green', 'red'],
    'linestyle': ['--', '-'],
    'linewidth': 2,
    'alpha': 0.7
}

ggH_opts = {
    'bb' : {
        'facecolor': 'None',
        'edgecolor': 'green',
        'linestyle': '--',
        'linewidth': 2,
        'alpha': 0.7
    },
    'cc': {
        'facecolor': 'None',
        'edgecolor': 'red',
        'linestyle': '--',
        'linewidth': 2,
        'alpha': 0.7
    }
}

selection = {
    'trigger'  : (r'Trigger'),
    'dilepton_SR' : (r'Trigger'+'\n'+
                     r'Dilepton cuts'+'\n'+
                     r'SR'),
    'dilepton_CR' : (r'Trigger'+'\n'+
                     r'Dilepton cuts'+'\n'+
                     r'CR'),
    'semileptonic_SR' : (r'Trigger'+'\n'+
                     r'Semileptonic cuts'+'\n'+
                     r'SR'),
    'semileptonic_CR' : (r'Trigger'+'\n'+
                     r'Semileptonic cuts'+'\n'+
                     r'CR'),
    'semileptonic_triggerSF_Ele32_EleHT_fail' : 'Trigger fail',
    'semileptonic_triggerSF_Ele32_EleHT_pass' : 'Trigger pass',
    'semileptonic_triggerSF_inclusive' : 'Inclusive',
}

plt.style.use([hep.style.ROOT, {'font.size': 16}])
if not os.path.exists(config.plots):
    os.makedirs(config.plots)

def make_plots(entrystart, entrystop):
    _accumulator = dict( [(key, value) for key, value in accumulator.items() if key.startswith('hist_')][entrystart:entrystop] )
    for histname in _accumulator:
        if config.plot_options["only"] and not (config.plot_options["only"] in histname): continue
        if not histname.startswith('hist_'): continue
        variable = histname.split('hist_')[1]
        print(histname, variable)
        if not variable.startswith(tuple(config.variables)): continue
        h = _accumulator[histname]

        for year in [str(s) for s in h.identifiers('year')]:
            # Convert lumi in fb^-1 and round to the first decimal digit
            totalLumi = femtobarn(lumi[year], digits=1)
            for cat in [str(s) for s in h.identifiers('cat')]:
                key = '_'.join([finalstate, cat])
                if key not in selection:
                    selection_text = cat
                else:
                    selection_text = selection[key]
                samples = [str(s) for s in h.identifiers('sample')]
                varname = h.fields[-1]
                varlabel = h.axis(varname).label
                # This if has to be rewritten!
                #if histname.lstrip('hist_').startswith( tuple(histogram_settings['variables'].keys()) ):
                #    h = h.rebin(varname, hist.Bin(varname, varlabel, **histogram_settings['variables']['_'.join(histname.split('_')[:2])]['binning']))
                #h.scale( scaleXS, axis='sample' )

                if not 'hist2d' in histname:

                    if variable in config.plot_options["rebin"].keys():
                        print(f"Rebinning {histname}")
                        h = h.rebin(h.dense_axes()[0], hist.Bin(h.dense_axes()[0].name, config.plot_options["rebin"][variable]['xlabel'], **config.plot_options["rebin"][variable]["binning"]))

                    fig, (ax, rax) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={"height_ratios": (3, 1)}, sharex=True)
                    fig.subplots_adjust(hspace=.07)
                    if len(h.axes()) > 4:
                        #categories_to_sum_over = ['cat', 'year', 'flavor']
                        categories_to_sum_over = config.plot_options["sum_over"]
                        sparse_axis = [axis.name for axis in h.sparse_axes() if not axis.name in config.plot_options["sum_over"]][0]
                        samples_data = list(filter(lambda x : 'DATA' in x, samples))
                        samples_qcd  = list(filter(lambda x : 'QCD' in x, samples))
                        plot.plot1d(h[(samples_qcd, cat, year)].sum(*categories_to_sum_over), ax=ax, fill_opts=qcd_opts, legend_opts={'loc':1}, stack=True)
                        plot.plot1d(h[(samples_data, cat, year)].sum(*categories_to_sum_over), ax=ax, error_opts=data_err_opts, legend_opts={'loc':1}, clear=False)
                        plot.plotratio(num=h[(samples_data, cat, year)].sum(*categories_to_sum_over, sparse_axis), denom=h[(samples_qcd, cat, year)].sum(*categories_to_sum_over, sparse_axis), ax=rax,
                                   error_opts=data_err_opts, denom_fill_opts={}, guide_opts={}, unc='num')
                        maxY = 1.2 *max( [ max(h[(s, cat, year)].sum(*categories_to_sum_over, sparse_axis).values()[()]) for s in [samples_qcd, samples_data]] )
                    else:
                        #categories_to_sum_over = ['cat', 'year']
                        categories_to_sum_over = config.plot_options["sum_over"]
                        plot.plot1d(h[(samples, cat, year)].sum(*categories_to_sum_over), ax=ax, legend_opts={'loc':1})
                        maxY = 1.2 *max( [ max(h[(sample, cat, year)].sum(*categories_to_sum_over).values()[(sample,)]) for sample in samples] )

                    hep.cms.text("Preliminary", ax=ax)
                    hep.cms.lumitext(text=f'{totalLumi}' + r' fb$^{-1}$, 13 TeV,' + f' {year}', fontsize=18, ax=ax)
                    ax.legend()
                    at = AnchoredText(selection_text, loc=2, frameon=False)
                    ax.add_artist(at)
                    ax.set_xlim(*config.variables[variable]['xlim'])
                    ax.set_ylim(0,maxY)
                    rax.set_ylim(0,2)
                    rax.set_ylabel("data/MC")

                    if histname.lstrip('hist_').startswith( tuple(histogram_settings['variables'].keys()) ):
                        if histname == 'hist_bquark_drMatchedJet':
                            ax.set_xlim(0,1)
                        elif histname == 'hist_bquark_pt':
                            ax.set_xlim(0,200)
                        #ax.set_xlim(**histogram_settings['variables']['_'.join(histname.lstrip('hist_').split('_')[:2])]['xlim'])
                    filepath = os.path.join(config.plots, f"{histname}_{finalstate}_{cat}_{year}.png")
                    if config.plot_options["scale"] == 'log':
                        ax.semilogy()
                        exp_high = 2 + math.floor(math.log(maxY, 10))
                        exp_low = -4
                        ax.set_ylim(10**exp_low, 10**exp_high)
                        #rax.set_ylim(0.1,10)
                        filepath = filepath.replace(".png", "_" + config.plot_options["scale"] + ".png")
                    print("Saving", filepath)
                    plt.savefig(filepath, dpi=300, format="png")
                    plt.close(fig)

    return

HistsToPlot = [k for k in accumulator.keys() if 'hist' in k]
NtotHists = len(HistsToPlot)
NHistsToPlot = len([key for key in HistsToPlot if config.only in key])
print("# tot histograms = ", NtotHists)
print("# histograms to plot = ", NHistsToPlot)
print("Histograms to plot:", HistsToPlot)
delimiters = np.linspace(0, NtotHists, config.plot_options['workers'] + 1).astype(int)
chunks = [(delimiters[i], delimiters[i+1]) for i in range(len(delimiters[:-1]))]
pool = Pool()
pool.starmap(make_plots, chunks)
pool.close()

end = time.time()
runTime = round(end-start)
print("Finishing ", end='')
print(time.ctime())
print(f"Drawn {NHistsToPlot} plots in {runTime} s")
