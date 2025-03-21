export interface PriceData {
  price: number;
  volume: number;
  listings: number;
  timestamp: string;
  source: string;
}

export interface PatternData {
  template: string;
  rarity: string;
  estimatedValue: number;
  overpay: number;
}

export interface TradeAnalysis {
  items: {
    name: string;
    price: number;
    pattern?: PatternData;
  }[];
  isFair: boolean;
  suggestedOverpay?: number;
  marketTrend?: string;
}

export interface MarketTrend {
  currentPrice: number;
  historicalPrices: PriceData[];
  predictedPrice?: number;
  confidence: number;
  timeframe: string;
} 