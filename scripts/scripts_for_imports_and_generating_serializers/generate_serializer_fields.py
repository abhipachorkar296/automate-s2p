s = """
invoice_id = models.AutoField(primary_key=True, editable=False)
    purchase_order_id = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    buyer_purchase_order_id = models.CharField(max_length=100)
    document_url = models.URLField(null=True, blank=True)
    created_by_user_id = models.ForeignKey(User, related_name="proforma_invoice_created_by_user_id", on_delete=models.CASCADE)
    invoice_creation_datetime = models.DateTimeField(auto_now_add=True)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    seller_comments = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=100)
    currency_code = models.ForeignKey(CurrencyCode, on_delete=models.CASCADE)
    amount_invoiced = models.DecimalField(max_digits=25, decimal_places=10)
    amount_paid = models.DecimalField(max_digits=25, decimal_places=10)
    closing_user_id_seller = models.ForeignKey(User, related_name="proforma_invoice_closing_user_id_seller",on_delete=models.CASCADE, null=True)
    closing_comment_seller = models.TextField(max_length=500, blank=True)
    closing_datetime_seller = models.DateTimeField(null=True)
    closing_user_id_buyer = models.ForeignKey(User, related_name="proforma_invoice_closing_user_id_buyer",on_delete=models.CASCADE, null=True)
    closing_comment_buyer = models.TextField(max_length=500, blank=True)
    closing_datetime_buyer = models.DateTimeField(null=True)
    invoice_close_datetime = models.DateTimeField(null=True)
"""
s = s.split("\n")
s = [i for i in s if len(i)!=0]
for i in range(len(s)):
    ind = s[i].find("=")
    if(ind!=-1):
        s[i] = s[i][:ind].strip()

print(s)