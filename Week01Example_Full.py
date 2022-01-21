import ROOT


# Create TChain

chain_data = ROOT.TChain("mini");
chain_data.Add("e:/data/4lep/Data/data_A.4lep.root")
chain_data.Add("e:/data/4lep/Data/data_B.4lep.root")
chain_data.Add("e:/data/4lep/Data/data_C.4lep.root")
chain_data.Add("e:/data/4lep/Data/data_D.4lep.root")

total_entries = chain_data.GetEntries()
print ("The chain has a total of ", total_entries, " entries")

# Create histograms
h_ptGeVe_pos = ROOT.TH1F("ptGeVe_pos","Positron spectrum; Transverse momentum (GeV); Entries/5 GeV",20,0,100)
h_ptGeVe_neg = ROOT.TH1F("ptGeVe_neg","Electron spectrum; Transverse momentum (GeV); Entries/5 GeV",20,0,100)
h_ptGeVm_pos = ROOT.TH1F("ptGeVm_pos","Muon+ spectrum; Transverse momentum (GeV); Entries/5 GeV",20,0,100)
h_ptGeVm_neg = ROOT.TH1F("ptGeVm_neg","Muon- spectrum; Transverse momentum (GeV); Entries/5 GeV",20,0,100)
  
# Loop over entries and fill histogram

n = 0
for event in chain_data:
    n += 1
    if(n%100==0) :
      print(n)
    for i in range(chain_data.lep_n):
      if (chain_data.lep_type[i] == 11) :
        if (chain_data.lep_charge[i] == 1) :
            h_ptGeVe_pos.Fill(chain_data.lep_pt[i]/1000)
        elif (chain_data.lep_charge[i]== -1) : 
            h_ptGeVe_neg.Fill(chain_data.lep_pt[i]/1000)
      elif (chain_data.lep_type[i] == 13) :
        if (chain_data.lep_charge[i] == 1) :
            h_ptGeVm_pos.Fill(chain_data.lep_pt[i]/1000)
        elif (chain_data.lep_charge[i] == -1) :
            h_ptGeVm_neg.Fill(chain_data.lep_pt[i]/1000)

# Aesthetics
  
h_ptGeVe_pos.SetFillColor(ROOT.kRed)
h_ptGeVm_pos.SetFillColor(ROOT.kBlue)
h_ptGeVe_neg.SetFillColor(ROOT.kRed-2)
h_ptGeVm_neg.SetFillColor(ROOT.kBlue-2)
  
# Draw histograms

can = ROOT.TCanvas("can","Overlayed spectra")
can.cd()

# Create Stacked histogram and add the basic histograms to it

hs = ROOT.THStack("hs","Lepton spectra; Transverse momentum (Gev); Leptons/5 GeV")
hs.Add(h_ptGeVe_pos)
hs.Add(h_ptGeVe_neg)
hs.Add(h_ptGeVm_pos)
hs.Add(h_ptGeVm_neg)
hs.Draw()

leg = ROOT.TLegend(0.5,0.7,0.9,0.9)
leg.AddEntry(h_ptGeVe_pos,"Positive electrons","f")
leg.AddEntry(h_ptGeVe_neg,"Negative electrons","f")
leg.AddEntry(h_ptGeVm_pos,"Positive muons","f")
leg.AddEntry(h_ptGeVm_neg,"Negative muons","f")
leg.Draw()

can.Draw()
can.Print("Week01.png")

print("Hit Enter to continue")
input()