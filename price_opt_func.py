import pandas as pd

def price_opt_func(df):
    """Returns a dataframe with the 150th row nulls for each product filled in with predicted order values and optimized price values."""
    
    # initialize empty dataframe
    df_output = pd.DataFrame()

    # For loop to separate each product and find elasticity on the product level
    for x in df['product'].unique():
        
        # separates products and makes copy of df
        df_product = df[df['product'] == x]
        df_product = df_product.copy()
        
        # Creates a new groupby df to find average orders and cost by price
        df_g = pd.DataFrame(df_product.groupby('price')[['orders', 'cost']].mean()).reset_index()

        # Calculates percentage change of price and orders to calculate elasticity for each price difference
        df_g['price_diff_pct'] = df_g['price'].pct_change()
        df_g['order_diff_pct'] = df_g['orders'].pct_change()
        df_g['elasticity'] = df_g['order_diff_pct'] / df_g['price_diff_pct']
        elasticity = df_g['elasticity'].mean()

        # Find predicted order loss. Doing it this way because elasticity is measured on a percentage basis (1% increase in price == x% decrease in orders). 
        # However, the price changes in the data may not necessarily change in increments of 1%. 
        # Thus, elasticity must be scaled to the price changes in the data. (pred_order_loss)
        df_g['pred_order_loss'] = df_g['price_diff_pct'] * elasticity
        # Shifting up to calculate with average orders
        df_g['pred_order_loss'] = df_g['pred_order_loss'].shift(-1)

        # Making order predictions
        df_g['order_pred'] = (df_g['orders'] * df_g['pred_order_loss']) + df_g['orders']
        # Shifting down since pred_order_loss was shifted up previously
        df_g['order_pred'] = df_g['order_pred'].shift(1)
        df_g['pred_order_loss'] = df_g['pred_order_loss'].shift(1)
        # Replacing index 0 value in order_pred with orders.
        # This makes the assumption that, at the lowest price point, the elasticity model would accurately represent real orders.
        df_g['order_pred'][0] = df_g['orders'][0]

        # Predicted profit to find maximum/optimal
        df_g['profit_pred'] = (df_g['price'] - df_g['cost']) * df_g['order_pred']

        # Singling out the row at which profit is maximized
        max_profit_pred_row = df_g[df_g['profit_pred'] == df_g['profit_pred'].max()].reset_index()

        # Optimal price and day order predictions (values to be imputed)
        opt_price = max_profit_pred_row['price'][0]
        day_order_pred = max_profit_pred_row['order_pred'][0]

        # Imputation of values
        df_product['price'] = df_product['price'].fillna(opt_price)
        df_product['orders'] = df_product['orders'].fillna(day_order_pred)

        # Putting the dataframe back together
        df_output = pd.concat([df_output, df_product])
        
    return df_output