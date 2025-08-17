from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDTextButton

from services.api import ApiClient
from services.i18n import I18N


class HomeScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class AppRoot(ScreenManager):
    pass


KV = """
<AppRoot>:
    HomeScreen:
        name: "home"
    LoginScreen:
        name: "login"

<HomeScreen>:
    MDBoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: app.t("app_title")
            left_action_items: [["account", lambda x: app.go_login()]]
        ScrollView:
            MDList:
                id: matches_list

<LoginScreen>:
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)
        MDToolbar:
            title: app.t("login")
            left_action_items: [["arrow-left", lambda x: app.go_home()]]
        MDTextField:
            id: email
            hint_text: app.t("email")
        MDTextField:
            id: password
            hint_text: app.t("password")
            password: True
        MDRaisedButton:
            text: app.t("login")
            on_release: app.handle_login(email.text, password.text)
        MDTextButton:
            text: app.t("register")
            on_release: app.handle_register(email.text, password.text)
"""


class PredictionsApp(MDApp):
    def build(self):
        self.i18n = I18N(default_locale="tr")
        self.api = ApiClient()
        self.root = Builder.load_string(KV)
        return self.root

    def on_start(self):
        self.load_matches()

    def t(self, key: str) -> str:
        return self.i18n.t(key)

    def go_login(self):
        self.root.current = "login"

    def go_home(self):
        self.root.current = "home"

    def handle_register(self, email: str, password: str):
        try:
            self.api.register(email, password)
            Snackbar(text="Kayıt başarılı.").open()
        except Exception as e:
            Snackbar(text=f"Hata: {e}").open()

    def handle_login(self, email: str, password: str):
        try:
            token = self.api.login(email, password)
            self.api.set_token(token)
            Snackbar(text="Giriş başarılı.").open()
            self.go_home()
            self.load_matches()
        except Exception as e:
            Snackbar(text=f"Hata: {e}").open()

    def load_matches(self):
        try:
            data = self.api.list_matches()
            lst = self.root.get_screen("home").ids.matches_list
            lst.clear_widgets()
            for m in data:
                subtitle = self._compose_match_subtitle(m)
                item = TwoLineListItem(
                    text=f"{m['home_team']} - {m['away_team']}",
                    secondary_text=subtitle,
                )
                lst.add_widget(item)
        except Exception as e:
            Snackbar(text=f"Hata: {e}").open()

    def _compose_match_subtitle(self, m: dict) -> str:
        lab = self.t("premium") if m.get("is_premium") else self.t("free")
        if m.get("prediction"):
            tip = m["prediction"]["tip_value"]
            return f"{m['league']} | {lab} | {self.t('tip')}: {tip}"
        else:
            return f"{m['league']} | {lab} | {self.t('prediction_hidden')}"


if __name__ == "__main__":
    PredictionsApp().run()
