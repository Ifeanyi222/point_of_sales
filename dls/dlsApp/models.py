from django.db import models



#This model will handle sales transactions, linking the sale to the products sold.
class Sale(models.Model):
    sale_date = models.DateTimeField(auto_now_add=True)  # Date and time of the sale
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total sale amount
    cashier = models.CharField(max_length=255)  # Name or ID of the cashier handling the sale
    customer_name = models.CharField(max_length=255, blank=True, null=True)  # Customer's name
    customer_address = models.TextField(blank=True, null=True)  # Customer's address

    def __str__(self):
        return f"Sale {self.id} - {self.sale_date}"

    def get_receipt_data(self):
        """
        Generate receipt data for printing or exporting.
        """
        receipt_items = self.items.all()  # Related sale items
        item_details = [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.price_per_item,
                "total_price": item.get_total_price(),
            }
            for item in receipt_items
        ]
        return {
            "sale_id": self.id,
            "sale_date": self.sale_date,
            "customer_name": self.customer_name,
            "customer_address": self.customer_address,
            "cashier": self.cashier,
            "total_amount": self.total_amount,
            "items": item_details,
        }



#This model will store information about the products available for sale
class Product(models.Model):
    name = models.CharField(max_length=255)  # Product name
    description = models.TextField(blank=True, null=True)  # Optional product description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    stock_quantity = models.PositiveIntegerField()  # Available stock
    sku = models.CharField(max_length=50, unique=True)  # Stock Keeping Unit (unique product identifier)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the product is added
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

    def __str__(self):
        return self.name
    

#This model will handle the relationship between a sale and the products sold in that sale
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")  # Link to the sale
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the product
    quantity = models.PositiveIntegerField()  # Quantity of the product sold
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)  # Price per item (in case of discounts)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.price_per_item

#For managing inventory changes like restocking or correcting errors
class StockAdjustment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the product
    quantity = models.IntegerField()  # Positive for restock, negative for deductions
    reason = models.TextField()  # Reason for the adjustment
    adjusted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for the adjustment

    def __str__(self):
        return f"Adjustment for {self.product.name}"
    
#for expense incurred
class Expense(models.Model):
    description = models.CharField(max_length=255)  # Short description of the expense
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Expense amount
    incurred_at = models.DateTimeField(auto_now_add=True)  # Timestamp for the expense

    def __str__(self):
        return self.description


