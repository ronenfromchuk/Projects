import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, StringProperty


class DbGenWidget(Widget):
    airline_companies = ObjectProperty(None)
    customers = ObjectProperty(None)
    administrators = ObjectProperty(None)
    flights_per_company = ObjectProperty(None)
    tickets_per_customer = ObjectProperty(None)
    countries = ObjectProperty(None)
    alerts_label = StringProperty('')

    # root.btn() in kv file
    def btn(self):
        #self.add_widget(Label(text=f'Your details has been submitted!'))
        print("Airline Companies:", self.airline_companies.text,
              "Customers:", self.customers.text,
              "Administrators:", self.administrators.text,
              "Flights Per Company:", self.flights_per_company.text,
              "Tickets Per Customer:", self.tickets_per_customer.text)

    def switchstate1(self):
        self.ids.rbutton1.state = 'down'
        self.ids.rbutton2.state = 'normal'

    def switchstate2(self):
        self.ids.rbutton2.state = 'down'
        self.ids.rbutton1.state = 'normal'


class MyApp(App):
    def build(self):
        return DbGenWidget()


Builder.load_file('KvGUI.kv')

if __name__ == "__main__":
    MyApp().run()
