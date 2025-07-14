<center>

## StockPred - AI-Powered Stock Prediction

</center>

### The Challenge of Stock Market Volatility

Stock market prediction is an inherently complex problem, influenced by countless factors such as macroeconomic trends, corporate performance, investor sentiment, and global events. While traditional models attempt to capture these relationships, they often struggle with overfitting, data limitations, and an inability to adapt to real-time market fluctuations.

<center> 

<img src="static/imgs/market_volatility.png" alt="Stock market volatility visualization" width="600"> 

</center>

### StockPred — A novel approach at predicting stock prices

#### Intro
StockPred presents a novel approach at predicting stock prices. It implements a lightweight architecture inspired by LLMs to achieve surprisingly high accuracy.

#### Rationale
Why use an LLM inspired architecture?

The story is a bit long, but in short, I was watching a youtube video on how LLMs work, then thought that some parts of the LLM process like attention and the fact that you can input outputs back in to continously predict caught my interest, and I thought that it would be applicable to this project, something I was already working on. Turns out, it worked out much better than I thought it would.
#### Architecture
**Model:**
Ticker Embedding -> Input Projection -> Positional Embedding -> Transformer Encoder -> Output Head MLP
**Loss:**
Custom Directional MSE loss
**Data:**
- yfinance for finance data
- FRED for interest rate, GDP, inflation, unemployment, and volitility
#### Efficiency
The model is only has about 30M parameters big, making it very efficient and runnable on low-end GPUs and high-end CPUs. This makes it one of the most accessible stock prediction models out there, especially given its accuracy.
#### Accuracy
The latest trained model, model_20250714_053856, when tested over 4909 samples, returned:
- A directional accuracy of 90.65%
- A median R^2 score of 0.8732
- An R^2 score of 0.5887
All of these scores are well above the average for models of this size and the directional accuracy is also well above even larger models.
#### Limitations
However, the models come at limitations too:
- A RMSE of 418.98
- A MAPE of 127.63%
- Recursive predictions make the prediction accuracy exponentially worse. It is recommended you only predict for 5 days (the default horizon) for highest accuracy.
Despite having overall good accuracy, there are a few disasterously horrible predictions, leading to horrible predictions shown above. 
### Usage
You can use this model at:
- https://xild-stockpred.streamlit.app/

### Key Points
StockPred introduces several key benefits and innovations:

1. Model: The model bases itself off of LLM architecture, which is a relatively unexplored method for model architecture.
2. Effectiveness: The model boasts an 867.2% directional accuracy along with many other good metrics, many of which outstrip, as mentioned before, even better models.
3. Efficiency: This is possibly one of the smallest models with the highest accuracy, making it both accessible and proficient.

### Conclusion

StockPred serves as a research-driven proof of concept, not a financial advisory tool. It provides a testing ground for integrating AI models into stock prediction, assessing their strengths and limitations. The ultimate goal is to refine these methods and explore their potential applications in real-world financial analysis.
