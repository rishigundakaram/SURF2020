void Pal1()
{
  //  gStyle->SetPalette(kCherry);
 
  // Inverted kCherry based on TColor.cxx Root v6.06.08
   const Int_t Number = 9;

   Double_t stops[9] = { 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000};

   //   Double_t red[9]   = { 37./255., 102./255., 157./255., 188./255., 196./255., 214./255., 223./255., 235./255., 251./255.};
   Double_t red[9]   = { 251./255., 235/255., 223./255., 214./255., 196./255., 188./255., 157./255., 102./255., 37./255.};

   //   Double_t green[9] = { 37./255.,  29./255.,  25./255.,  37./255.,  67./255.,  91./255., 132./255., 185./255., 251./255.};

   Double_t green[9] = { 251./255.,  185./255.,  132./255.,  91./255.,  67./255.,  37./255., 25./255., 29./255., 37./255.};

   //   Double_t blue[9]  = { 37./255.,  32./255.,  33./255.,  45./255.,  66./255.,  98./255., 137./255., 187./255., 251./255.};
   Double_t blue[9]  = { 251./255.,  187./255.,  137./255.,  98./255.,  66./255.,  45./255., 33./255., 32./255., 37./255.};
      TColor::CreateGradientColorTable(9, stops, red, green, blue, 255, Number);


}

void Pal2()
{

  // Inverted kDeepSea based on TColor.cxx Root v6.06.08
   const Int_t Number = 9;

   Double_t stops[9] = { 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000};


   //           Double_t red[9]   = {  0./255.,  9./255., 13./255., 17./255., 24./255.,  32./255.,  27./255.,  25./255.,  29./255.};
              Double_t red[9]   = {  29./255.,  25./255., 27./255., 32./255., 24./255.,  17./255.,  13./255.,  9./255.,  0./255.};

   //            Double_t green[9] = {  0./255.,  0./255.,  0./255.,  2./255., 37./255.,  74./255., 113./255., 160./255., 221./255.};

	      Double_t green[9] = {  211./255.,  160./255.,  113./255.,  74./255., 37./255.,  2./255., 0./255., 0./255., 0./255.};

   //         Double_t blue[9]  = { 28./255., 42./255., 59./255., 78./255., 98./255., 129./255., 154./255., 184./255., 221./255.};

           Double_t blue[9]  = { 221./255., 184./255., 154./255., 129./255., 98./255., 78./255., 59./255., 42./255., 28./255.};


      TColor::CreateGradientColorTable(9, stops, red, green, blue, 255, Number);

}

void Pal3()
{

   const Int_t Number = 9;

  // Inverted Greyscale

   Double_t stops[9] = { 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000};

   //   Double_t red[9]   = { 0./255., 32./255., 64./255., 96./255., 128./255., 160./255., 192./255., 224./255., 255./255.};

      Double_t red[9]   = { 255./255., 224./255., 192./255., 160./255., 128./255., 96./255., 64./255., 32./255., 0./255.};

   //   Double_t green[9] = { 0./255., 32./255., 64./255., 96./255., 128./255., 160./255., 192./255., 224./255., 255./255.};

      Double_t green[9]   = { 255./255., 224./255., 192./255., 160./255., 128./255., 96./255., 64./255., 32./255., 0./255.};

   // Double_t blue[9]  = { 0./255., 32./255., 64./255., 96./255., 128./255., 160./255., 192./255., 224./255., 255./255.};

      Double_t blue[9]   = { 255./255., 224./255., 192./255., 160./255., 128./255., 96./255., 64./255., 32./255., 0./255.};


   TColor::CreateGradientColorTable(9, stops, red, green, blue, 255, Number);

}


void plot_2D_fluxes(TString infilename)
{

  Double_t ybinmin=1;
  Double_t ybinmax=250;
  Double_t ytext=52;
  gStyle->SetOptStat(0);
  TFile f(infilename);
  TH2D* nusperbin2d_nue = (TH2D*)f.Get("nusperbin2d_nue");
  TH2D* nusperbin2d_nuebar = (TH2D*)f.Get("nusperbin2d_nuebar");
  TH2D* nusperbin2d_nux = (TH2D*)f.Get("nusperbin2d_nux");

  //  Int_t MyPalette[999];
  //  Double_t r[]    = {1., 1.0, 0.0, 0.0, 0.0};
  //Double_t g[]    = {0., 1.0, 1.0, 1.0, 0.0};
  //Double_t b[]    = {0., 0.0, 0.0, 1.0, 1.0};
  //Double_t stop[] = {0., .25, .50, .75, 1.0};


   //   Double_t r[]    = { 0.00, 0.00, 0.00};
   //Double_t g[]  = { 1.00, 0.60, 0.00};
   //Double_t b[]   = { 1.00, 1.00, 1.00};
   //Double_t stop[] = { 0.00, 0.5, 1.00 };

   //   Int_t FI = TColor::CreateGradientColorTable(3, stop, r, g, b, 100);
  //   Int_t FI = TColor::CreateGradientColorTable(5, stop, r, g, b, 999);
  // for (int i=0;i<999;i++) MyPalette[i] = FI+i;


  TCanvas* canv1 = new TCanvas("c1"," ",1000,500);
  canv1->SetLogx(0);
  canv1->SetLogz(0);

  canv1->Divide(3,1);

 
  nusperbin2d_nue->GetXaxis()->SetTitleSize(0.06);
  nusperbin2d_nue->GetXaxis()->SetTitleOffset(1.1);
  nusperbin2d_nue->GetXaxis()->SetLabelSize(0.0);

  nusperbin2d_nue->GetYaxis()->SetTitleSize(0.06);
  nusperbin2d_nue->GetYaxis()->SetTitleOffset(.9);
  nusperbin2d_nue->GetYaxis()->SetLabelSize(0.06);
  nusperbin2d_nue->GetZaxis()->SetTitleSize(0.1);
  nusperbin2d_nue->GetZaxis()->SetTitleOffset(0.);
  nusperbin2d_nue->GetZaxis()->SetLabelSize(0.05);
  //  nusperbin2d_nue->SetMaximum(5.e8);

  //  nusperbin2d_nue->SetTitle(" #nu_{e} flux, Garching model");

  nusperbin2d_nue->SetYTitle(" Energy (MeV) ");

  nusperbin2d_nue->GetXaxis()->SetRange(1,100);
  nusperbin2d_nue->GetYaxis()->SetRange(ybinmin,ybinmax);

  canv1->cd(1);
  gPad->SetLeftMargin(0.16);
  gPad->SetRightMargin(0.16);
  nusperbin2d_nue->Draw("colz");
  TExec *ex1 = new TExec("ex1","Pal1();");
  ex1->Draw();
  nusperbin2d_nue->Draw("colz same");

  // Root doesn't draw x-axis ticks... stupid Root


  //   Double_t xmin = -0.02;
  // Double_t xmax = 0.08;

  Double_t xmin = nusperbin2d_nue->GetXaxis()->GetBinLowEdge(1);
  Double_t xmax = nusperbin2d_nue->GetXaxis()->GetBinLowEdge(100);
   Double_t ymin = nusperbin2d_nue->GetYaxis()->GetBinLowEdge(1);
   Double_t ymax = nusperbin2d_nue->GetYaxis()->GetBinLowEdge(1);;
   cout << "xmin,xmax "<<xmin<<" "<<xmax<<endl;
   TGaxis *rax = new TGaxis(xmin, ymin, xmax, ymax, xmin, xmax, 5, "+L");
   rax->SetLineColor(kBlack);
   rax->SetLabelColor(kBlack); 
   rax->SetTitleColor(kBlack);
   rax->SetLabelFont(42);
   rax->SetTitleOffset(1.1); 
   rax->SetTitleSize(0.1);
   rax->SetLabelSize(0.06);
   rax->Draw();


  TText tneutronization;
  tneutronization.SetTextAlign(32);
  tneutronization.SetTextAngle(0);
  tneutronization.SetTextSize(0.07);
  tneutronization.DrawText(0.05,ytext,"Neutronization");

  canv1->Update();

  canv1->cd(2);
  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.16);

  nusperbin2d_nue->GetXaxis()->SetLabelSize(0.06);

  nusperbin2d_nue->SetYTitle(" ");
  nusperbin2d_nue->GetXaxis()->SetRange(100,600);
  nusperbin2d_nue->Draw("colz");


  TText taccretion;
  taccretion.SetTextAlign(32);
  taccretion.SetTextAngle(0);
  taccretion.SetTextSize(0.07);
  taccretion.DrawText(0.3,ytext,"Accretion");

  canv1->Update();

  canv1->cd(3);
  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.16);

  //  nusperbin2d_nue->SetXTitle(" Time (seconds) ");

  Int_t xbinmax = nusperbin2d_nue->GetNbinsX();
  // For case when flux cuts off
  Double_t bhxmax = 3.;

  bhxmin = nusperbin2d_nue->GetXaxis()->GetBinLowEdge(601);
  bhymin = nusperbin2d_nue->GetYaxis()->GetBinLowEdge(ybinmin);
  bhymax = nusperbin2d_nue->GetYaxis()->GetBinLowEdge(ybinmax);
  TH2D* hdum = new TH2D("hdum"," ",100,bhxmin,bhxmax,2,bhymin,bhymax);

  hdum->GetXaxis()->SetTitleSize(0.06);
  hdum->GetXaxis()->SetTitleOffset(1.1);
  hdum->GetXaxis()->SetLabelSize(0.06);

  hdum->GetYaxis()->SetTitleSize(0.06);
  hdum->GetYaxis()->SetTitleOffset(.9);
  hdum->GetYaxis()->SetLabelSize(0.06);
  hdum->GetZaxis()->SetTitleSize(0.1);
  hdum->GetZaxis()->SetTitleOffset(0.);
  hdum->GetZaxis()->SetLabelSize(0.05);
  hdum->SetXTitle(" Time (seconds) ");


  nusperbin2d_nue->GetXaxis()->SetRange(601,xbinmax);

  xmax = nusperbin2d_nue->GetXaxis()->GetBinLowEdge(xbinmax);
  if (xmax<bhxmax) {
    hdum->Draw();
    nusperbin2d_nue->Draw("colzsame");
    hdum->Draw("same");

  } else {
    nusperbin2d_nue->Draw("colzsame");

  }

  TText tcooling;
  tcooling.SetTextAlign(32);
  tcooling.SetTextAngle(0);
  tcooling.SetTextSize(0.07);
  tcooling.DrawText(3.3,ytext,"Cooling");


  canv1->Update();

  TString pngfilename = "nue_flux_3timescales_"+infilename;
  pngfilename.ReplaceAll("root","png");

  canv1->Print(pngfilename);

  cout << "Integral: "<<nusperbin2d_nue->Integral()<<endl;
  
  //====================

  TCanvas* canv3 = new TCanvas("c3"," ",1000,500);
  canv3->SetLogx(1);
  canv3->SetLogz(0);

  canv3->Divide(3,1);

 
  nusperbin2d_nuebar->GetXaxis()->SetTitleSize(0.06);
  nusperbin2d_nuebar->GetXaxis()->SetTitleOffset(1.1);
  nusperbin2d_nuebar->GetXaxis()->SetLabelSize(0.0);
  nusperbin2d_nuebar->GetXaxis()->SetTickSize(0.0);

  nusperbin2d_nuebar->GetYaxis()->SetTitleSize(0.06);
  nusperbin2d_nuebar->GetYaxis()->SetTitleOffset(1.);
  nusperbin2d_nuebar->GetYaxis()->SetLabelSize(0.06);
  nusperbin2d_nuebar->GetZaxis()->SetTitleSize(0.1);
  nusperbin2d_nuebar->GetZaxis()->SetTitleOffset(0.);
  nusperbin2d_nuebar->GetZaxis()->SetLabelSize(0.05);
  //  nusperbin2d_nuebar->SetMaximum(5.e8);

  //  nusperbin2d_nuebar->SetTitle(" #nu_{e} flux, Garching model");

  //  nusperbin2d_nuebar->SetYTitle(" Energy (MeV) ");

  nusperbin2d_nuebar->GetXaxis()->SetRange(1,100);
  nusperbin2d_nuebar->GetYaxis()->SetRange(ybinmin,ybinmax);

  canv3->cd(1);
  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.16);
  nusperbin2d_nuebar->Draw("colz");
  TExec *ex2 = new TExec("ex2","Pal2();");
  ex2->Draw();
  nusperbin2d_nuebar->Draw("colz same");

  // Root doesn't draw x-axis ticks... stupid Root

   rax->Draw();


   //  tneutronization.DrawText(0.03,ytext,"Neutronization");

  canv3->Update();

  canv3->cd(2);
  nusperbin2d_nuebar->GetXaxis()->SetLabelSize(0.06);

  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.16);

  nusperbin2d_nuebar->SetYTitle(" ");
  nusperbin2d_nuebar->GetXaxis()->SetRange(100,600);
  nusperbin2d_nuebar->Draw("colz");

  //  taccretion.DrawText(0.25,ytext,"Accretion");

  canv3->Update();

  canv3->cd(3);
  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.16);
  //  nusperbin2d_nuebar->SetXTitle(" Time (seconds) ");
  //  nusperbin2d_nuebar->GetXaxis()->SetRange(601,10000);
  nusperbin2d_nuebar->GetXaxis()->SetRange(601,xbinmax);



  xmax = nusperbin2d_nue->GetXaxis()->GetBinLowEdge(xbinmax);
  
  if (xmax<bhxmax) {
    hdum->Draw();
    nusperbin2d_nuebar->Draw("colzsame");
    hdum->Draw("same");

  } else {
    nusperbin2d_nuebar->Draw("colzsame");

  }
  

  //  tcooling.DrawText(3.,ytext,"Cooling");


  canv3->Update();

  pngfilename = "nuebar_flux_3timescales_"+infilename;

  pngfilename.ReplaceAll("root","png");

  canv3->Print(pngfilename);

 
  cout << "Integral: "<<nusperbin2d_nuebar->Integral()<<endl;
  
  //=============

  TCanvas* canv5 = new TCanvas("c5"," ",1000,500);
  canv5->SetLogx(1);
  canv5->SetLogz(0);


  canv5->Divide(3,1);


  nusperbin2d_nux->GetXaxis()->SetTitleSize(0.06);
  nusperbin2d_nux->GetXaxis()->SetTitleOffset(1.1);
  nusperbin2d_nux->GetXaxis()->SetLabelSize(0.0);
  nusperbin2d_nux->GetXaxis()->SetTickSize(0.0);

  nusperbin2d_nux->GetYaxis()->SetTitleSize(0.06);
  nusperbin2d_nux->GetYaxis()->SetTitleOffset(1.);
  nusperbin2d_nux->GetYaxis()->SetLabelSize(0.06);
  nusperbin2d_nux->GetZaxis()->SetTitleSize(0.1);
  nusperbin2d_nux->GetZaxis()->SetTitleOffset(0.);
  nusperbin2d_nux->GetZaxis()->SetLabelSize(0.05);
  //  nusperbin2d_nux->SetMaximum(5.e8);

  //  nusperbin2d_nux->SetTitle(" #nu_{e} flux, Garching model");

  //  nusperbin2d_nux->SetYTitle(" Energy (MeV) ");

  nusperbin2d_nux->GetXaxis()->SetRange(1,100);
  nusperbin2d_nux->GetYaxis()->SetRange(ybinmin,ybinmax);

  canv5->cd(1);
  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.16);
  nusperbin2d_nux->Draw("colz");
  TExec *ex3 = new TExec("ex3","Pal3();");
  ex3->Draw();
  nusperbin2d_nux->Draw("colz same");

  // Root doesn't draw x-axis ticks... stupid Root

  rax->Draw();


  //  tneutronization.DrawText(0.03,ytext,"Neutronization");

  canv5->Update();

  canv5->cd(2);
  nusperbin2d_nux->GetXaxis()->SetLabelSize(0.06);

  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.16);

  nusperbin2d_nux->SetYTitle(" ");
  nusperbin2d_nux->GetXaxis()->SetRange(100,600);
  nusperbin2d_nux->Draw("colz");

  //  taccretion.DrawText(0.25,ytext,"Accretion");

  canv5->Update();

  canv5->cd(3);
  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.16);

  nusperbin2d_nux->SetXTitle(" Time (seconds) ");
  //  nusperbin2d_nux->GetXaxis()->SetRange(601,10000);
  nusperbin2d_nux->GetXaxis()->SetRange(601,xbinmax);

  xmax = nusperbin2d_nue->GetXaxis()->GetBinLowEdge(xbinmax);
  
  if (xmax<bhxmax) {
    hdum->Draw();
    nusperbin2d_nux->Draw("colzsame");
    hdum->Draw("same");

  } else {
    nusperbin2d_nux->Draw("colzsame");

  }


  //  tcooling.DrawText(3.,ytext,"Cooling");


  canv5->Update();

  pngfilename = "nux_flux_3timescales_"+infilename;

  pngfilename.ReplaceAll("root","png");
  canv5->Print(pngfilename);



  cout << "Integral: "<<nusperbin2d_nux->Integral()<<endl;
  



}
