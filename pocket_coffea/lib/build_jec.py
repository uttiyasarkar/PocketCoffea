'''
Nice code to build the JEC/JER and JES uncertainties taken from
https://github.com/andrzejnovak/boostedhiggs/blob/master/boostedhiggs/build_jec.py
'''

import importlib.resources
import contextlib
from coffea.lookup_tools import extractor
from coffea.jetmet_tools import JECStack, CorrectedJetsFactory, CorrectedMETFactory

jec_name_map = {
    'JetPt': 'pt',
    'JetMass': 'mass',
    'JetEta': 'eta',
    'JetA': 'area',
    'ptGenJet': 'pt_gen',
    'ptRaw': 'pt_raw',
    'massRaw': 'mass_raw',
    'Rho': 'event_rho',
    'METpt': 'pt',
    'METphi': 'phi',
    'JetPhi': 'phi',
    'UnClusteredEnergyDeltaX': 'MetUnclustEnUpDeltaX',
    'UnClusteredEnergyDeltaY': 'MetUnclustEnUpDeltaY',
}


def jet_factory_factory(files):
    ext = extractor()
    with contextlib.ExitStack() as stack:
        # this would work even in zipballs but since extractor keys on file extension and
        # importlib make a random tempfile, it won't work. coffea needs to enable specifying the type manually
        # for now we run this whole module as $ python -m boostedhiggs.build_jec boostedhiggs/data/jec_compiled.pkl.gz
        # so the compiled value can be loaded using the importlib tool in corrections.py
        real_files = [stack.enter_context(importlib.resources.path("pocket_coffea.parameters.jec", f)) for f in files]
        ext.add_weight_sets([f"* * {file}" for file in real_files])
        ext.finalize()

    jec_stack = JECStack(ext.make_evaluator())
    return CorrectedJetsFactory(jec_name_map, jec_stack)


jet_factory = {
    "2016_PreVFP": jet_factory_factory(
        files=[
            "Summer19UL16APV_V7_MC_L1FastJet_AK4PFchs.jec.txt.gz",
            "Summer19UL16APV_V7_MC_L2Relative_AK4PFchs.jec.txt.gz",
            "RegroupedV2_Summer19UL16APV_V7_MC_UncertaintySources_AK4PFchs.junc.txt.gz",
            "Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.junc.txt.gz",
            "Summer20UL16_JRV3_MC_PtResolution_AK4PFchs.jr.txt.gz",
            "Summer20UL16_JRV3_MC_SF_AK4PFchs.jersf.txt.gz",
        ]
    ),
    # "2016mcNOJER": jet_factory_factory(
    #     files=[
    #         "Summer19UL16APV_V7_MC_L1FastJet_AK4PFchs.jec.txt.gz",
    #         "Summer19UL16APV_V7_MC_L2Relative_AK4PFchs.jec.txt.gz",
    #         "Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.junc.txt.gz",
    #     ]
    # ),
    # "2017mc": jet_factory_factory(
    #     files=[
    #         # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Fall17_17Nov2017_V32_MC/Fall17_17Nov2017_V32_MC_L1FastJet_AK4PFchs.txt
    #         "Fall17_17Nov2017_V32_MC_L1FastJet_AK4PFchs.jec.txt.gz",
    #         # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Fall17_17Nov2017_V32_MC/Fall17_17Nov2017_V32_MC_L2Relative_AK4PFchs.txt
    #         "Fall17_17Nov2017_V32_MC_L2Relative_AK4PFchs.jec.txt.gz",
    #         # https://raw.githubusercontent.com/cms-jet/JECDatabase/master/textFiles/Fall17_17Nov2017_V32_MC/RegroupedV2_Fall17_17Nov2017_V32_MC_UncertaintySources_AK4PFchs.txt
    #         "RegroupedV2_Fall17_17Nov2017_V32_MC_UncertaintySources_AK4PFchs.junc.txt.gz",
    #         # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Fall17_17Nov2017_V32_MC/Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFchs.txt
    #         "Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFchs.junc.txt.gz",
    #         # https://github.com/cms-jet/JRDatabase/raw/master/textFiles/Fall17_V3b_MC/Fall17_V3b_MC_PtResolution_AK4PFchs.txt
    #         "Fall17_V3b_MC_PtResolution_AK4PFchs.jr.txt.gz",
    #         # https://github.com/cms-jet/JRDatabase/raw/master/textFiles/Fall17_V3b_MC/Fall17_V3b_MC_SF_AK4PFchs.txt
    #         "Fall17_V3b_MC_SF_AK4PFchs.jersf.txt.gz",
    #     ]
    # ),
    # "2017mcNOJER": jet_factory_factory(
    #     files=[
    #         "Fall17_17Nov2017_V32_MC_L1FastJet_AK4PFchs.jec.txt.gz",
    #         "Fall17_17Nov2017_V32_MC_L2Relative_AK4PFchs.jec.txt.gz",
    #         "Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFchs.junc.txt.gz",
    #     ]
    # ),
    "2018": jet_factory_factory(
        files=[
            "Summer19UL18_V5_MC_L1FastJet_AK4PFchs.jec.txt.gz",
            "Summer19UL18_V5_MC_L2Relative_AK4PFchs.jec.txt.gz",
            "RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.junc.txt.gz",
            "Summer19UL18_V5_MC_Uncertainty_AK4PFchs.junc.txt.gz",
            "Summer19UL18_JRV2_MC_PtResolution_AK4PFchs.jr.txt.gz",
            "Summer19UL18_JRV2_MC_SF_AK4PFchs.jersf.txt.gz",
        ]
    ),
    "2018_NOJER": jet_factory_factory(
        files=[
            "Summer19UL18_V5_MC_L1FastJet_AK4PFchs.jec.txt.gz",
            "Summer19UL18_V5_MC_L2Relative_AK4PFchs.jec.txt.gz",
            "RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.junc.txt.gz",
        ]
    ),
}

fatjet_factory = {
#     "2016mc": jet_factory_factory(
#         files=[
#             # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16_V7_MC/Summer19UL16_V7_MC_L1FastJet_AK8PFPuppi.txt
#             "Summer19UL16_V7_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
#             # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16_V7_MC/Summer19UL16_V7_MC_L2Relative_AK8PFPuppi.txt
#             "Summer19UL16_V7_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
#             # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16_V7_MC/Summer19UL16_V7_MC_UncertaintySources_AK8PFPuppi.txt
#             "Summer19UL16_V7_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
#             # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16_V7_MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt
#             "Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
#             # https://github.com/cms-jet/JRDatabase/raw/master/textFiles/Summer16_25nsV1b_MC/Summer16_25nsV1b_MC_PtResolution_AK8PFPuppi.txt
#             "Summer16_25nsV1b_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
#             # https://github.com/cms-jet/JRDatabase/raw/master/textFiles/Summer16_25nsV1b_MC/Summer16_25nsV1b_MC_SF_AK8PFPuppi.txt
#             "Summer16_25nsV1b_MC_SF_AK8PFPuppi.jersf.txt.gz",
#         ]
#     ),
#     "2016mcNOJER": jet_factory_factory(
#         files=[
#             "Summer19UL16_V7_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
#             "Summer19UL16_V7_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
#             "Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
#         ]
#     ),
#     "2017mc": jet_factory_factory(
#         files=[
#             # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Fall17_17Nov2017_V32_MC/Fall17_17Nov2017_V32_MC_L1FastJet_AK8PFPuppi.txt
#             "Fall17_17Nov2017_V32_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
#             # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Fall17_17Nov2017_V32_MC/Fall17_17Nov2017_V32_MC_L2Relative_AK8PFPuppi.txt
#             "Fall17_17Nov2017_V32_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
#             # https://raw.githubusercontent.com/cms-jet/JECDatabase/master/textFiles/Fall17_17Nov2017_V32_MC/Fall17_17Nov2017_V32_MC_UncertaintySources_AK8PFPuppi.txt
#             "Fall17_17Nov2017_V32_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
#             # https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Fall17_17Nov2017_V32_MC/Fall17_17Nov2017_V32_MC_Uncertainty_AK8PFPuppi.txt
#             "Fall17_17Nov2017_V32_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
#             # https://github.com/cms-jet/JRDatabase/raw/master/textFiles/Fall17_V3b_MC/Fall17_V3b_MC_PtResolution_AK8PFPuppi.txt
#             "Fall17_V3b_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
#             # https://github.com/cms-jet/JRDatabase/raw/master/textFiles/Fall17_V3b_MC/Fall17_V3b_MC_SF_AK8PFPuppi.txt
#             "Fall17_V3b_MC_SF_AK8PFPuppi.jersf.txt.gz",
#         ]
#     ),
#     "2017mcNOJER": jet_factory_factory(
#         files=[
#             "Fall17_17Nov2017_V32_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
#             "Fall17_17Nov2017_V32_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
#             "Fall17_17Nov2017_V32_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
#         ]
#     ),
     "2018": jet_factory_factory(
         files=[
             "Summer19UL18_V5_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
             "Summer19UL18_V5_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
             "Summer19UL18_V5_MC_UncertaintySources_AK8PFPuppi.junc.txt.gz",
             "Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
             "Summer19UL18_JRV2_MC_PtResolution_AK8PFPuppi.jr.txt.gz",
             "Summer19UL18_JRV2_MC_SF_AK8PFPuppi.jersf.txt.gz",
         ]
     ),
     "2018_NOJER": jet_factory_factory(
         files=[
             "Summer19UL18_V5_MC_L1FastJet_AK8PFPuppi.jec.txt.gz",
             "Summer19UL18_V5_MC_L2Relative_AK8PFPuppi.jec.txt.gz",
             "Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.junc.txt.gz",
         ]
     ),
}

met_factory = CorrectedMETFactory(jec_name_map)

if __name__ == "__main__":
    import sys
    import gzip
    # jme stuff not pickleable in coffea
    import cloudpickle

    with gzip.open(sys.argv[-1], "wb") as fout:
        cloudpickle.dump(
            {
                "jet_factory": jet_factory,
                "fatjet_factory": fatjet_factory,
                "met_factory": met_factory,
            },
            fout
        )
