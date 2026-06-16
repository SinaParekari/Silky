from .models import Cart as CartDB, CartItem, Discount
from product.models import Product, ProductVariant


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = request.user

        if self.user.is_authenticated:
            # کاربر لاگین کرده - از دیتابیس
            self.db_cart, _ = CartDB.objects.get_or_create(user=self.user)
            self.use_db = True
        else:
            # کاربر لاگین نکرده - از سشن
            if 'cart' not in self.session:
                self.session['cart'] = {}
            self.session_cart = self.session['cart']
            self.use_db = False

    def add(self, product, variant, quantity=1, update_quantity=False):
        if self.use_db:
            # دیتابیس
            item, created = CartItem.objects.get_or_create(
                cart=self.db_cart,
                variant=variant,
                defaults={'product': product, 'quantity': 0}
            )
            if update_quantity:
                item.quantity = quantity
            else:
                item.quantity += quantity

            # چک موجودی
            if item.quantity > variant.stock:
                item.quantity = variant.stock

            item.save()
        else:
            # سشن
            key = f'{product.slug}-{variant.color}'
            if key not in self.session_cart:
                self.session_cart[key] = {
                    'product_id': product.id,
                    'name': product.name,
                    'slug': product.slug,
                    'color': variant.color,
                    'color_code': variant.color_code,
                    'price': str(variant.price),
                    'quantity': 0,
                    'image': product.main_image.image.url if product.main_image else '',
                }
            if update_quantity:
                self.session_cart[key]['quantity'] = quantity
            else:
                self.session_cart[key]['quantity'] += quantity

            if self.session_cart[key]['quantity'] > variant.stock:
                self.session_cart[key]['quantity'] = variant.stock

            self.save()

    def remove(self, key):
        if self.use_db:
            CartItem.objects.filter(cart=self.db_cart, id=key).delete()
        else:
            if key in self.session_cart:
                del self.session_cart[key]
                self.save()

    def update(self, key, quantity):
        if self.use_db:
            try:
                item = CartItem.objects.get(cart=self.db_cart, id=key)
                if quantity <= 0:
                    item.delete()
                else:
                    item.quantity = quantity
                    item.save()
            except CartItem.DoesNotExist:
                pass
        else:
            if key in self.session_cart:
                if quantity <= 0:
                    del self.session_cart[key]
                else:
                    self.session_cart[key]['quantity'] = quantity
                self.save()

    def clear(self):
        if self.use_db:
            self.db_cart.items.all().delete()
        else:
            self.session['cart'] = {}
            self.save()

    def save(self):
        self.session.modified = True

    def get_total(self):
        if self.use_db:
            return self.db_cart.get_total()
        return sum(
            int(item['price']) * item['quantity']
            for item in self.session_cart.values()
        )

    def get_total_after_discount(self, discount_amount=0):
        return max(0, self.get_total() - discount_amount)

    def __len__(self):
        if self.use_db:
            return len(self.db_cart)
        return sum(item['quantity'] for item in self.session_cart.values())

    def __iter__(self):
        if self.use_db:
            for item in self.db_cart.items.all():
                yield {
                    'key': item.id,
                    'name': item.product.name,
                    'slug': item.product.slug,
                    'color': item.variant.color,
                    'color_code': item.variant.color_code,
                    'price': item.variant.price,
                    'quantity': item.quantity,
                    'total_price': item.get_total_price(),
                    'image': item.product.main_image.image.url if item.product.main_image else '',
                }
        else:
            for key, item in self.session_cart.items():
                yield {
                    **item,
                    'key': key,
                    'total_price': int(item['price']) * item['quantity'],
                }