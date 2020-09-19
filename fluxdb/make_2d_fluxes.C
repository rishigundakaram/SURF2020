// Tool to turn digitized Huedepohl files into pinched flux files for time slices
// Input is flux file name
// Reads the digitized files, makes fluxname_pinched_info.dat for use with
// Snowglobes pinched.C file
// Also makes fluxname_key.dat to associate flux number with time slide
// Note: produces luminosities appropriate for *fluences* in Snowglobes-- luminosities are in ergs/s, then integrated over the given time bin.
// K. Scholberg December 2013


// Function to calculate the energy spectrum, from Snowglobes pinched.C
double phi(double E_nu, double E_nu0, double alpha) {
	double N=pow((alpha+1.),(alpha+1.))/(E_nu0*tgamma(alpha+1.));
	double R=N*pow((E_nu/E_nu0),alpha)*exp((-1.)*(alpha+1.)*E_nu/E_nu0); 


	//	cout << pow(alpha+1, alpha+1)<<" "<<tgamma(alpha+1)<<endl;
	//	cout << "phi "<<E_nu<<" "<<E_nu0<<" "<<alpha<<" "<<N<<" "<<R<<endl;
	return R;
}


void make_2d_fluxes(TString indirname, TString outdirname, TString fluxname, Int_t write_root)
{

  gStyle->SetOptStat(0);

  // Two timescales, 6 flavors, three types of quantities (lum, eavg, alpha)
  // One graph array per quantity, indexed by flavor. 

  const Int_t numflavor = 3;
  //  TString flavname[6] = {"nue","nuebar","numu","numubar","nutau","nutaubar"};
  TString flavname[numflavor] = {"nue","nuebar","numu"};
  TString flavname2[numflavor] = {"nu_e","nubar_e","nu_x"};

  // numu is same as nux

  TGraph** luminosity_graphs = new TGraph*[numflavor];
  TGraph** avgen_graphs = new TGraph*[numflavor];
  TGraph** alpha_graphs = new TGraph*[numflavor];
  

  const Int_t maxpoints=20000;
  Double_t time[maxpoints];
  Double_t yval_lum[maxpoints];
  Double_t yval_avgen[maxpoints];
  Double_t yval_avgen2[maxpoints];
  Double_t alpha[maxpoints];

  Int_t i=0;
  Int_t j=0;

  Double_t lum_factor = 1.e51;

  std::string line;

  for (i;i<numflavor;i++){

    // Luminosity
    std::ifstream in;

    TString infilename = indirname+fluxname+"/timedata/neutrino_signal_"+flavname2[i];

    cout << "Reading "<< infilename<<endl;

    in.open(infilename);
    j=0;
    Int_t numpoints;
    
    //    while(1) {

    while( getline(in, line) ) {

      if (!line.length() || line[0] == '#')
	continue;
      std::istringstream iss(line);
      iss >> time[j]>>yval_lum[j]>>yval_avgen[j]>>yval_avgen2[j];
      //      cout << "time "<<time[j]<<" "<<yval_lum[j]<<endl;
      if (yval_lum[j]<0) {yval_lum[j]=0;}
      if (yval_avgen[j]<0) {yval_avgen[j]=0;}
      if (yval_avgen2[j]<0) {yval_avgen2[j]=0;}
      
      if ((yval_avgen[j]*yval_avgen[j]-yval_avgen2[j])!= 0.) {
	alpha[j] = (yval_avgen2[j]-2.*yval_avgen[j]*yval_avgen[j])/(yval_avgen[j]*yval_avgen[j]-yval_avgen2[j]);
	  }
      else {
	alpha[j] = 0.;
      }


      if (!in.good()) break;
      j++;

    } // End of file reading loop

    numpoints = j;
    in.close();
    
    luminosity_graphs[i]= new TGraph(numpoints,time,yval_lum);
    
    avgen_graphs[i]= new TGraph(numpoints,time,yval_avgen);

    alpha_graphs[i]= new TGraph(numpoints,time,alpha);

    //    graphs[i]->Print();

  } // End of loop over flavors

  // Now choose time intervals in log steps

  const Int_t maxtimebins = 100000;
  Double_t timebins[maxtimebins];

  // Want log steps but starts negative, so put an offset

  //  Double_t t_offset = 0.35;
  Double_t t_offset = 0.;
  //  Double_t t_start = 0. ;
  Double_t t_start = time[0];

  //  Double_t t_end = 8.35+t_offset;
  t_end = time[j-1];
  //  Double_t t_step = TMath::Log10(t_end/t_start)/double(ntimebins);
  t_step = 0.0001;

  //    cout << "t_step "<<t_step<<endl;

  Double_t t;

  Double_t tot_dt=0;

  // Get the ranges of each of the graphs

  Int_t k;
  Double_t xx,yy;
  Double_t alpha_first[numflavor];
  Double_t avgen_first[numflavor];
  Double_t luminosity_first[numflavor];
  Double_t alpha_last[numflavor];
  Double_t avgen_last[numflavor];
  Double_t luminosity_last[numflavor];

  //Saved for nue flux
  Double_t alpha_val_first[numflavor];
  Int_t ret;

  for (k=0;k<numflavor;k++) {
    Int_t numpt;
    numpt = alpha_graphs[k]->GetN();
    if (numpt>0) {
      ret = alpha_graphs[k]->GetPoint(0,xx,yy);
      alpha_first[k] = xx;
      alpha_val_first[k] = yy;
      ret = alpha_graphs[k]->GetPoint(numpt-1,xx,yy);
      alpha_last[k] = xx;

    }

    numpt = avgen_graphs[k]->GetN();
    if (numpt>0) {
      ret = avgen_graphs[k]->GetPoint(0,xx,yy);
      avgen_first[k] = xx;
      ret = avgen_graphs[k]->GetPoint(numpt-1,xx,yy);
      avgen_last[k] = xx;
    }

    numpt = luminosity_graphs[k]->GetN();
    if (numpt>0) {
      ret = luminosity_graphs[k]->GetPoint(0,xx,yy);
      luminosity_first[k] = xx;
      ret = luminosity_graphs[k]->GetPoint(numpt-1,xx,yy);
      luminosity_last[k] = xx;
    }


    cout << "flav "<<k<<" alpha "<< alpha_first[k]<<" "<<alpha_last[k]<<endl;
     cout << "flav "<<k<<" avgen "<< avgen_first[k]<<" "<<avgen_last[k]<<endl;
    cout << "flav "<<k<<" luminosity "<< luminosity_first[k]<<" "<<luminosity_last[k]<<endl;
  }


  // Output files

  TString outfilename = outdirname+fluxname+"_parameters.dat";
  outfilename.ReplaceAll("/","-");
  ofstream outfile;
  outfile.open(outfilename);
  cout << "Outfilename: "<< outfilename<<endl;

  outfile << "# If you use this flux, cite http://wwwmpa.mpa-garching.mpg.de/ccsnarchive/data/Huedepohl2014_phd_thesis/, "<<endl;
  outfile << "# Huedepohl, L. (2014), Neutrinos from the Formation, Cooling and Black Hole Collapse of Neutron Stars, PhD. Thesis, Technische Universitat Muenchen"<<endl;
  outfile << "# time (s), <energy> (MeV), alpha, luminosity (foe/s), for nu_e, nu_e_bar, nu_mu" <<endl;


  Double_t dt=t_step;

  for (t=t_start;t<=t_end;t+=t_step) {
  //  for (i=0;i<=ntimebins;i++)   {
    //      t = t_start*TMath::Power(10.0, double(i)*t_step);
    timebins[i]= t;

    //    cout <<timebins[i]<<" "<<luminosity_graphs[0]->Eval(timebins[i],0,"")<<endl;

      // Approximate dt.. maybe should be a geometric mean for bin center
    //      Double_t dt = t_start*TMath::Power(10.0,double(i+0.5)*t_step)-
    //                      t_start*TMath::Power(10.0,double(i-0.5)*t_step);
    //      cout << i<<" time bin "<<t_start*TMath::Power(10.0,double(i-0.5)*t_step)-t_offset<<" "<<timebins[i]<<" "<<t_start*TMath::Power(10.0,double(i+0.5)*t_step)-t_offset<<" "<<dt<<endl;

      tot_dt += dt;  // for check


      Double_t alpha_nue, avgen_nue, luminosity_nue;
      Double_t alpha_nuebar, avgen_nuebar, luminosity_nuebar;
      Double_t alpha_nux, avgen_nux, luminosity_nux;

      // Get the values from the plots.  But first check we are within the meaningful range for each graph for each flavor.


      // Fine-tuning for nue for Garching flux:  nue luminosity and energies are non-zero at negative times; assume alpha is the same as at the beginning for the range.  Don't need here...

       if (timebins[i]>alpha_first[0] && timebins[i]<alpha_last[0]
 	  && timebins[i]>avgen_first[0] && timebins[i]<avgen_last[0] 
           && timebins[i]>luminosity_first[0] && timebins[i]<luminosity_last[0]) {

// 	if (timebins[i]>alpha_first[0]) {
 	  alpha_nue = alpha_graphs[0]->Eval(timebins[i],0,""); 
 	  avgen_nue = avgen_graphs[0]->Eval(timebins[i],0,""); 
 	  luminosity_nue = luminosity_graphs[0]->Eval(timebins[i],0,""); 
	  /// 	} else {

// 	  // Use the saved value
// 	  alpha_nue = alpha_val_first[0];
// 	  avgen_nue = avgen_graphs[0]->Eval(timebins[i],0,""); 
// 	  luminosity_nue = luminosity_graphs[0]->Eval(timebins[i],0,""); 

// 	}

	
       } else {
 	alpha_nue=0.;
 	avgen_nue = 0.;
 	luminosity_nue=0.;
       }


//       // Nuebar
       if (timebins[i]>alpha_first[1] && timebins[i]<alpha_last[1]
 	  && timebins[i]>avgen_first[1] && timebins[i]<avgen_last[1] 
           && timebins[i]>luminosity_first[1] && timebins[i]<luminosity_last[1]) {

 	alpha_nuebar = alpha_graphs[1]->Eval(timebins[i],0,""); 
 	avgen_nuebar = avgen_graphs[1]->Eval(timebins[i],0,""); 
 	luminosity_nuebar = luminosity_graphs[1]->Eval(timebins[i],0,""); 
	
       } else {
 	alpha_nuebar=0.;
 	avgen_nuebar = 0.;
 	luminosity_nuebar=0.;
       }

//       //Numu

       if (timebins[i]>alpha_first[2] && timebins[i]<alpha_last[2]
 	  && timebins[i]>avgen_first[2] && timebins[i]<avgen_last[2] 
           && timebins[i]>luminosity_first[2] && timebins[i]<luminosity_last[2]) {

 	alpha_nux = alpha_graphs[2]->Eval(timebins[i],0,""); 
 	avgen_nux = avgen_graphs[2]->Eval(timebins[i],0,""); 
 	luminosity_nux = luminosity_graphs[2]->Eval(timebins[i],0,""); 
	
       } else {
 	alpha_nux=0.;
 	avgen_nux = 0.;
 	luminosity_nux=0.;
       }

  // Save the time and dt for each flux file number in the key file
       //      outfile2 << i<< " "<<timebins[i]<<" "<<dt<<endl;

      // Correct luminosity units
      //      cout <<"timebin"<<timebins[i]<<" "<<dt<<endl;
       //      dt*= 1.e51;

  outfile << t<< " "
       <<avgen_nue<<" "
       <<alpha_nue<<" "
       <<luminosity_nue*lum_factor<<" "
       <<avgen_nuebar<<" "
       <<alpha_nuebar<<" "
       <<luminosity_nuebar*lum_factor<<" "
       <<avgen_nux<<" "
       <<alpha_nux<<" "
       <<luminosity_nux*lum_factor<<endl;



  //  cout << i<< " "<<timebins[i]<<" "
  //     <<alpha_nue<<" "
  //     <<alpha_nuebar<<" "
  //     <<alpha_nux<<" "
  //     <<avgen_nue<<" "
  //     <<avgen_nuebar<<" "
  //     <<avgen_nux<<" "
  //     <<luminosity_nue*dt<<" "
  //     <<luminosity_nuebar*dt<<" "
  //     <<luminosity_nux*dt<<endl;

  i++;
  }


  //  cout << "tot_dt "<< tot_dt <<" "<<t_end-t_start<<endl;

  outfile.close();


  //   avgen_graphs[0]->Print("all");

  // Now make the 2D histos

  t_step = 0.001;
  ntimebins = TMath::Nint((t_end-t_start)/t_step)+1;
  cout << "ntimebins "<<ntimebins<<endl;

  Double_t firsten = 0.;
  Double_t lasten = 100.;
  Double_t estep=0.2;
  Int_t numenbins = TMath::Nint((lasten-firsten)/estep)+1;


  TH2D* nusperbin2d_nue = new TH2D("nusperbin2d_nue"," ",ntimebins,t_start-t_step/2.,t_end+t_step/2.,numenbins,firsten-estep/2.,lasten+estep/2.);

  TH2D* nusperbin2d_nuebar = new TH2D("nusperbin2d_nuebar"," ",ntimebins,t_start-t_step/2.,t_end+t_step/2.,numenbins,firsten-estep/2.,lasten+estep/2.);


  TH2D* nusperbin2d_nux = new TH2D("nusperbin2d_nux"," ",ntimebins,t_start-t_step/2.,t_end+t_step/2.,numenbins,firsten-estep/2.,lasten+estep/2.);

  Double_t Fnue;
  Double_t Fnuebar;
  Double_t Fnux;
  Double_t en;


  const Double_t dist=3.08568025e22; // [dist]=cm
  const Double_t gevpererg = 624.15;

  
  //    avgen_graphs[0]->Print("all");
   cout << "avgen "<< avgen_graphs[0]->Eval(0.688717,0,"")<<endl;
  //exit(0);

   Double_t avgen_nue1;
   Double_t luminosity_nue1;
   Double_t alpha_nue1;

   Double_t avgen_nuebar1;
   Double_t luminosity_nuebar1;
   Double_t alpha_nuebar1;

   Double_t avgen_nux1;
   Double_t luminosity_nux1;
   Double_t alpha_nux1;

  for (t=t_start;t<=t_end;t+=t_step) {
    en = firsten;
    i=0;
    avgen_nue1 = avgen_graphs[0]->Eval(t,0,"");
    luminosity_nue1 = luminosity_graphs[0]->Eval(t,0,"")*lum_factor*gevpererg*1000.;
    alpha_nue1 = alpha_graphs[0]->Eval(t,0,"");

    avgen_nuebar1 = avgen_graphs[1]->Eval(t,0,"");
    luminosity_nuebar1 = luminosity_graphs[1]->Eval(t,0,"")*lum_factor*gevpererg*1000.;
    alpha_nuebar1 = alpha_graphs[1]->Eval(t,0,"");

    avgen_nux1 = avgen_graphs[2]->Eval(t,0,"");
    luminosity_nux1 = luminosity_graphs[2]->Eval(t,0,"")*lum_factor*gevpererg*1000.;
    alpha_nux1 = alpha_graphs[2]->Eval(t,0,"");


   
    for(en=firsten; en<=lasten; en+=estep) {
     

      if (avgen_nue1>0) {

	Fnue = 1/(4*TMath::Pi()*dist*dist)*luminosity_nue1/avgen_nue1*phi(en,avgen_nue1,alpha_nue1)*estep*t_step;
      } else {
	Fnue = 0.;
      }

      nusperbin2d_nue->Fill(t,en,Fnue);

      if (avgen_nuebar1>0) {

	Fnuebar = 1/(4*TMath::Pi()*dist*dist)*luminosity_nuebar1/avgen_nuebar1*phi(en,avgen_nuebar1,alpha_nuebar1)*estep*t_step;
      } else {
	Fnue = 0.;
      }

      nusperbin2d_nuebar->Fill(t,en,Fnuebar);

      if (avgen_nux1>0) {

	Fnux = 1/(4*TMath::Pi()*dist*dist)*luminosity_nux1/avgen_nux1*phi(en,avgen_nux1,alpha_nux1)*estep*t_step;
      } else {
	Fnux = 0.;
      }

      nusperbin2d_nux->Fill(t,en,Fnux);

      //   if (t<1. && t> 0.5) {
      //cout << "t "<<t<<" "<<avgen_nue1<<" "<<alpha_nue1<<" "<<luminosity_nue1<<" "<<Fnue<<endl;
      //}


	//	nusperbin2d_nuebar->Fill(t,en,Fnuebar);
	//nusperbin2d_nux->Fill(t,en,Fnumu+Fnumubar+Fnutau+Fnutaubar);
      i++;
      //          cout << en<<" "<<t<<" "<<Fnue<<endl;

    }
  }

  //  cout << i<<endl;

  if (write_root == 1) {
    TString rootfilename =  outdirname+fluxname+".root";

    rootfilename.ReplaceAll("/","-");

    cout <<"rootfilename "<<rootfilename<<endl;
    TFile f(rootfilename,"recreate");
    nusperbin2d_nue->Write();
    nusperbin2d_nuebar->Write();
    nusperbin2d_nux->Write();
    f.Close();

  }


}




