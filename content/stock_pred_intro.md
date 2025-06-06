<center>

## StockPred - AI-Powered Stock Prediction

</center>

### The Challenge of Stock Market Volatility

Stock market prediction is an inherently complex problem, influenced by countless factors such as macroeconomic trends, corporate performance, investor sentiment, and global events. While traditional models attempt to capture these relationships, they often struggle with overfitting, data limitations, and an inability to adapt to real-time market fluctuations.

<center> 

<img src="static/imgs/market_volatility.png" alt="Stock market volatility visualization" width="600"> 

</center>

Many existing prediction models focus solely on historical stock prices, ignoring crucial economic indicators and sentiment data that significantly impact market behavior. StockPred aims to explore how a hybrid AI-driven approach can enhance market forecasting by integrating deep learning, reinforcement learning, and sentiment analysis.

### StockPred and Its Structure

StockPred is a proof-of-concept project that experiments with AI techniques for stock prediction, testing their effectiveness in a realistic market setting. While not intended for direct financial decision-making, it provides a framework for exploring how AI can synthesize financial data, news sentiment, and technical indicators to generate stock trend predictions.

The pipeline consists of several experimental components:

1. Data Collection & Preprocessing:
    - Gathers historical stock prices, financial statements, and macroeconomic indicators from sources like Yahoo Finance, FRED, and other financial APIs.
    - Extracts and analyzes news sentiment to assess how media coverage influences stock movements.

2. Feature Engineering & Clustering:
    - Structures stock data into feature sets, including price history, trading volume, economic indicators, and sentiment scores.
    - Uses clustering techniques to identify similar market patterns for better generalization.

3. Hybrid Deep Learning Model (LSTM + Transformer):
    - Combines LSTMs for sequential trend detection and Transformer models for enhanced pattern recognition.
    - Implements a custom loss function that prioritizes directional accuracy over raw price prediction.

4. Sentiment & News Analysis:
    - NLP sentiment model for analyzing financial news sentiment.
    - Weighs sentiment data alongside quantitative stock indicators to adjust predictions dynamically.

5. Calculated Stock Values:
    - Instead of providing binary "buy/sell" recommendations, StockPred generates actual stock values.
    - This provides the user with more agency, as it predicts future prices instead of given assumptions for buying and selling.

You can try this program out here: [https://xild-stockpred.streamlit.app/](https://xild-stockpred.streamlit.app/)

### Innovations
StockPred introduces several experimental ideas in stock market forecasting:

1. Hybrid AI Approach: Tests the effectiveness of combining LSTMs and Transformers
2. Sentiment-Driven Adjustments: Evaluates how real-time financial news and investor sentiment influence market trends.
3. Multi-Source Data Fusion: Merges stock history, macroeconomic data, and sentiment analysis for a broader market perspective.

### Conclusion

StockPred serves as a research-driven proof of concept, not a financial advisory tool. It provides a testing ground for integrating AI models into stock prediction, assessing their strengths and limitations. The ultimate goal is to refine these methods and explore their potential applications in real-world financial analysis.
