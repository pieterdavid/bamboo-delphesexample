import logging
logger = logging.getLogger(__name__)

from bamboo.root import loadLibrary, gbl
loadLibrary("DelphesIO/libDelphesIO.so.3.4.2")
gbl.gInterpreter.Declare('#include "delphes_helpers.h"')

class DelphesDescription:
    def __init__(self, collections=None, singletons=None):
        self.collections = collections or []
        self.singletons = singletons or []

test_phase2_descr = DelphesDescription(
        collections=["Particle", "GenJet", "WeightLHEF",
            "GenJet02", "GenJet04", "GenJet08", "GenJet15", 
            "ParticleFlowJet02", "ParticleFlowJet04", "ParticleFlowJet08", "ParticleFlowJet15", 
            "CaloJet02", "CaloJet04", "CaloJet08", "CaloJet15", 
            "TrackJet02", "TrackJet04", "TrackJet08", "TrackJet15", 
            "Track", "Tower", "EFlowTrack", "EFlowPhoton", "EFlowNeutralHadron",
            "Electron", "Jet", "Photon", "Muon"
            ],
        singletons=["Event", "EventLHEF", "GenMissingET", "MissingET", "ScalarHT"]
        )

def decorateCMSPhase2DelphesTree(aTree, isMC=True, description=None):
    """ Decorate a Delphes native tree as used for CMS Phase2 physics studies """
    from bamboo.root import gbl
    # make sure dictionaries are loaded
    try:
        gbl.HepMCEvent
    except AttributeError as ex:
        raise RuntimeError("A dictionary for the Delphes classes must be loaded to use these trees")
    aTree.GetEntry(0)
    tree_dict = {"__doc__" : "{0} tree proxy class".format(aTree.GetName())}
    branches = {br.GetName(): br for br in aTree.GetListOfBranches()}
    brForClonesArrays = set()
    from bamboo.treeproxies import TreeBaseProxy
    from bamboo.treeoperations import GetColumn
    from bamboo import treefunctions as op
    for brNm, br in branches.items():
        if isinstance(br, gbl.TBranchElement) and br.GetClassName() == "TClonesArray":
            elmType = br.GetClonesName()
            if elmType == brNm:
                elmType = f"delphes_{elmType.lower()}"
                gbl.gInterpreter.Declare(f"using {elmType} = {brNm};")
            brForClonesArrays.add(brNm)
            brForClonesArrays.add(f"{brNm}_size")
            col = GetColumn("TClonesArray", brNm)
            col_conv = op.extMethod(f"rdfhelpers::objArrayToRVec<{elmType}>",
                    returnType=f"ROOT::VecOps::RVec<{elmType}*>")(col)
            if brNm in description.singletons:
                col_conv = col_conv[0]
            elif brNm not in description.collections:
                logger.warning(f"{brNm} not specified, adding as collection")
            tree_dict[brNm] = op.defineOnFirstUse(col_conv)
    if len(branches) != len(brForClonesArrays):
        logger.warning(f"Branches not in proxy: {', '.join(br for br in branches if br not in brForClonesArrays)}")

    TreeProxy = type("{0}Proxy".format(aTree.GetName().capitalize()), (TreeBaseProxy,), tree_dict)
    return TreeProxy(aTree)

from bamboo.analysismodules import AnalysisModule, HistogramsModule

class CMSPhase2DelphesModule(AnalysisModule):
    def prepareTree(self, tree, sample=None, sampleCfg=None):
        from bamboo.dataframebackend import DataframeBackend
        t = decorateCMSPhase2DelphesTree(tree, isMC=True, description=test_phase2_descr)
        be, noSel = DataframeBackend.create(t)
        return t, noSel, be, tuple()

class CMSPhase2DelphesHistoModule(CMSPhase2DelphesModule, HistogramsModule):
    pass  # nothing to add

class DelphesTest(CMSPhase2DelphesHistoModule):
    """ Plotter module for Phase2 flat trees """
    def definePlots(self, t, noSel, sample=None, sampleCfg=None):
        from bamboo.plots import Plot, CutFlowReport
        from bamboo.plots import EquidistantBinning as EqB
        from bamboo import treefunctions as op

        plots = []

        plots.append(Plot.make1D("allPartPT", op.map(t.Electron, lambda el : el.PT), noSel, EqB(50, 0., 250.), title="All particles PT"))
        plots.append(Plot.make1D("nWeightLHEF", op.rng_len(t.WeightLHEF), noSel, EqB(10, 0., 10.), title="n WeightLHEF"))

        return plots

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from bamboo.root import loadLibrary, gbl
    f = gbl.TFile.Open("/afs/cern.ch/user/a/atalierc/public/snowmass/delphes_lhe_file_47_14TeV.lhe.root")
    tree_ = f.Get("Delphes")
    tree_.GetEntry(0)
    tree = decorateCMSPhase2DelphesTree(tree_, description=test_phase2_descr)
    import IPython
    IPython.start_ipython(argv=[], user_ns=vars())
