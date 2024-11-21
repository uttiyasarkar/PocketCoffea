# This config has been generated by the pocket_coffea CLI 0.9.4.
from pocket_coffea.utils.configurator import Configurator
from pocket_coffea.lib.cut_definition import Cut
from pocket_coffea.lib.cut_functions import get_nObj_min, get_nObj_eq, get_HLTsel, get_nPVgood, goldenJson, eventFlags
from pocket_coffea.parameters.cuts import passthrough
from pocket_coffea.parameters.histograms import *
from pocket_coffea.lib.categorization import StandardSelection, CartesianSelection, MultiCut

import workflow
from workflow import BasicProcessor

# Register custom modules in cloudpickle to propagate them to dask workers
import cloudpickle
import custom_cut_functions
cloudpickle.register_pickle_by_value(workflow)
cloudpickle.register_pickle_by_value(custom_cut_functions)

from custom_cut_functions import *
import os
localdir = os.path.dirname(os.path.abspath(__file__))

# Creating weights configuration
from pocket_coffea.lib.weights.common import common_weights

# Loading default parameters
from pocket_coffea.parameters import defaults
default_parameters = defaults.get_default_parameters()
defaults.register_configuration_dir("config_dir", localdir+"/params")

parameters = defaults.merge_parameters_from_files(default_parameters,
                                                    f"{localdir}/params/object_preselection.yaml",
                                                    f"{localdir}/params/triggers.yaml",
                                                   update=True)

#Creating custom weight
from pocket_coffea.lib.weights.weights import WeightLambda
import numpy as np



cfg = Configurator(
    parameters = parameters,
    datasets = {
        "jsons": ['datasets/datasets_cern.json'],
        "filter" : {
            "samples": ['TTTo2L2Nu', "DATA_SingleMuon"
                        #, "DATA_SingleEle"
                        ],
            "samples_exclude" : [],
            "year": ['2018']
        },
        "subsamples": {
            "TTTo2L2Nu": {
                "ele": [get_nObj_min(1, coll="ElectronGood"), get_nObj_eq(0, coll="MuonGood")],
                "mu":  [get_nObj_eq(0, coll="ElectronGood"), get_nObj_min(1, coll="MuonGood")],
            },
            "DATA_SingleMuon": {
                "clean": [get_HLTsel(primaryDatasets=["SingleEle"], invert=True)], # crosscleaning SingleELe trigger on SIngleMuon
            }
        }
    },

    workflow = BasicProcessor,

    skim = [get_nPVgood(1), eventFlags, goldenJson,
            get_HLTsel(primaryDatasets=["SingleMuon", "SingleEle"])], 

    preselections = [passthrough],
    categories = {
        "baseline": [passthrough],
        "1btag": [get_nObj_min(1, coll="BJetGood")],
        "2btag": [get_nObj_min(2, coll="BJetGood")],
    },

    weights = {
        "common": {
            "inclusive": ["genWeight","lumi","XS","pileup",
                          "sf_ele_id","sf_ele_reco",
                          "sf_mu_id","sf_mu_iso"
                          ],
            "bycategory": {
                "1btag": ["sf_btag"],
                "2btag": ["sf_btag"],
            },
       },
        "bysample": {
        }
    },
    # Passing a list of WeightWrapper objects
    weights_classes = common_weights,

    variations = {
        "weights": {
            "common": {
                "inclusive": [ "pileup",
                               "sf_ele_id", "sf_ele_reco",
                               "sf_mu_id", "sf_mu_iso",
                               ],
                "bycategory" : {
                    "1btag": ["sf_btag"],
                    "2btag": ["sf_btag"],
                }
            },
            "bysample": {
            }
        },
        "shape": {
            "common": {
                "inclusive": [ "JES_Total_AK4PFchs"],
                "bycategory": {
                    "1btag": ["JER_AK4PFchs"]
                }
            },
        }
    },

    variables = {
        **ele_hists(),
        **jet_hists(),
        **count_hist("JetGood"),
        **count_hist("BJetGood"),
    },

    columns = {

    },
)
