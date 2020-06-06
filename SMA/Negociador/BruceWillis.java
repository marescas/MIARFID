import java.util.Random;
import java.util.Vector;

import negotiator.Bid;
import negoUPV.UPVAgent;

public class BruceWillis extends UPVAgent {

	Bid last_moment_offer;
	double S;
	double beta;
	double RU;
	int delta;
	Vector<Bid> opponent_offers;
	double thresholdTimeInitial,thresholdTimeFinal;
	
	public void initialize() {
		last_moment_offer = null;
		opponent_offers = null;
		delta = 50; //Con un delta mayor conseguimos un promedio mas estable al explorar ofertas mas antiguas
		
		//Empezamos como un negociador duro
		beta = 0.1;
		RU = 0.9;
		S = 0.99;
		thresholdTimeInitial = 0.5;
		thresholdTimeFinal = 0.82;
		update();
	}

	public boolean acceptOffer(Bid offer) {
		
		update();
	
		return getUtility(offer) >= S;
	}

	private void update() {
		
		opponent_offers = this.m_list_opponent_offers;
		int t = opponent_offers.size();
		double calculo = 0;	
		double time = getTime();
		
		//Seguimos con nuestra filosof�a dura
		if (time < thresholdTimeInitial) {
			S = 1 - (1 - RU)*Math.pow(getTime(),1.0/beta);
		//Si tenemos suficientes ofertas para calcular el tit-tat
		} else if (t > delta && time > thresholdTimeInitial  && time < thresholdTimeFinal) {
			//Relativo
			//calculo = (1 - this.getUtility(opponent_offers.get(t-delta+1))) / (1 - this.getUtility(opponent_offers.get(t-delta)));
			//calculo *= this.getUtility(last_moment_offer);
			
			//Absoluto
			//calculo = this.getUtility(last_moment_offer) - this.getUtility(opponent_offers.get(t-delta+1))
			// - this.getUtility(opponent_offers.get(t-delta));
			
			//Promediado
			calculo = (1 - this.getUtility(opponent_offers.get(t-1))) / (1 - this.getUtility(opponent_offers.get(t-delta)));
			calculo *= this.getUtility(last_moment_offer);
			S = Math.min(1, Math.max(RU, calculo));
			
		// nos arrastramos a veer si nos quieren
		} else if (time > thresholdTimeFinal) {
			beta = 5;
			RU = time * RU;
			
			if (time > 0.95) {
				RU = (1 - time) * RU;
			}
			
			S = 1 - (1 - RU)*Math.pow(getTime(),1.0/beta);		
		}
			
	}

	public Bid proposeOffer() {			
	
			
			Vector<Bid> m_bids = getOffers(S , S + 0.1);
	
			Bid selected = m_bids.get(rand.nextInt(m_bids.size()));
			last_moment_offer = selected;
			
			return selected;
		
	}
}

