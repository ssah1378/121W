import ROOT

# Open the background file and print the number of events in contains

bkg = ROOT.TFile.Open('/Users/shasha/Downloads/4lep/MC/mc_363490.llll.4lep.root')
t_bkg = bkg.Get('mini')
t_bkg.GetEntries()

# Create a TChain to combine the signal files, and print the total number of signal events (Higgs decays)

sig = ROOT.TChain('mini')
sig.Add('/Users/shasha/Downloads/4lep/MC/mc_344235.VBFH125_ZZ4lep.4lep.root')
sig.Add('/Users/shasha/Downloads/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root')
sig.GetEntries()

# Create background histogram

h_c30_bgs = ROOT.TH1F('h_c30_bgs','Transverse momentum; lep_pt (GeV); Events/bin',20,0,200)

# Create signal histogram

h_c30_sig = ROOT.TH1F('h_c30_sig','Transverse momentum; lep_pt (GeV); Events/bin',20,0,200)

# Fill the background histogram

n=0
for event in t_bkg:
    n += 1
    ## printing the evolution in number of events
    if(n%10000==0):
        print(n)
    
    if (t_bkg.trigE==True) or (t_bkg.trigM==True):
        if (sum(t_bkg.lep_type)==44) or (sum(t_bkg.lep_type)==48) or (sum(t_bkg.lep_type)==52):
            if (sum(t_bkg.lep_charge)==0):
                for i in range(t_bkg.lep_n):        
                    if (abs(t_bkg.lep_eta[i])<2.5) and ((t_bkg.lep_ptcone30[i])/(t_bkg.lep_pt[i])<0.3) and ((t_bkg.lep_etcone20[i])/(t_bkg.lep_pt[i])<0.3):                     
                        h_c30_bgs.Fill(t_bkg.lep_pt[i]/1000)


# Fill the signal histogram

m=0
for event in sig:
    m += 1
    ## printing the evolution in number of events
    if(m%10000==0):
        print(m)
    
    if (sig.trigE==True) or (sig.trigM==True):
        if (sum(sig.lep_type)==44) or (sum(sig.lep_type)==48) or (sum(sig.lep_type)==52):
            if (sum(sig.lep_charge)==0):
                for i in range(sig.lep_n):       
                    if (abs(sig.lep_eta[i])<2.5) and ((sig.lep_ptcone30[i])/(sig.lep_pt[i])<0.3) and ((sig.lep_etcone20[i])/(sig.lep_pt[i])<0.3):                     
                        h_c30_sig.Fill(sig.lep_pt[i]/1000)                        


# Normalize all histograms to 1

norm_c30_bgs = h_c30_bgs.Integral()
h_c30_bgs.Scale(1.0/norm_c30_bgs)
norm_c30_sig = h_c30_sig.Integral()
h_c30_sig.Scale(1.0/norm_c30_sig)

# Aesthetics
h_c30_sig.SetFillStyle(3003)
h_c30_sig.SetFillColor(2)
h_c30_sig.SetLineColor(2)
h_c30_sig.SetStats(0)       #<--- removing the stats box

h_c30_bgs.SetFillStyle(3001)
h_c30_bgs.SetFillColor(4)
h_c30_bgs.SetLineColor(4)
h_c30_bgs.SetStats(0)


#  Create Legend
leg = ROOT.TLegend(0.5,0.7,0.9,0.9);
leg.AddEntry(h_c30_sig, "Signal (H #rightarrow ZZ)", "f");
leg.AddEntry(h_c30_bgs, "Background (ZZ)", "f");

# Create a TCanvas to contain each pair of histograms

c1 = ROOT.TCanvas("c30Canvas","lep_pt Canvas",800,600)

# Draw the c30 plots overlain

h_c30_sig.Draw("HIST")
h_c30_bgs.Draw("HIST SAME")
leg.Draw()
c1.Draw()

c1.Print("lep_pt.png")

print("Hit enter to continue")
input()
