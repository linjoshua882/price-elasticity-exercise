# price-elasticity-exercise

This task was to find the optimal price for day 150 for each of the 250 products in the attached dataset- optimal price being defined as the price that would result in the maximum profit for a given day. Profit is defined as (price - cost) * orders. To reference exploratory code, please refer to the draft_code.ipynb jupyter notebook in the attached files. The final written function is both at the bottom of the jupyter notebook as well as in the price_opt_func.py file.

Initially, I wanted to explore the data to see if there were any patterns worth noting both at the category and product levels. I started by calculating daily profit for the whole dataset, and created scatter plots for each category. The scatter plots had price on the x axis, and orders on the y axis, and color hues dependent on daily profit. These scatter plots were meant to show any price/order pattern behavior, as well as showing where the most profitable areas were. The most profitable days tended to ride the top curve of the scatter plots. These indicated the days with the highest orders at those price points. I was tempted to use that curve as the measure of optimized price. However, I realized that within the same categories, it is likely that there are different products with different levels of customer perceived value. Thus, pricing every product in the category at that curve may not be 
optimal. 

![category scatter plot](https://github.com/linjoshua882/price-elasticity-exercise/blob/main/assets/scatter_price_orders_cat0.png)

So, I decided to explore further at the product level.

![prod scatter plot](https://github.com/linjoshua882/price-elasticity-exercise/blob/main/assets/scatter_prod_cat_2.png)

To do this, I selected one product from each category to examine on a deeper level. I noticed clusters that indicated price banding, as well as a similar pattern to the category scatter plots in regards to the price/orders relationship as well as the distribution of profitability on the plots. High daily profit levels tended to be near the median or near the maximum of the price range. I also noticed that the patterns on every scatter plot at the product level were slightly different- indicating that each product has a different type of customer behavior, levels of perceived value, and price ranges. This is where I decided to calculate price elasticity at the product level.

This was my plan:
1. Calculate price elasticity at the product level for each difference in price, using a
dataframe that is grouped by price and average orders at each price point
2. Calculate the mean elasticity and use it as a “slope” to generalize and predict orders at
different price points
3. Use predicted orders and price to calculate a predicted daily profit
4. Find the price and predicted orders at max daily predicted profit
5. Impute price and predicted orders into an aggregated dataframe

I created a dataframe with a single product to work on this process- I knew if I could effectively predict optimal price and orders on one product, I would be able to generalize it to the rest of the dataframe. I went through the plan above, and it worked successfully.
Here is the in-depth process of the price optimization function that I developed:

The price optimization function takes in any dataframe with the columns similar to the dataframe provided. It initializes an empty separate dataframe that ends up being the output- because when I decide to separate the dataframe into different products, once I fill in the nulls, I will need to concatenate all of the product dataframes together. I use a for loop to separate the dataframes by product name. From there, I create a new groupby dataframe to find average orders and cost by price. I then calculate the percentage difference for each row of the price and orders columns so that I can calculate elasticity at every price point.

This was the major conceptual roadblock I had encountered. An elasticity value (e.g -3) is applied on a percentage basis: 1% increase in price is equal to an x% decrease in orders. The price differences of each row in the dataset did not equate necessarily to a 1% increase at each interval. So, I needed to scale elasticity for each row to account for the percentage price change differences. This gave me an opportunity to use these new values that I called ‘pred_order_loss’ to calculate predicted orders at each price point. From there, I was able to use the formula of (price - cost) * predicted orders to calculate a predicted profit in dollars at each price point.

By identifying the maximum predicted profit, we are able to find a price point that would be optimal, and the predicted orders that would be the result of that price point. After imputing the nulls with my predicted and optimized values, I was able to then concatenate each product-separated dataframe onto the initialized empty dataframe at the beginning of the function, thus returning the whole original dataframe with the nulls replaced.

![predicted profit and orders by price elasticity](https://github.com/linjoshua882/price-elasticity-exercise/blob/main/assets/line_pred_profit_pred_orders.png)

If I had more time and more experience, I would pursue the use of a recurrent neural network or some time series predictive model to better account for order predictions. I think that this optimization model could be better if I could figure out a way to implement integration with other factors that I think affect orders, such as review count, rating (in stars), brand strength, and other external variables. This model makes the assumption that price is the only factor that affects orders. This model also cannot account for sudden demand changes as a result of external variables. However, I think given the time that I spent on this, and the fact that on the Amazon marketplace, price is a huge factor when customers make purchasing decisions, I think this model is acceptable for what it is.
