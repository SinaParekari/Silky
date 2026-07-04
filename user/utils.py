from order.models import Order

STATUS_GROUP_MAP = {
    Order.Status.PENDING: "در انتظار",
    Order.Status.PAID: "در انتظار",
    Order.Status.PROCESSING: "در انتظار",
    Order.Status.SHIPPED: "در حال ارسال",
    Order.Status.DELIVERED: "تحویل شد",
    Order.Status.CANCELLED: "لغو شد",
    Order.Status.FAILED: "لغو شد",
    Order.Status.RETURNED: "لغو شد",
    Order.Status.REFUNDED: "لغو شد",
}

def to_persian_digits(s):
    fa = "۰۱۲۳۴۵۶۷۸۹"
    return "".join(fa[int(c)] if c.isdigit() else c for c in str(s))

def format_amount(value):
    millions = value / 1_000_000
    if millions >= 1:
        text = f"{millions:.1f}".rstrip("0").rstrip(".") + "M"
    else:
        text = f"{value:,}"
    return to_persian_digits(text)

def build_order_row(order):
    first_item = order.items.first()
    item_count = order.items.count()
    if item_count > 1:
        product_label = f"{first_item.product_name} +{item_count - 1} مورد"
    elif first_item:
        product_label = first_item.product_name
    else:
        product_label = "-"

    return {
        "id": f"#ORD-{order.pk:03d}",
        "product": product_label,
        "date": to_persian_digits(order.created_at.strftime("%Y/%m/%d")),
        "amount": format_amount(order.final_price),
        "status":  order.get_status_display(),
    }

def get_orders_json(user):
    orders = (
        Order.objects.filter(user=user)
        .prefetch_related('items')
        .order_by('-created_at')
    )
    return [build_order_row(o) for o in orders]  # return the list, not json.dumps(...)