import ROOT
import numpy as np

# Open the background file and print the number of events in contains

bgs = ROOT.TFile.Open('/Users/shasha/Desktop/Physics 121W/4lep/MC/mc_363490.llll.4lep.root')
c_bgs = bgs.Get('mini')
c_bgs.GetEntries()

# Create a TChain to combine the signal files, and print the total number of signal events (Higgs decays)

c_sig = ROOT.TChain('mini')
c_sig.Add('/Users/shasha/Desktop/Physics 121W/4lep/MC/mc_344235.VBFH125_ZZ4lep.4lep.root')
c_sig.Add('/Users/shasha/Desktop/Physics 121W/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root')
c_sig.GetEntries()

# Create background histogram

h_e_bgs = ROOT.TH1F('h_e_bgs','Electron pair; Mass (MeV); Events/bin',50,0,50)
h_m_bgs = ROOT.TH1F('h_m_bgs','Muon pair; Mass (MeV); Events/bin',50,0,500)
h_em_bgs = ROOT.TH1F('h_m_bgs','Electron and Muon pair; Mass (MeV); Events/bin',50,0,500)

# Create background histogram

h_e_sig = ROOT.TH1F('h_e_sig','Electron pair; Mass (MeV); Events/bin',50,0,50)
h_m_sig = ROOT.TH1F('h_m_sig','Muon pair; Mass (MeV); Events/bin',50,0,500)
h_em_sig = ROOT.TH1F('h_m_bgs','Electron and Muon pair; Mass (MeV); Events/bin',50,0,500)

# Fill the background histogram

n = 0
for event in c_bgs:
    n += 1
    ## printing the evolution in number of events
    if(n%10000==0):
        print(n)
    # Check trigger requirement
    if (not (c_bgs.trigE or c_bgs.trigM) ):
        continue
    # lists to record good leptons of each type
    goodEPlus = []
    goodEMinus = []
    goodMuPlus = []
    goodMuMinus = []
    for ilep in range(c_bgs.lep_n):
        if (abs(c_bgs.lep_eta[ilep]) < 2.5 and
            c_bgs.lep_ptcone30[ilep]/c_bgs.lep_pt[ilep] < 0.3 and
            c_bgs.lep_etcone20[ilep]/c_bgs.lep_pt[ilep] < 0.3):
            # Passes lepton selection; store in appropriate list
            if (c_bgs.lep_type[ilep] == 11):
                if (c_bgs.lep_charge[ilep] > 0):
                    goodEPlus += [ilep]
                else:
                    goodEMinus += [ilep]
            if (c_bgs.lep_type[ilep] == 13):
                if (c_bgs.lep_charge[ilep] > 0):
                    goodMuPlus += [ilep]
                else:
                    goodMuMinus += [ilep]
    # Count good leptons
    if (len(goodEPlus) + len(goodEMinus) == 2) and (len(goodEPlus) == len(goodEMinus)):
        group1 = goodEPlus + goodEMinus 
        theta = 2*np.arctan(np.exp(-c_bgs.lep_eta[group1[0]]))
        theta1 = 2*np.arctan(np.exp(-c_bgs.lep_eta[group1[1]]))
        sin = np.sin(theta)
        sin1 = np.sin(theta1)
        lep_pe = c_bgs.lep_pt[group1[0]]/sin
        lep_pe1 = c_bgs.lep_pt[group1[1]]/sin1
        h_e_bgs.Fill( ( (c_bgs.lep_E[group1[0]]+c_bgs.lep_E[group1[1]])**2 - (lep_pe+lep_pe1)**2 )**0.5)
    
    if (len(goodMuPlus) + len(goodMuMinus) == 2) and (len(goodMuPlus) == len(goodMuMinus)):
        group2 = goodMuPlus + goodMuMinus
        theta = 2*np.arctan(np.exp(-c_bgs.lep_eta[group2[0]]))
        theta1 = 2*np.arctan(np.exp(-c_bgs.lep_eta[group2[1]]))
        sin = np.sin(theta)
        sin1 = np.sin(theta1)
        lep_pm = c_bgs.lep_pt[group2[0]]/sin
        lep_pm1 = c_bgs.lep_pt[group2[1]]/sin1
        h_m_bgs.Fill( ((c_bgs.lep_E[group2[0]]+c_bgs.lep_E[group2[1]])**2 - (lep_pm+lep_pm1)**2)**0.5)
        
    if (len(goodEPlus) + len(goodEMinus) == 2) and (len(goodEPlus) == len(goodEMinus)) and (len(goodMuPlus) + len(goodMuMinus) == 2) and (len(goodMuPlus) == len(goodMuMinus)):
        group3 = goodEPlus + goodEMinus + goodMuPlus + goodMuMinus
        h_em_bgs.Fill( ((c_bgs.lep_E[group1[0]]+c_bgs.lep_E[group1[1]]+c_bgs.lep_E[group2[0]]+c_bgs.lep_E[group2[1]])**2
                        -(lep_pe+lep_pe1+lep_pm+lep_pm1)**2)**0.5)


# Fill the signal histogram 

m = 0
for event in c_sig:
    m += 1
    ## printing the evolution in number of events
    if(m%10000==0):
        print(m)
    # Check trigger requirement
    if (not (c_sig.trigE or c_sig.trigM) ):
        continue
    # lists to record good leptons of each type
    goodEPlus = []
    goodEMinus = []
    goodMuPlus = []
    goodMuMinus = []
    for ilep in range(c_sig.lep_n):
        if (abs(c_sig.lep_eta[ilep]) < 2.5 and
            c_sig.lep_ptcone30[ilep]/c_sig.lep_pt[ilep] < 0.3 and
            c_sig.lep_etcone20[ilep]/c_sig.lep_pt[ilep] < 0.3):
            # Passes lepton selection; store in appropriate list
            if (c_sig.lep_type[ilep] == 11):
                if (c_sig.lep_charge[ilep] > 0):
                    goodEPlus += [ilep]
                else:
                    goodEMinus += [ilep]
            if (c_sig.lep_type[ilep] == 13):
                if (c_sig.lep_charge[ilep] > 0):
                    goodMuPlus += [ilep]
                else:
                    goodMuMinus += [ilep]
    # Count good leptons
    if (len(goodEPlus) + len(goodEMinus) == 2) and (len(goodEPlus) == len(goodEMinus)):
        group1 = goodEPlus + goodEMinus 
        theta = 2*np.arctan(np.exp(-c_sig.lep_eta[group1[0]]))
        theta1 = 2*np.arctan(np.exp(-c_sig.lep_eta[group1[1]]))
        sin = np.sin(theta)
        sin1 = np.sin(theta1)
        lep_pe = c_sig.lep_pt[group1[0]]/sin
        lep_pe1 = c_sig.lep_pt[group1[1]]/sin1
        h_e_sig.Fill( ((c_sig.lep_E[group1[0]]+c_sig.lep_E[group1[1]])**2 - (lep_pe+lep_pe1)**2)**0.5)
    
    if (len(goodMuPlus) + len(goodMuMinus) == 2) and (len(goodMuPlus) == len(goodMuMinus)):
        group2 = goodMuPlus + goodMuMinus
        theta = 2*np.arctan(np.exp(-c_sig.lep_eta[group2[0]]))
        theta1 = 2*np.arctan(np.exp(-c_sig.lep_eta[group2[1]]))
        sin = np.sin(theta)
        sin1 = np.sin(theta1)
        lep_pm = c_sig.lep_pt[group2[0]]/sin
        lep_pm1 = c_sig.lep_pt[group2[1]]/sin1
        h_m_sig.Fill( ((c_sig.lep_E[group2[0]]+c_sig.lep_E[group2[1]])**2 - (lep_pm+lep_pm1)**2)**0.5)
        
    if (len(goodEPlus) + len(goodEMinus) == 2) and (len(goodEPlus) == len(goodEMinus)) and (len(goodMuPlus) + len(goodMuMinus) == 2) and (len(goodMuPlus) == len(goodMuMinus)):
        group3 = goodEPlus + goodEMinus + goodMuPlus + goodMuMinus
        h_em_sig.Fill( ((c_sig.lep_E[group1[0]]+c_sig.lep_E[group1[1]]+c_sig.lep_E[group2[0]]+c_sig.lep_E[group2[1]])**2
                        -(lep_pe+lep_pe1+lep_pm+lep_pm1)**2)**0.5)
                                                       
# Normalize all histograms to 1

norm_h_e_sig = h_e_sig.Integral()
h_e_sig.Scale(1.0/norm_h_e_sig)
norm_h_e_bgs = h_e_bgs.Integral()
h_e_bgs.Scale(1.0/norm_h_e_bgs)
norm_h_m_sig = h_m_sig.Integral()
h_m_sig.Scale(1.0/norm_h_m_sig)
norm_h_m_bgs = h_m_bgs.Integral()
h_m_bgs.Scale(1.0/norm_h_m_bgs)
norm_h_em_sig = h_e_sig.Integral()
h_em_sig.Scale(1.0/norm_h_e_sig)
norm_h_em_bgs = h_e_bgs.Integral()
h_em_bgs.Scale(1.0/norm_h_e_bgs)

# Aesthetics
h_e_sig.SetFillStyle(3003)
h_e_sig.SetFillColor(2)
h_e_sig.SetLineColor(2)
h_e_sig.SetStats(0)       #<--- removing the stats box

h_e_bgs.SetFillStyle(3001)
h_e_bgs.SetFillColor(4)
h_e_bgs.SetLineColor(4)
h_e_bgs.SetStats(0)

h_m_sig.SetFillStyle(3003)
h_m_sig.SetFillColor(2)
h_m_sig.SetLineColor(2)
h_m_sig.SetStats(0)      #<--- removing the stats box

h_m_bgs.SetFillStyle(3001)
h_m_bgs.SetFillColor(4)
h_m_bgs.SetLineColor(4)
h_m_bgs.SetStats(0)

h_em_sig.SetFillStyle(3003)
h_em_sig.SetFillColor(2)
h_em_sig.SetLineColor(2)
h_em_sig.SetStats(0)       #<--- removing the stats box

h_em_bgs.SetFillStyle(3001)
h_em_bgs.SetFillColor(4)
h_em_bgs.SetLineColor(4)
h_em_bgs.SetStats(0)

#  Create Legend
leg = ROOT.TLegend(0.5,0.7,0.9,0.9);
leg.AddEntry(h_e_sig, "Signal (H #rightarrow ZZ)", "f");
leg.AddEntry(h_e_bgs, "Background (ZZ)", "f");

leg1 = ROOT.TLegend(0.5,0.7,0.9,0.9);
leg1.AddEntry(h_m_sig, "Signal (H #rightarrow ZZ)", "f");
leg1.AddEntry(h_m_bgs, "Background (ZZ)", "f");

leg2 = ROOT.TLegend(0.5,0.7,0.9,0.9);
leg2.AddEntry(h_m_sig, "Signal (H #rightarrow ZZ)", "f");
leg2.AddEntry(h_m_bgs, "Background (ZZ)", "f");

# Create a TCanvas to contain each pair of histograms

c1 = ROOT.TCanvas("electron","MassE Canvas",800,600)

# Draw the c30 plots overlain

h_e_sig.Draw("HIST")
h_e_bgs.Draw("HIST SAME")
leg.Draw()
c1.Draw()

c1.Print("EMassPlot_3.png")

print("Hit enter to continue")
input()

c1.Close()
c2 = ROOT.TCanvas("muon","MassM Canvas",800,600)

h_m_sig.Draw("HIST")
h_m_bgs.Draw("HIST SAME")
leg1.Draw()
c2.Draw()

c2.Print("MMassPlot_3.png")

print("Hit enter to continue")
input()  

c3 = ROOT.TCanvas("muon and electron","MassME Canvas",800,600)

h_em_sig.Draw("HIST")
h_em_bgs.Draw("HIST SAME")
leg2.Draw()
c3.Draw()

c3.Print("MEMassPlot_3.png")

print("Hit enter to continue")
input()  
 