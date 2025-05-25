import gi

from entities.order import Order
from entities.product import Product
from entities.user import User
from mysql_connection import new_mysql_connection

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gdk, Gtk  # noqa: E402

connection = new_mysql_connection()


@Gtk.Template(filename="src/ui/main_window.ui")
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"

    split_view: Adw.NavigationSplitView = Gtk.Template.Child("split_view")
    nav_list: Gtk.ListBox = Gtk.Template.Child("nav_list")
    nav_users: Gtk.ListBoxRow = Gtk.Template.Child("nav_users")
    nav_products: Gtk.ListBoxRow = Gtk.Template.Child("nav_products")
    nav_orders: Gtk.ListBoxRow = Gtk.Template.Child("nav_orders")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize pages
        self.users_page = UsersPage()
        self.products_page = ProductsPage()
        self.orders_page = OrdersPage()

        # Connect signals
        self.nav_list.connect("row-activated", self.on_navigation)

        # Set initial view
        self.nav_users.activate()

    def on_navigation(self, list_box, row):
        # Update active styling
        if hasattr(self, "last_active_row"):
            self.last_active_row.remove_css_class("active")
        self.last_active_row = row
        row.add_css_class("active")

        # Switch pages
        if row == self.nav_users:
            self.split_view.set_content(self.users_page)
        elif row == self.nav_products:
            self.split_view.set_content(self.products_page)
        elif row == self.nav_orders:
            self.split_view.set_content(self.orders_page)


@Gtk.Template(filename="src/ui/users_page.ui")
class UsersPage(Adw.NavigationPage):
    __gtype_name__ = "UsersPage"

    users_list: Gtk.ListBox = Gtk.Template.Child("users_list")
    refresh_users_button: Gtk.Button = Gtk.Template.Child("refresh_users_button")

    def __init__(self):
        super().__init__()
        self.load_users()
        self.refresh_users_button.connect("clicked", lambda _: self.refresh())

    def refresh(self):
        # Clear and reload users
        self.users_list.remove_all()
        self.load_users()

    def load_users(self):
        users = User.list_all(connection)
        for user in users:
            rows = [
                BoxedListRow(f"{key}: {value}")
                for key, value in user.as_dict(True).items()
            ]

            # Add addresses
            user.load_addresses()
            for index, address in enumerate(user.addresses):
                address_rows = [
                    BoxedListRow(f"{key}: {value}")
                    for key, value in address.as_dict(True).items()
                ]
                rows.append(
                    BoxedListExpanderRow(
                        title=f"Endereço {index + 1}", rows=address_rows
                    )
                )

            # Add cart
            user.load_cart()
            if hasattr(user.cart, "products"):
                cart_rows = []
                for product in user.cart.products:
                    cart_rows.append(
                        BoxedListSpinRowWrapper(
                            title=product.name,
                            subtitle=f"Preço: {product.price}",
                            value=product.quantity,
                            max_value=product.available_on_stock,
                            on_change=lambda editable, u=user, p=product: self.on_product_quantity_changed(
                                editable, u, p
                            ),
                        ).spin_row
                    )
                cart_rows.append(
                    BoxedListActionRow(
                        title="Adicionar produto",
                        subtitle="Adicionar produto ao carrinho",
                        action=lambda _, u=user: self.add_product_dialog(u),
                    )
                )
                cart_rows.append(
                    BoxedListActionRow(
                        title="Finalizar pedido",
                        subtitle="Selecione o endereço e finalize seu pedido",
                        action=lambda _, u=user: self.select_address_for_order(u),
                    )
                )
                rows.append(BoxedListExpanderRow(title="Carrinho", rows=cart_rows))

            expander = BoxedListExpanderRow(title=user.name, rows=rows)
            self.users_list.append(expander)

    def select_address_for_order(self, user):
        addresses_list = BoxedList()
        scrollable_dialog = ScrollableDialog(
            title="Selecionar endereço",
            content=addresses_list,
        )

        # Add address selection
        for address in user.addresses:
            addresses_list.append(
                BoxedListActionRow(
                    title=f"{address.state} - {address.city}",
                    subtitle=f"{address.first_line}, {address.second_line}, {address.third_line}",
                    action=lambda _, d=scrollable_dialog, u=user, a=address: self.place_order(
                        d, u, a
                    ),
                )
            )

        scrollable_dialog.present()

    def place_order(self, dialog, user, address):
        # Create order
        total_price = 0
        for product in user.cart.products:
            total_price += product.price * product.quantity

        order = Order(0, total_price, user.id, address.id, connection)
        order.save()

        # Add products to order
        for product in user.cart.products:
            order.add_product(product.id, product.quantity)

        user.cart.clear()

        self.refresh()

        dialog.close()

    def on_product_quantity_changed(self, editable: Gtk.Editable, user, product):
        # Update product quantity in the cart
        new_quantity = editable.get_text()
        new_quantity = int(new_quantity) if new_quantity.isdigit() else 0
        if new_quantity > product.available_on_stock:
            new_quantity = product.available_on_stock

        user.cart.update_product_quantity(product.id, new_quantity)

    def add_product_dialog(self, user):
        product_list = BoxedList()

        dialog = ScrollableDialog(
            title="Adicionar produto ao carrinho",
            content=product_list,
        )

        # Add product selection
        products = Product.list_all(connection)
        for product in products:
            if user.cart.has_product(product.id):
                continue

            row = BoxedListActionRow(
                title=product.name,
                subtitle=f"Preço: {product.price}",
                action=lambda _, d=dialog, u=user, p=product: self.add_product_to_cart(
                    d, u, p.id
                ),
            )
            product_list.append(row)

        dialog.present()

    def add_product_to_cart(self, dialog, user, product_id):
        user.cart.add_product(product_id)

        self.refresh()

        dialog.close()


@Gtk.Template(filename="src/ui/products_page.ui")
class ProductsPage(Adw.NavigationPage):
    __gtype_name__ = "ProductsPage"

    products_list = Gtk.Template.Child("products_list")
    refresh_products_button = Gtk.Template.Child("refresh_products_button")

    def __init__(self):
        super().__init__()
        self.load_products()
        self.refresh_products_button.connect("clicked", lambda _: self.refresh())

    def refresh(self):
        # Clear and reload products
        self.products_list.remove_all()
        self.load_products()

    def load_products(self):
        products = Product.list_all(connection)
        for product in products:
            rows = [
                BoxedListRow(f"{key}: {value}")
                for key, value in product.as_dict(True).items()
            ]

            # Add categories
            product.load_categories()
            category_rows = []
            if len(product.categories) > 0:
                for category in product.categories:
                    category_rows.append(BoxedListRow(category.name))
                rows.append(
                    BoxedListExpanderRow(title="Categorias", rows=category_rows)
                )

            expander = BoxedListExpanderRow(title=product.name, rows=rows)
            self.products_list.append(expander)


@Gtk.Template(filename="src/ui/orders_page.ui")
class OrdersPage(Adw.NavigationPage):
    __gtype_name__ = "OrdersPage"

    orders_list = Gtk.Template.Child("orders_list")
    refresh_orders_button = Gtk.Template.Child("refresh_orders_button")

    def __init__(self):
        super().__init__()
        self.load_orders()
        self.refresh_orders_button.connect("clicked", lambda _: self.refresh())

    def refresh(self):
        # Clear and reload orders
        self.orders_list.remove_all()
        self.load_orders()

    def load_orders(self):
        orders = Order.list_all(connection)
        for order in orders:
            rows = [
                BoxedListRow(f"{key}: {value}")
                for key, value in order.as_dict(True).items()
            ]

            # Add user
            order.load_user()
            user_rows = []
            for key, value in order.user.as_dict(True).items():
                user_rows.append(BoxedListRow(f"{key}: {value}"))

            rows.append(BoxedListExpanderRow(title="Usuário", rows=user_rows))

            # Add products
            order.load_products()
            product_rows = []
            for product in order.products:
                product_rows.append(
                    BoxedListRow(
                        title=f"x{product.quantity} {product.name}",
                        subtitle=product.price * product.quantity,
                    )
                )
            rows.append(BoxedListExpanderRow(title="Produtos", rows=product_rows))

            # Add address
            order.load_address()
            address_rows = []
            for key, value in order.address.as_dict(True).items():
                address_rows.append(BoxedListRow(f"{key}: {value}"))
            rows.append(BoxedListExpanderRow(title="Endereço", rows=address_rows))

            expander = BoxedListExpanderRow(title=f"Pedido {order.id}", rows=rows)
            self.orders_list.append(expander)


class ScrollableDialog(Adw.Dialog):
    def __init__(self, title, content):
        super().__init__(title=title)
        self.set_content_width(600)
        self.set_content_height(800)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_spacing(20)

        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        footer_box.set_halign(Gtk.Align.END)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(content)
        scrolled_window.set_vexpand(True)

        close_button = Gtk.Button(label="Fechar")
        close_button.connect("clicked", lambda _: self.close())
        close_button.set_cursor(Gdk.Cursor.new_from_name("pointer"))

        main_box.append(scrolled_window)
        main_box.append(footer_box)

        footer_box.append(close_button)

        self.set_child(main_box)


class BoxedList(Gtk.ListBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_css_classes(["boxed-list"])
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_valign(Gtk.Align.START)


class BoxedListExpanderRow(Adw.ExpanderRow):
    def __init__(self, title, rows, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title)
        self.set_css_classes(["expander", "boxed-list-expander-row"])

        for row in rows:
            self.add_row(row)


class BoxedListRow(Adw.ActionRow):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)
        self.set_css_classes(["boxed-list-row"])
        self.set_title(title)


class BoxedListActionRow(Adw.ActionRow):
    def __init__(self, title, subtitle, action, **kwargs):
        super().__init__(**kwargs)
        self.set_css_classes(["boxed-list-action-row"])
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.set_activatable(True)
        self.connect("activated", action)


# This class is a wrapper for Adw.SpinRow
class BoxedListSpinRowWrapper:
    def __init__(self, title, subtitle, value, max_value, on_change=None):
        super().__init__()
        self.spin_row = Adw.SpinRow()
        self.spin_row.set_title(title)
        self.spin_row.set_subtitle(subtitle)
        self.spin_row.set_numeric(True)
        self.spin_row.set_adjustment(
            Gtk.Adjustment(lower=0, upper=max_value, step_increment=1)
        )
        self.spin_row.set_value(value)

        if on_change:
            self.spin_row.connect("changed", on_change)


def on_activate(app):
    # Load CSS
    css = Gtk.CssProvider()
    css.load_from_path("src/style.css")
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    window = MainWindow(application=app)
    window.present()


def main():
    app = Adw.Application(application_id="com.example.gui")
    app.connect("activate", on_activate)
    app.run(None)
