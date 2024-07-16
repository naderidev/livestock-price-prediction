# Livestock Price Prediction in Iran

This project predicts livestock prices in Iran using a dataset of 31,534 entries spanning from **1392-01-01 to 1403-04-24** (Iranian calendar).

## Features

- Predicts livestock prices based on daily timestamps
- Uses data mined from [itpnews.com](https://www1.itpnews.com/)
- Provides price predictions with an error range

## Data Mining

The dataset is sourced from [itpnews.com](https://www1.itpnews.com/). To update the dataset:

1. Navigate to the `scrapping` directory
2. Run `main.py`

```python
python scrapping/main.py
```

## Usage

After running all cells in the notebook:

1. Call the `guess_the_price` function
2. Pass the desired date as arguments (year, month, day)

### Example

```python
predicted_price = guess_the_price(1403, 5, 10)
```

This returns an `int` value representing the predicted price for the given date.

### Error Range

The `mae_error` variable provides an error margin. To get a price range:

```python
lower_bound = predicted_price - mae_error
upper_bound = predicted_price + mae_error
```