# Goal: reconstruct invariant mass of Z^0 boson and Higgs boson, compare with background

#        Preselction: isSF,sum(lepCharge) == 0, only 1 good pair (e-e+ or m-m+) not both STORE ONLY THE GOOD PAIRS, NOT THE EVENTS WITH THE GOOD PAIRS


import ROOT as r

# Open the background file and print the number of events it contains

bkg = r.TFile.Open("data/4lep/MC/mc_363490.llll.4lep.root") #opens file
t_bkg = bkg.Get("mini") #converts file to Tree, mini is name of TTree object
t_bkg.GetEntries() 

# Create a TChain to combine the signal files, and print the total number of signal events (Higgs decays)

sig = r.TChain("mini") #same thing but with chain so we can add files together
sig.Add("data/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root")
sig.Add("data/4lep/MC/mc_344235.VBFH125_ZZ4lep.4lep.root")
sig.GetEntries()

# Create background histograms

h_invMe_bkg = r.TH1F("h_invMe_bkg"," Invariant mass of e^{-}e^{+}; Invariant Mass (GeV) ; Events/bin",40,0,200) #creating histogram containers
h_invMm_bkg = r.TH1F("h_invMm_bkg"," Invariant mass of m^{-}m^{+}; Invariant Mass (GeV) ; Events/bin",40,0,200)
h_invMem_bkg = r.TH1F("h_invMem_bkg"," Invariant mass of em^{-}em^{+}; Invariant Mass (GeV) ; Events/bin",40,0,200)


# Create signal histograms

h_invMe_sig = r.TH1F("h_invMe_sig"," Invariant mass of e^{-}e^{+}; Invariant Mass (GeV) ; Events/bin",40,0,200) #creating histogram containers
h_invMm_sig = r.TH1F("h_invMm_sig"," Invariant mass of m^{-}m^{+}; Invariant Mass (GeV) ; Events/bin",40,0,200)
h_invMem_sig = r.TH1F("h_invMem_sig"," Invariant mass of em^{-}em^{+}; Invariant Mass (GeV) ; Events/bin",40,0,200)


# Create lists for the lepton variables that you will be using to reconstruct the invariant mass (background)
ePluspT_bkg = []
ePlusPhi_bkg = []
ePlusEta_bkg = []
ePlusE_bkg = []

eMinuspT_bkg = []
eMinusPhi_bkg = []
eMinusEta_bkg = []
eMinusE_bkg = []

mPluspT_bkg = []
mPlusPhi_bkg = []
mPlusEta_bkg = []
mPlusE_bkg = []

mMinuspT_bkg = []
mMinusPhi_bkg = []
mMinusEta_bkg = []
mMinusE_bkg = []

# Fill the lists for the background
for event in t_bkg: 
    if (t_bkg.trigE == True) or (t_bkg.trigM == True): #passes trigger
        if (sum(t_bkg.lep_charge) == 0): # lep_charge stored as 1 or -1, so if we want 2 positive charges and 2 negative charges, sum must be 0
            if (sum(t_bkg.lep_type) == 48): # lep_type stored as 11 or 13, 48 for 2 muon 2 electron
                for lepton in range(t_bkg.lep_n): # go into each lepton
                    #if (abs(t_bkg.lep_eta[lepton]) < 2.5) and (t_bkg.lep_ptcone30[lepton]/t_bkg.lep_pt[lepton] < 0.3) and (t_bkg.lep_etcone20[lepton]/t_bkg.lep_pt[lepton] < 0.3):
                        if (t_bkg.lep_type[lepton]) == 13: #if lepton is electron
                                if (t_bkg.lep_charge[lepton]) == 1: #if electron is + charge
                                        ePluspT_bkg.append(t_bkg.lep_pt[lepton])
                                        ePlusPhi_bkg.append(t_bkg.lep_phi[lepton])
                                        ePlusEta_bkg.append(t_bkg.lep_eta[lepton])
                                        ePlusE_bkg.append(t_bkg.lep_E[lepton])
                                elif (t_bkg.lep_charge[lepton]) == -1: #if electron is - charge
                                        eMinuspT_bkg.append(t_bkg.lep_pt[lepton])
                                        eMinusPhi_bkg.append(t_bkg.lep_phi[lepton])
                                        eMinusEta_bkg.append(t_bkg.lep_eta[lepton])
                                        eMinusE_bkg.append(t_bkg.lep_E[lepton])
                        elif (t_bkg.lep_type[lepton]) == 11: #if lepton is muon
                                if (t_bkg.lep_charge[lepton]) > 0: #if muon is + charge
                                        mPluspT_bkg.append(t_bkg.lep_pt[lepton])
                                        mPlusPhi_bkg.append(t_bkg.lep_phi[lepton])
                                        mPlusEta_bkg.append(t_bkg.lep_eta[lepton])
                                        mPlusE_bkg.append(t_bkg.lep_E[lepton])
                                elif (t_bkg.lep_charge[lepton]) < 0: #if muon is - charge
                                        mMinuspT_bkg.append(t_bkg.lep_pt[lepton])
                                        mMinusPhi_bkg.append(t_bkg.lep_phi[lepton])
                                        mMinusEta_bkg.append(t_bkg.lep_eta[lepton])
                                        mMinusE_bkg.append(t_bkg.lep_E[lepton])
                                        
# # Create lists for the lepton variables that you will be using to reconstruct the invariant mass (signal)                                            
ePluspT_sig = []
ePlusPhi_sig = []
ePlusEta_sig = []
ePlusE_sig = []

eMinuspT_sig = []
eMinusPhi_sig = []
eMinusEta_sig = []
eMinusE_sig = []

mPluspT_sig = []
mPlusPhi_sig = []
mPlusEta_sig = []
mPlusE_sig = []

mMinuspT_sig = []
mMinusPhi_sig = []
mMinusEta_sig = []
mMinusE_sig = []
        
                
    
# # Fill the lists for the signal 
for event in sig: 
    if (sig.trigE == True) or (sig.trigM == True): #passes trigger
        if (sum(sig.lep_charge) == 0): # lep_charge stored as 1 or -1, so if we want 2 positive charges and 2 negative charges, sum must be 0
            if (sum(sig.lep_type) == 48): # lep_type stored as 11 or 13, 48 for 2 muon 2 electron
                for lepton in range(sig.lep_n): # go into each lepton
                    #if (abs(sig.lep_eta[lepton]) < 2.5) and (sig.lep_ptcone30[lepton]/sig.lep_pt[lepton] < 0.3) and (sig.lep_etcone20[lepton]/sig.lep_pt[lepton] < 0.3):
                        if (sig.lep_type[lepton]) == 13: #if lepton is electron
                                if (sig.lep_charge[lepton]) == 1: #if electron is + charge
                                        ePluspT_sig.append(sig.lep_pt[lepton])
                                        ePlusPhi_sig.append(sig.lep_phi[lepton])
                                        ePlusEta_sig.append(sig.lep_eta[lepton])
                                        ePlusE_sig.append(sig.lep_E[lepton])
                                elif (sig.lep_charge[lepton]) == -1: #if electron is - charge
                                        eMinuspT_sig.append(sig.lep_pt[lepton])
                                        eMinusPhi_sig.append(sig.lep_phi[lepton])
                                        eMinusEta_sig.append(sig.lep_eta[lepton])
                                        eMinusE_sig.append(sig.lep_E[lepton])
                        elif (sig.lep_type[lepton]) == 11: #if lepton is muon
                                if (sig.lep_charge[lepton]) == 1: #if muon is + charge
                                        mPluspT_sig.append(sig.lep_pt[lepton])
                                        mPlusPhi_sig.append(sig.lep_phi[lepton])
                                        mPlusEta_sig.append(sig.lep_eta[lepton])
                                        mPlusE_sig.append(sig.lep_E[lepton])
                                elif (sig.lep_charge[lepton]) == -1: #if muon is - charge
                                        mMinuspT_sig.append(sig.lep_pt[lepton])
                                        mMinusPhi_sig.append(sig.lep_phi[lepton])
                                        mMinusEta_sig.append(sig.lep_eta[lepton])
                                        mMinusE_sig.append(sig.lep_E[lepton])


# Checking that the number of e-e+ pairs equals number of m-m+ pairs
if len(ePluspT_sig) != len(eMinuspT_sig) or len(mPluspT_sig) != len(mMinuspT_sig):
        print("ERROR: You dont have an equal number of electron pairs and muon pairs for your signal!")
        
if len(ePluspT_bkg) != len(eMinuspT_bkg) or len(mPluspT_bkg) != len(mMinuspT_bkg):
        print("ERROR: You dont have an equal number of electron pairs and muon pairs for your background!")

#Next step, fill histograms with invariant mass (need equation)

for i in range(len(ePluspT_sig)):
        h_invMe_sig.Fill(r.sqrt(2*ePluspT_sig[i]*eMinuspT_sig[i]*(r.cosh(ePlusEta_sig[i]-eMinusEta_sig[i])-r.cos(ePlusPhi_sig[i]-eMinusPhi_sig[i])))/1000)
        h_invMe_bkg.Fill(r.sqrt(2*ePluspT_bkg[i]*eMinuspT_bkg[i]*(r.cosh(ePlusEta_bkg[i]-eMinusEta_bkg[i])-r.cos(ePlusPhi_bkg[i]-eMinusPhi_bkg[i])))/1000)
        h_invMm_sig.Fill(r.sqrt(2*mPluspT_sig[i]*mMinuspT_sig[i]*(r.cosh(mPlusEta_sig[i]-mMinusEta_sig[i])-r.cos(mPlusPhi_sig[i]-mMinusPhi_sig[i])))/1000)
        h_invMm_bkg.Fill(r.sqrt(2*mPluspT_bkg[i]*mMinuspT_bkg[i]*(r.cosh(mPlusEta_bkg[i]-mMinusEta_bkg[i])-r.cos(mPlusPhi_bkg[i]-mMinusPhi_bkg[i])))/1000)
        h_invMem_sig.Fill(r.sqrt((ePlusE_sig[i]+eMinusE_sig[i]+mPlusE_sig[i]+mMinusE_sig[i])**2 * (ePluspT_sig[i]+eMinuspT_sig[i]+mPluspT_sig[i]+mMinuspT_sig[i])**2)/1000)
        h_invMem_bkg.Fill(r.sqrt((ePlusE_bkg[i]+eMinusE_bkg[i]+mPlusE_bkg[i]+mMinusE_bkg[i])**2 * (ePluspT_bkg[i]+eMinuspT_bkg[i]+mPluspT_bkg[i]+mMinuspT_bkg[i])**2)/1000)

norm_invMe_bkg = h_invMe_bkg.Integral()
h_invMe_bkg.Scale(1.0/norm_invMe_bkg) # Scales the histogram by multiplying all the contents by the normalization factor (which is 1/sum(bins))s
norm_invMm_bkg = h_invMm_bkg.Integral()
h_invMm_bkg.Scale(1.0/norm_invMm_bkg)
norm_invMe_sig = h_invMe_sig.Integral()
h_invMe_sig.Scale(1.0/norm_invMe_sig)
norm_invMm_sig = h_invMm_sig.Integral()
h_invMm_sig.Scale(1.0/norm_invMm_sig)
norm_invMem_sig = h_invMem_sig.Integral()
h_invMem_sig.Scale(1.0/norm_invMem_sig)
norm_invMem_bkg = h_invMem_sig.Integral()
h_invMem_bkg.Scale(1.0/norm_invMem_bkg)


# Aesthetics
h_invMe_sig.SetFillStyle(3003)  # pattern style in the histogram
h_invMe_sig.SetFillColor(2) # color of histogram
h_invMe_sig.SetLineColor(2) # line color of histogram
h_invMe_sig.SetStats(0)       #<--- removing the stats box

h_invMe_bkg.SetFillStyle(3001)
h_invMe_bkg.SetFillColor(4)
h_invMe_bkg.SetLineColor(4)
h_invMe_bkg.SetStats(0)

h_invMm_sig.SetFillStyle(3003)
h_invMm_sig.SetFillColor(2)
h_invMm_sig.SetLineColor(2)
h_invMm_sig.SetStats(0)      #<--- removing the stats box

h_invMm_bkg.SetFillStyle(3001)
h_invMm_bkg.SetFillColor(4)
h_invMm_bkg.SetLineColor(4)
h_invMm_bkg.SetStats(0)

h_invMem_sig.SetFillStyle(3003)
h_invMem_sig.SetFillColor(2)
h_invMem_sig.SetLineColor(2)
h_invMem_sig.SetStats(0)      #<--- removing the stats box

h_invMem_bkg.SetFillStyle(3001)
h_invMem_bkg.SetFillColor(4)
h_invMem_bkg.SetLineColor(4)
h_invMem_bkg.SetStats(0)

#  Create Legend
leg = r.TLegend(0.5,0.7,0.9,0.9); #puts legend in upper right area
leg.AddEntry(h_invMe_sig, "Signal (H #rightarrow ZZ)", "f"); #add entry to Legend, (which histogram, "name you want entry to say","style of box of color")
leg.AddEntry(h_invMe_bkg, "Background (ZZ)", "f");

# Create a TCanvas to contain each pair of histograms

c1 = r.TCanvas("invMeCanvas","invMe Canvas",800,600)

# Draw the E_T plots overlain

h_invMe_sig.Draw("HIST")
h_invMe_bkg.Draw("HIST SAME")
leg.Draw()
c1.Draw()

c1.Print("invMe.png")

print("Hit enter to continue")
input()

c1.Close()
c2 = r.TCanvas("invMmCanvas", "invMm Canvas",800,600)

h_invMm_sig.Draw("HIST")
h_invMm_bkg.Draw("HIST SAME")
leg.Draw()
c2.Draw()

c2.Print("invMmPlot.png")

print("Hit enter to continue")
input()

c3 = r.TCanvas("invMemCanvas", "Invariant Mass 4 lep Canvas",800,600)

h_invMem_sig.Draw("HIST")
h_invMem_bgs.Draw("HIST SAME")
leg.Draw()
c3.Draw()

c3.Print("invMemPlot.png")

print("Hit enter to continue")
input()






#            for lep in range(t_bkg.lep_n):
 #                   if sig.lep_type[lep] == 13: #if lepton is an electron
  #                          if sig.lep_charge[lep] == 1: #electron is positive charge (positron)
 #                                   goodEPlus.append(lep)
   #                         elif sig.lep_charge[lep] == -1: # electron is negative charge
  #                                  goodEMinus.append(lep)
    #                 elif sig.lep_type[lep] == 1: #if lepton is a muon
    #                        if sig.lep_charge[lep] == 1: #muon is positive charge 
       #                             goodMPlus.append(lep)
     #                       elif sig.lep_charge[lep] == -1: # muon is negative charge
         #                           goodMMinus.append(lep)  
