# CS2 Trading Bot

An intelligent AI chatbot for CS2 trading that provides real-time pricing, pattern analysis, and market insights.

## Features

### Core AI Capabilities
- **Multi-Market Price Analysis**
  - Steam Market integration
  - Third-party marketplace price comparison
  - Real-time price updates and alerts

- **Trade Analysis & Recommendations**
  - Trade value comparison
  - Market trend analysis
  - Trade opportunity identification
  - Fair trade suggestions

- **Pattern Recognition & Valuation**
  - Pattern template identification
  - Pattern-specific overpay analysis
  - Rarity assessment
  - Historical pattern value tracking

- **Market Trend Analysis**
  - Price trend visualization
  - Future value projections
  - Market volatility analysis
  - Historical price charts

### Technical Features
- Real-time price updates
- Interactive charts and graphs
- Pattern template database
- Multi-market price aggregation
- Trade-up calculators
- Case ROI analysis
- Themed inventory suggestions
- Sticker craft recommendations

## Setup

1. Clone the repository
2. Set up the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   # Frontend (.env.local)
   OPENAI_API_KEY=your_openai_api_key
   NEXT_PUBLIC_API_URL=http://localhost:8000

   # Backend (.env)
   STEAM_API_KEY=your_steam_api_key
   DATABASE_URL=postgresql://user:password@localhost:5432/cs2bot
   ```

## Development

### Frontend
- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- Vercel AI SDK
- Chart.js for data visualization
- React Query for data fetching

### Backend
- FastAPI
- PostgreSQL
- Redis for caching
- Multiple LLM integration options:
  - OpenAI GPT-4 (primary)
  - Anthropic Claude (alternative)
  - Local LLM options (Llama 2, Mistral)

### Data Sources
- Steam Market API
- Third-party marketplaces
- Pattern template database
- Historical price data

## AI Capabilities

The chatbot is designed to be an expert CS2 trading assistant with the following capabilities:

1. **Price Intelligence**
   - Multi-market price comparison
   - Real-time price updates
   - Historical price analysis
   - Price trend prediction

2. **Trade Analysis**
   - Trade value comparison
   - Fair trade suggestions
   - Market opportunity identification
   - Risk assessment

3. **Pattern Recognition**
   - Pattern template identification
   - Pattern value analysis
   - Rarity assessment
   - Overpay recommendations

4. **Market Insights**
   - Trend visualization
   - Future value projections
   - Market volatility analysis
   - Investment recommendations

## License

MIT 