import json
from datetime import datetime
from collections import defaultdict
import logging

class StockAnalytics:
    def __init__(self, file_path):
        self.file_path = file_path
        self.orders = self.load_orders()
        self.total_cost = 0
        self.total_quantity = 0
        self.total_revenue = 0
        self.total_quantity_sold = 0
        self.average_purchase_price = 0
        self.average_sell_price = 0
        self.net_gain_per_share = 0
        self.total_net_gain = 0
        self.num_days = 0
        self.num_transactions = 0
        self.daily_profit = defaultdict(float)
        self.daily_transactions = defaultdict(int)
        self.daily_position = defaultdict(int)

        # Configure logging
        logging.basicConfig(filename='trading_log.log', level=logging.INFO)

    def load_orders(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def process_orders(self):
        order_dates = set()
        self.num_transactions = len(self.orders)

        sell_short_price_sum = 0
        sell_short_quantity_sum = 0
        buy_to_cover_price_sum = 0
        buy_to_cover_quantity_sum = 0

        # Reverse the order of orders
        self.orders.reverse()

        for order in self.orders:
            instruction = order["orderLegCollection"][0]["instruction"]
            order_id = order["orderId"]
            entered_time = order["enteredTime"]
            
            # Parse the date from enteredTime
            order_date = datetime.strptime(entered_time, "%Y-%m-%dT%H:%M:%S%z").date()

            order_strategy_type = order["orderStrategyType"]
            order_price = order["orderLegCollection"][0].get("price", 0)  # Get price if available
            order_quantity = order["orderActivityCollection"][0]["quantity"]

            order_log_msg = f"OrderId: {order_id}, Instruction: {instruction}, Quantity: {order_quantity}, Price: {order_price}, Position: {self.daily_position[order_date]}, StrategyType: {order_strategy_type}"

            order_dates.add(order_date)
            self.daily_transactions[order_date] += 1
            
            for activity in order["orderActivityCollection"]:
                if activity["executionType"] == "FILL":
                    quantity = activity["quantity"]
                    price = activity["executionLegs"][0]["price"]
                    
                    # if instruction == "BUY":
                    #     self.total_cost += quantity * price
                    #     self.total_quantity += quantity
                    #     self.daily_profit[order_date] -= quantity * price
                    #     self.daily_position[order_date] += quantity
                    # elif instruction == "SELL":
                    #     self.total_revenue += quantity * price
                    #     self.total_quantity_sold += quantity
                    #     self.daily_profit[order_date] += quantity * price
                    #     self.daily_position[order_date] -= quantity
                    if instruction == "SELL_SHORT" or instruction == "SELL":
                        self.total_revenue += quantity * price
                        self.total_quantity_sold += quantity
                        self.daily_profit[order_date] += quantity * price
                        self.daily_position[order_date] -= quantity
                        sell_short_price_sum += quantity * price
                        sell_short_quantity_sum += quantity
                    elif instruction == "BUY_TO_COVER" or instruction =="BUY":
                        self.total_cost += quantity * price
                        self.total_quantity += quantity
                        self.daily_profit[order_date] -= quantity * price
                        self.daily_position[order_date] += quantity
                        buy_to_cover_price_sum += quantity * price
                        buy_to_cover_quantity_sum += quantity

                    # Log order details
                    logging.info(f"Time: {entered_time}, {order_log_msg}")

            # Check if the order strategy type is "FLATTEN"
            if order_strategy_type == "FLATTEN":
                if sell_short_quantity_sum == buy_to_cover_quantity_sum and sell_short_quantity_sum > 0:
                    profit = (sell_short_price_sum / sell_short_quantity_sum) - (buy_to_cover_price_sum / buy_to_cover_quantity_sum)
                    profit *= sell_short_quantity_sum
                    logging.info(f"Time: {entered_time}, OrderId: {order_id}, StrategyType: {order_strategy_type}, Profit: {profit}")
                    sell_short_price_sum = 0
                    sell_short_quantity_sum = 0
                    buy_to_cover_price_sum = 0
                    buy_to_cover_quantity_sum = 0

        self.num_days = len(order_dates)
        self.calculate_analytics()

    def calculate_analytics(self):
        self.average_purchase_price = self.total_cost / self.total_quantity if self.total_quantity > 0 else 0
        self.average_sell_price = self.total_revenue / self.total_quantity_sold if self.total_quantity_sold > 0 else 0
        self.net_gain_per_share = self.average_sell_price - self.average_purchase_price
        self.total_net_gain = self.net_gain_per_share * self.total_quantity_sold

    def display_results(self):
        results = {
            "Total Shares Bought": self.total_quantity,
            "Total Shares Sold": self.total_quantity_sold,
            "Average Purchase Price": round(self.average_purchase_price, 4),
            "Average Sell Price": round(self.average_sell_price, 4),
            "Net Gain per Share": round(self.net_gain_per_share, 4),
            "Total Net Gain": round(self.total_net_gain, 2),
            "Number of Days": self.num_days,
            "Number of Transactions": self.num_transactions
        }
        for key, value in results.items():
            print(f"{key}: {value}")
        
        print("\nDaily Profits, Transactions, and Positions:")
        sorted_dates = sorted(self.daily_profit.keys())
        cumulative_position = 0
        for date in sorted_dates:
            daily_position = self.daily_position[date]
            cumulative_position += daily_position
            print(f"{date}: Profit: {round(self.daily_profit[date], 2)}, Transactions: {self.daily_transactions[date]}, Position: {cumulative_position}")


# Path to the JSON file
file_path = 'output/_orders.json'

# Create a StockAnalytics instance
stock_analytics = StockAnalytics(file_path)
stock_analytics.process_orders()
stock_analytics.display_results()
