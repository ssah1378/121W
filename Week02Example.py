import ROOT

# Open the background file and print the number of events it contains

bkg = ROOT.TFile.Open("/Users/shasha/Downloads/4lep/MC/mc_363490.llll.4lep.root")
t_bkg = bkg.Get("mini")
t_bkg.GetEntries()

# Create a TChain to combine the signal files, and print the total number of signal events (Higgs decays)

sig = ROOT.TChain("mini")
sig.Add("/Users/shasha/Downloads/4lep/MC/mc_344235.VBFH125_ZZ4lep.4lep.root")
sig.Add("/Users/shasha/Downloads/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root")
sig.GetEntries()

# Create background histograms

h_met_bgs = ROOT.TH1F("h_met_bgs","Example plot: Missing Transverse Energy; Missing E_{T} (GeV); Events/bin",20,0,200)
h_njet_bgs = ROOT.TH1F("h_njet_bgs","Example plot: Number of Jets; n_{jets}; Events/bin",10,0,10)

# Create signal histograms

h_met_sig = ROOT.TH1F("h_met_sig","Example plot: Missing Transverse Energy; Missing E_{T} (GeV); Events/bin",20,0,200)
h_njet_sig = ROOT.TH1F("h_njet_sig","Example plot: Number of Jets; n_{jets}; Events/bin",10,0,10)

# Fill the background histograms

n=0
for event in t_bkg:
    n += 1
    ## printing the evolution in number of events
    if(n%10000==0):
        print(n)
    h_met_bgs.Fill(t_bkg.met_et/1000.)
    h_njet_bgs.Fill(t_bkg.jet_n)
    
# Fill the signal histograms

m=0 
for event in sig:
    m += 1
    ## printing the evolution in number of events
    if(m%10000==0):
        print(m)
    h_met_sig.Fill((sig.met_et)/1000.)
    h_njet_sig.Fill(sig.jet_n)

# Normalize all histograms to 1

norm_met_bgs = h_met_bgs.Integral()
h_met_bgs.Scale(1.0/norm_met_bgs)
norm_njet_bgs = h_njet_bgs.Integral()
h_njet_bgs.Scale(1.0/norm_njet_bgs)
norm_met_sig = h_met_sig.Integral()
h_met_sig.Scale(1.0/norm_met_sig)
norm_njet_sig = h_njet_sig.Integral()
h_njet_sig.Scale(1.0/norm_njet_sig)

# Aesthetics
h_met_sig.SetFillStyle(3003)
h_met_sig.SetFillColor(2)
h_met_sig.SetLineColor(2)
h_met_sig.SetStats(0)       #<--- removing the stats box

h_met_bgs.SetFillStyle(3001)
h_met_bgs.SetFillColor(4)
h_met_bgs.SetLineColor(4)
h_met_bgs.SetStats(0)

h_njet_sig.SetFillStyle(3003)
h_njet_sig.SetFillColor(2)
h_njet_sig.SetLineColor(2)
h_njet_sig.SetStats(0)      #<--- removing the stats box

h_njet_bgs.SetFillStyle(3001)
h_njet_bgs.SetFillColor(4)
h_njet_bgs.SetLineColor(4)
h_njet_bgs.SetStats(0)

#  Create Legend
leg = ROOT.TLegend(0.5,0.7,0.9,0.9);
leg.AddEntry(h_met_sig, "Signal (H #rightarrow ZZ)", "f");
leg.AddEntry(h_met_bgs, "Background (ZZ)", "f");

# Create a TCanvas to contain each pair of histograms

c1 = ROOT.TCanvas("metCanvas","E_T Canvas",800,600)

# Draw the E_T plots overlain

h_met_sig.Draw("HIST")
h_met_bgs.Draw("HIST SAME")
leg.Draw()
c1.Draw()

c1.Print("EtPlot.png")

print("Hit enter to continue")
input()

c1.Close()
c2 = ROOT.TCanvas("njetsCanvas", "n_jets Canvas",800,600)

h_njet_sig.Draw("HIST")
h_njet_bgs.Draw("HIST SAME")
leg.Draw()
c2.Draw()

c2.Print("NjetsPlot.png")

print("Hit enter to continue")
input()
