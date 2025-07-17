import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import math

kivy.require('2.1.0')  # Ensure you are using an appropriate version

class CalculatorApp(App):
    def build(self):
        self.grid = GridLayout(cols=4)
        self.result = TextInput(font_size=32, readonly=True, halign='right', multiline=False)
        self.grid.add_widget(self.result)

        # Buttons for number system conversions
        self.grid.add_widget(Button(text="To Bin", on_press=self.convert_to_bin))
        self.grid.add_widget(Button(text="To Oct", on_press=self.convert_to_oct))
        self.grid.add_widget(Button(text="To Hex", on_press=self.convert_to_hex))
        self.grid.add_widget(Button(text="To Dec", on_press=self.convert_to_dec))

        # Buttons for mode selection
        self.mode_label = Label(text="Select Mode", font_size=32)
        self.grid.add_widget(self.mode_label)
        self.grid.add_widget(Button(text="Dec", on_press=self.set_mode))
        self.grid.add_widget(Button(text="Bin", on_press=self.set_mode))
        self.grid.add_widget(Button(text="Oct", on_press=self.set_mode))
        self.grid.add_widget(Button(text="Hex", on_press=self.set_mode))

        # Basic Calculator buttons
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
        ]

        # Adding hexadecimal buttons (a to f)
        hex_buttons = ['a', 'b', 'c', 'd', 'e', 'f']

        # Adding number and hex buttons to the grid
        for button in buttons + hex_buttons:
            self.grid.add_widget(Button(text=button, on_press=self.on_button_press))

        # Adding Clear and Backspace buttons
        self.grid.add_widget(Button(text="Clear", on_press=self.clear_text))
        self.grid.add_widget(Button(text="Backspace", on_press=self.backspace_text))

        self.current_base = None  # Initially no base selected
        return self.grid

    def set_mode(self, instance):
        mode = instance.text

        if mode == "Dec":
            self.current_base = 10
            self.mode_label.text = "Mode: Decimal"
        elif mode == "Bin":
            self.current_base = 2
            self.mode_label.text = "Mode: Binary"
        elif mode == "Oct":
            self.current_base = 8
            self.mode_label.text = "Mode: Octal"
        elif mode == "Hex":
            self.current_base = 16
            self.mode_label.text = "Mode: Hexadecimal"

    def convert_to_bin(self, instance):
        try:
            num = int(self.result.text, self.current_base)  # Convert based on current base
            self.result.text = bin(num)[2:]  # Convert to binary and update result
        except ValueError:
            self.result.text = "Error"

    def convert_to_oct(self, instance):
        try:
            num = int(self.result.text, self.current_base)
            self.result.text = oct(num)[2:]  # Convert to octal and update result
        except ValueError:
            self.result.text = "Error"

    def convert_to_hex(self, instance):
        try:
            num = int(self.result.text, self.current_base)
            self.result.text = hex(num)[2:]  # Convert to hexadecimal and update result
        except ValueError:
            self.result.text = "Error"

    def convert_to_dec(self, instance):
        try:
            num = int(self.result.text, self.current_base)
            self.result.text = str(num)  # Convert to decimal and update result
        except ValueError:
            self.result.text = "Error"

    def on_button_press(self, instance):
        if self.current_base is None:
            self.result.text = "Select Mode First"
            return

        current = self.result.text
        button_text = instance.text

        if button_text == "=":
            try:
                if self.current_base == 10:
                    result = self.decimal_calculation(current)  # For decimal calculation
                elif self.current_base == 2:
                    result = self.binary_calculation(current)  # For binary
                elif self.current_base == 8:
                    result = self.octal_calculation(current)  # For octal
                elif self.current_base == 16:
                    result = self.hexadecimal_calculation(current)  # For hexadecimal
                self.result.text = str(result)
            except Exception as e:
                self.result.text = "Error"
        else:
            self.result.text += button_text

    def decimal_calculation(self, expression):
        try:
            # Split the expression by operator
            if '+' in expression:
                num1, num2 = expression.split('+')
                result = int(num1) + int(num2)
            elif '-' in expression:
                num1, num2 = expression.split('-')
                result = int(num1) - int(num2)
            elif '*' in expression:
                num1, num2 = expression.split('*')
                result = int(num1) * int(num2)
            elif '/' in expression:
                num1, num2 = expression.split('/')
                num1, num2 = int(num1), int(num2)
                if num2 != 0:
                    result = num1 / num2  # Normal division
                else:
                    return "Error: Division by zero"
            else:
                result = "Error"
            return result
        except ValueError:
            return "Error"

    def binary_calculation(self, expression):
        try:
            if '+' in expression:
                num1, num2 = expression.split('+')
                result = bin(int(num1, 2) + int(num2, 2))[2:]
            elif '-' in expression:
                num1, num2 = expression.split('-')
                result = bin(int(num1, 2) - int(num2, 2))[2:]
            elif '*' in expression:
                num1, num2 = expression.split('*')
                result = bin(int(num1, 2) * int(num2, 2))[2:]
            elif '/' in expression:
                num1, num2 = expression.split('/')
                if int(num2, 2) != 0:
                    result = bin(int(num1, 2) // int(num2, 2))[2:]
                else:
                    return "Error"
            else:
                result = "Error"
            return result
        except ValueError:
            return "Error"

    def octal_calculation(self, expression):
        try:
            if '+' in expression:
                num1, num2 = expression.split('+')
                result = oct(int(num1, 8) + int(num2, 8))[2:]
            elif '-' in expression:
                num1, num2 = expression.split('-')
                result = oct(int(num1, 8) - int(num2, 8))[2:]
            elif '*' in expression:
                num1, num2 = expression.split('*')
                result = oct(int(num1, 8) * int(num2, 8))[2:]
            elif '/' in expression:
                num1, num2 = expression.split('/')
                if int(num2, 8) != 0:
                    result = oct(int(num1, 8) // int(num2, 8))[2:]
                else:
                    return "Error"
            else:
                result = "Error"
            return result
        except ValueError:
            return "Error"

    def hexadecimal_calculation(self, expression):
        try:
            if '+' in expression:
                num1, num2 = expression.split('+')
                result = hex(int(num1, 16) + int(num2, 16))[2:]
            elif '-' in expression:
                num1, num2 = expression.split('-')
                result = hex(int(num1, 16) - int(num2, 16))[2:]
            elif '*' in expression:
                num1, num2 = expression.split('*')
                result = hex(int(num1, 16) * int(num2, 16))[2:]
            elif '/' in expression:
                num1, num2 = expression.split('/')
                if int(num2, 16) != 0:
                    result = hex(int(num1, 16) // int(num2, 16))[2:]
                else:
                    return "Error"
            else:
                result = "Error"
            return result
        except ValueError:
            return "Error"

    def clear_text(self, instance):
        self.result.text = ""

    def backspace_text(self, instance):
        self.result.text = self.result.text[:-1]


if __name__ == '__main__':
    CalculatorApp().run()
