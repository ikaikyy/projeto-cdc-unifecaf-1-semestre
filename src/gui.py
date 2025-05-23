import gi

from entities.product import Product
from entities.user import User
from mysql_connection import new_mysql_connection

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gdk, Gtk  # noqa: E402

connection = new_mysql_connection()


@Gtk.Template(filename='src/ui/main_window.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    split_view: Adw.NavigationSplitView = Gtk.Template.Child("split_view")
    nav_list: Gtk.ListBox = Gtk.Template.Child("nav_list")
    nav_users: Gtk.ListBoxRow = Gtk.Template.Child("nav_users")
    nav_products: Gtk.ListBoxRow = Gtk.Template.Child("nav_products")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize pages
        self.users_page = UsersPage()
        self.products_page = ProductsPage()

        # Connect signals
        self.nav_list.connect('row-activated', self.on_navigation)

        # Set initial view
        self.nav_users.activate()

    def on_navigation(self, list_box, row):
        # Update active styling
        if hasattr(self, 'last_active_row'):
            self.last_active_row.remove_css_class('active')
        self.last_active_row = row
        row.add_css_class('active')

        # Switch pages
        if row == self.nav_users:
            self.split_view.set_content(self.users_page)
        elif row == self.nav_products:
            self.split_view.set_content(self.products_page)


@Gtk.Template(filename='src/ui/users_page.ui')
class UsersPage(Adw.NavigationPage):
    __gtype_name__ = 'UsersPage'

    users_list = Gtk.Template.Child("users_list")

    def __init__(self):
        super().__init__()
        self.load_users()

    def load_users(self):
        self.users = User.list_all(connection)
        for user in self.users:
            rows = [[f"{key}: {value}", None] for key,
                    value in user.as_dict(True).items()]
            rows.append(
                ["Endereços", lambda _, u=user: self.show_user_addresses(u)])
            expander = BoxedListExpanderRow(label=user.name, rows=rows)
            self.users_list.append(expander)

    def show_user_addresses(self, user):
        user.load_addresses()
        addresses_list = BoxedList()
        for index, address in enumerate(user.addresses):
            rows = [[f"{key}: {value}", None] for key,
                    value in address.as_dict(True).items()]
            expander = BoxedListExpanderRow(
                label=f"Endereço {index + 1}", rows=rows)
            addresses_list.append(expander)
        dialog = ScrollableDialog(
            title=f"Endereços de {user.name}", content=addresses_list)
        dialog.present()


@Gtk.Template(filename='src/ui/products_page.ui')
class ProductsPage(Adw.NavigationPage):
    __gtype_name__ = 'ProductsPage'

    products_list = Gtk.Template.Child("products_list")

    def __init__(self):
        super().__init__()
        self.load_products()

    def load_products(self):
        products = Product.list_all(connection)
        for product in products:
            rows = [[f"{key}: {value}", None] for key,
                    value in product.as_dict(True).items()]
            expander = BoxedListExpanderRow(label=product.name, rows=rows)
            self.products_list.append(expander)


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
    def __init__(self, label, rows, **kwargs):
        super().__init__(title=label, **kwargs)
        self.set_css_classes(["expander", "boxed-list-expander-row"])

        for text, action in rows:
            if action:
                self.add_row(BoxedListRow(text, action))
            else:
                self.add_row(BoxedListRow(text))


class BoxedListRow(Adw.ActionRow):
    def __init__(self, text, action=None, **kwargs):
        super().__init__(**kwargs)
        self.set_css_classes(["boxed-list-row"])
        self.set_title(text)

        if action:
            self.set_activatable(True)
            self.connect('activated', action)


def on_activate(app):
    # Load CSS
    css = Gtk.CssProvider()
    css.load_from_path('src/style.css')
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    window = MainWindow(application=app)
    window.present()


def main():
    app = Adw.Application(application_id='com.example.gui')
    app.connect('activate', on_activate)
    app.run(None)


if __name__ == '__main__':
    main()
