import wx
import requests
from datetime import datetime
from Country import Country
from Currency import Currency
from CurrencySymbol import CurrencySymbol, Currency_Symbols, Currency_Symbol_Codes
from APIKey import APIKey

class CurrencyConverter(wx.Frame):
    def __init__(self, *args, **kw) -> None:
        super(CurrencyConverter, self).__init__(*args, **kw)

        # Create the Panel to contain the widgets
        self.panel = wx.Panel(self)

        # Create the Horizontal BoxSizer to use for the frame, input/output, and buttons
        self.Horizontal_Boxsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Call functions
        self.App_Amount_Input()
        self.App_From_Currency_Choices()
        self.App_To_Currency_Choices()
        self.App_Texts()
        self.Convert_Button()
        self.Swap_Button()
        self.Currenct_Date()

        # Bind the close click to show the Copyright message
        self.Bind(wx.EVT_CLOSE, self.CopyRight)

    def App_Texts(self):
        # Initialize the labels, add to horizontal_Boxsizer, and set positions
        self.Currency_Codes_Top = wx.StaticText(self.panel, label = "$  ¢  €  £  ¥  ₩  ₽  ₹  ₱  ₦  ₮   ៛  ₫  ₭  ₲  ₴  ₵")     # Initialize the first line of currency codes label to be above the title
        self.Horizontal_Boxsizer.Add(self.Currency_Codes_Top, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Currency_Codes_Top.SetPosition(wx.Point(170, 20))                                                          # Set its position to be above the title

        self.Currency_Codes_Bottom = wx.StaticText(self.panel, label = "﷼  ₡  L  J$  лв  C$  lei  ฿  ₴  $U  ₫  Z$  ₨  ௹  ৲")     # Initialize the second line of currency codes label to be under the title
        self.Horizontal_Boxsizer.Add(self.Currency_Codes_Bottom, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Currency_Codes_Bottom.SetPosition(wx.Point(170, 120))                                                          # Set its position to be under the title

        self.Title_Label = wx.StaticText(self.panel, label = "Worldwide Currency Converter")             # Initialize the title label
        self.Horizontal_Boxsizer.Add(self.Title_Label, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Title_Label.SetPosition(wx.Point(170, 60))                                                          # Set its position to be at the top in between the the first and second currency codes
        
        self.Amount_label = wx.StaticText(self.panel, label = "Amount")                                 # Initialize the Amount label
        self.Horizontal_Boxsizer.Add(self.Amount_label, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Amount_label.SetPosition(wx.Point(25, 175))                                                          # Set its position

        self.From_label = wx.StaticText(self.panel, label = "From")                                 # Initialize the From label
        self.Horizontal_Boxsizer.Add(self.From_label, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.From_label.SetPosition(wx.Point(375, 175))                                                          # Set its position

        self.To_label = wx.StaticText(self.panel, label = "To")                                     # Initialize the To label
        self.Horizontal_Boxsizer.Add(self.To_label, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.To_label.SetPosition(wx.Point(775, 175))                                                          # Set its position

        self.From_Result = wx.StaticText(self.panel, label = "")                                    # Initialize the From_Result label to display the amount from the first currency
        self.Horizontal_Boxsizer.Add(self.From_Result, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.From_Result.SetPosition(wx.Point(25, 255))                                                          # Set its position

        self.To_Result = wx.StaticText(self.panel, label = "")                                      # Initialize the To_Result label to display the amount equivalent in the second currency
        self.Horizontal_Boxsizer.Add(self.To_Result, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.To_Result.SetPosition(wx.Point(25, 285))                                                          # Set its position

        self.Currently = wx.StaticText(self.panel, label = "")                                      # Initialize the current time label 
        self.Horizontal_Boxsizer.Add(self.Currently, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Currently.SetPosition(wx.Point(25, 400))                                                          # Set its position

        self.First_Coin = wx.StaticText(self.panel, label = "")                                    # Initialize the First_Coin label to display how much 1 coin in the first currency is equivalent to in the second currency
        self.Horizontal_Boxsizer.Add(self.First_Coin, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.First_Coin.SetPosition(wx.Point(25, 335))                                                          # Set its position

        self.Second_Coin = wx.StaticText(self.panel, label = "")                                   # Initialize the Second_Coin label to display how much 1 coin in the second currency is equivalent to in the first currency
        self.Horizontal_Boxsizer.Add(self.Second_Coin, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Second_Coin.SetPosition(wx.Point(25, 355))                                                          # Set its position

        self.Copyright = wx.StaticText(self.panel, label = "Copyright © 2024 Abdul Karim Tamim. All rights reserved")       # Initialize the Copyright label
        self.Horizontal_Boxsizer.Add(self.Copyright, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Copyright.SetPosition(wx.Point(822, 400))                                                          # Set its position

        self.First_Box = wx.Panel(self.panel, size = (327, 32), style = wx.SIMPLE_BORDER)                       # Initialize the First_Box label for a better feature to be around the amount input
        self.Horizontal_Boxsizer.Add(self.First_Box, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.First_Box.SetPosition(wx.Point(22, 199))                                                          # Set its position

        self.Second_Box = wx.Panel(self.panel, size = (352, 32), style = wx.SIMPLE_BORDER)                       # Initialize the Second_Box label for a better feature to be around the From_Currency_Choices
        self.Horizontal_Boxsizer.Add(self.Second_Box, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Second_Box.SetPosition(wx.Point(374, 199))                                                          # Set its position
        
        self.Third_Box = wx.Panel(self.panel, size = (352, 32), style = wx.SIMPLE_BORDER)                       # Initialize the First_Box label for a better feature to be around the To_Currency_Choices
        self.Horizontal_Boxsizer.Add(self.Third_Box, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Third_Box.SetPosition(wx.Point(774, 199))                                                          # Set its position

        # Set size and font for the Amount_label, From_label, and To_label labels
        Size_Font = wx.Font(15, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_NORMAL, style = wx.FONTSTYLE_NORMAL)       # Size 15, Roman font, Normal wight, Normal style
        self.Amount_label.SetFont(Size_Font)
        self.From_label.SetFont(Size_Font)
        self.To_label.SetFont(Size_Font)

        # Set size and font for the From_Result
        Size_Font_From_Result = wx.Font(15, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_BOLD, style = wx.FONTSTYLE_NORMAL)       # Size 15, Roman font, Bold wight, Normal style
        self.From_Result.SetFont(Size_Font_From_Result)

        # Set size and font for the To_Result
        Size_Font_To_Result = wx.Font(25, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_BOLD, style = wx.FONTSTYLE_NORMAL)       # Size 25, Roman font, Bold wight, Normal style
        self.To_Result.SetFont(Size_Font_To_Result)

        # Set size and font for First_Coin and Second_Coin
        Size_Font_Coins = wx.Font(10, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_BOLD, style = wx.FONTSTYLE_NORMAL)       # Size 10, Roman font, Bold wight, Normal style
        self.First_Coin.SetFont(Size_Font_Coins)
        self.Second_Coin.SetFont(Size_Font_Coins)

        # Set size and font for the Title_Label
        Size_Font_Title_Label = wx.Font(35, family = wx.FONTFAMILY_MODERN, weight = wx.FONTWEIGHT_BOLD, style = wx.FONTSTYLE_NORMAL)       # Size 35, Modern font, Bold wight, Normal style
        self.Title_Label.SetFont(Size_Font_Title_Label)

        # Set size and font for the Current time
        Size_Font_Currently = wx.Font(12, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_BOLD, style = wx.FONTSTYLE_NORMAL)       # Size 12, Roman font, Bold wight, Normal style
        self.Currently.SetFont(Size_Font_Currently)

        # Set size and font for the Currency_Codes
        Size_Font_Currency_Codes = wx.Font(20, family = wx.FONTFAMILY_MODERN, weight = wx.FONTWEIGHT_BOLD, style = wx.FONTSTYLE_NORMAL)       # Size 20, Modern font, Bold wight, Normal style
        self.Currency_Codes_Top.SetFont(Size_Font_Currency_Codes)
        self.Currency_Codes_Bottom.SetFont(Size_Font_Currency_Codes)

        # Set the colors
        self.panel.SetBackgroundColour(wx.Colour(255, 255, 255))                # Set the panel color to white
        self.From_Result.SetForegroundColour(wx.Colour(100, 100, 100))                # Set the From_Result color to gray
        self.Currency_Codes_Top.SetForegroundColour(wx.Colour(102, 178, 255))                # Set the Currency_Codes_Top color to light blue
        self.Currency_Codes_Bottom.SetForegroundColour(wx.Colour(255, 51, 51))                      # Set the Currency_Codes_Bottom color to red

    def Currenct_Date(self):
        # Initialize the current time using the datetime library and set Currently label to the Date
        now = datetime.now()
        Date = f"Last Updated{now: %A, %B %d, %Y, %I:%M %p} PST"
        self.Currently.SetLabel(Date)       

    def App_Amount_Input(self):
        # Create the amount text input, add to horizontal_Boxsizer, and set positions
        self.Amount_input = wx.TextCtrl(self.panel, size = (285, 30))                                    # Create the Amount_input input to accepts integers for the Amount
        self.Horizontal_Boxsizer.Add(self.Amount_input, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Amount_input.SetPosition(wx.Point(63, 200))                                                          # Set its position
        
        # Set size and font for the Amount text input
        Size_Font = wx.Font(15, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_NORMAL, style = wx.FONTSTYLE_NORMAL)       # Size 15, Roman font, Normal wight, Normal style
        self.Amount_input.SetFont(Size_Font)
    
    def App_From_Currency_Choices(self):
        currencySymbol = CurrencySymbol()         # Initialize the returned currency symbols from CurrencySymbol() function to currencySymbol, from the imported CurrencySymbol file
        currency = Currency()                   # Initialize the returned currencies from Currency() function to currency, from the imported Currency file
        country = Country()                   # Initialize the returned Countries from Country() function to country, from the imported Country file

        self.choices = [f"{currencySymbol} - {currency} ({country})" for currencySymbol, currency, country in zip(currencySymbol, currency, country)]       # Initialize choices to "currencySymbol - currency (country)"

        # Create the From_currency_choices ComboBox, add to horizontal_Boxsizer, and set positions
        self.From_currency_choices = wx.ComboBox(self.panel, value = "Select", choices = self.choices, style = wx.CB_DROPDOWN, size = (350, -1))      # Create the From_currency_choices ComboBox and add the all choices
        self.Horizontal_Boxsizer.Add(self.From_currency_choices, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.From_currency_choices.SetPosition(wx.Point(375, 200))                                                          # Set its position

        # Bind the chosen currency to display the currency's code
        self.From_currency_choices.Bind(wx.EVT_COMBOBOX, self.Currency_Codes)

        # Set size and font for From_currency_choices
        Size_Font = wx.Font(15, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_NORMAL, style = wx.FONTSTYLE_NORMAL)       # Size 15, Roman font, Normal wight, Normal style
        self.From_currency_choices.SetFont(Size_Font)

    def App_To_Currency_Choices(self):
        currencySymbol = CurrencySymbol()         # Initialize the returned currency symbols from CurrencySymbol() function to currencySymbol, from the imported CurrencySymbol file
        currency = Currency()                   # Initialize the returned currencies from Currency() function to currency, from the imported Currency file
        country = Country()                   # Initialize the returned Countries from Country() function to country, from the imported Country file

        choices = [f"{currencySymbol} - {currency} ({country})" for currencySymbol, currency, country in zip(currencySymbol, currency, country)]       # Initialize choices to "currencySymbol - currency (country)"

        self.To_currency_choices = wx.ComboBox(self.panel, value = "Select", choices = choices, style = wx.CB_DROPDOWN, size = (350, -1))      # Create the To_currency_choices ComboBox and add the all choices
        self.Horizontal_Boxsizer.Add(self.To_currency_choices, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.To_currency_choices.SetPosition(wx.Point(775, 200))                                                          # Set its position

        # Set size and font for To_currency_choices
        Size_Font = wx.Font(15, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_NORMAL, style = wx.FONTSTYLE_NORMAL)       # Size 15, Roman font, Normal wight, Normal style
        self.To_currency_choices.SetFont(Size_Font)

    def Currency_Codes(self, evt):
        # Create the code TextCtrl, add to horizontal_Boxsizer, set position, and display the code of the currency chosen
        self.Code = wx.TextCtrl(self.panel, style = wx.TE_READONLY, size = (40, 30))                                    # Create the Code readonly input to accepts display the code of the currency chosen from
        self.Horizontal_Boxsizer.Add(self.Code, 0, wx.EXPAND | wx.ALL, border = 10)                           # Add to Horizontal_Boxsizer
        self.Code.SetPosition(wx.Point(23, 200))                                                          # Set its position

        From_Currency = self.From_currency_choices.GetValue()           # Get the currency of From_currency_choices chosen and store it in From_Currency
        From_Currency_Symbol = From_Currency.split()[0]             # Get the currency symbol of From_Currency and store it in From_Currency_Symbol
        
        Currency_Symbols_ = Currency_Symbols()         # Initialize the returned currency symbols from Currency_Symbols() function to Currency_Symbols_, from the imported CurrencySymbol file
        Symbol_Codes = Currency_Symbol_Codes()         # Initialize the returned currency codes from Currency_Symbol_Codes() function to Symbol_Codes, from the imported CurrencySymbol file
        
        # For loop to check every currency symbol and attach the correct currency code to it
        for i in range(len(Currency_Symbols_)):
            if From_Currency_Symbol == Currency_Symbols_[i]:
                if len(Symbol_Codes[i]) == 3 or len(Symbol_Codes[i]) == 2:
                    self.Code.SetValue(f"{Symbol_Codes[i]}")
                elif len(Symbol_Codes[i]) == 1:
                    self.Code.SetValue(f"  {Symbol_Codes[i]}")

        # Set size and font for the code
        Size_Font = wx.Font(12, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_NORMAL, style = wx.FONTSTYLE_NORMAL)       # Size 12, Roman font, Normal wight, Normal style
        self.Code.SetFont(Size_Font)

    def Convert_Button(self):
        # Create the convert button, add to horizontal_Boxsizer, and set position
        self.Convert = wx.Button(self.panel, label = "Convert", size = (100, 50))                           # Create the convert button to convert from the first currency to the second
        self.Horizontal_Boxsizer.Add(self.Convert, 0, wx.EXPAND | wx.ALL, border = 10)                     # Add to Horizontal_Boxsizer
        self.Convert.SetPosition(wx.Point(1027, 250))                                                     # Set its position

        # Set the colors
        self.Convert.SetBackgroundColour(wx.Colour(0, 128, 255))            # Set the background color of the convert button to blue
        self.Convert.SetForegroundColour(wx.Colour(255, 255, 255))            # Set the foreground color of the convert button to while
        
        # Bind the convert button to Button_Click to display the conversions
        self.Convert.Bind(wx.EVT_BUTTON, self.Button_Click)

        # Set size and font for the convert button 
        Size_Font = wx.Font(15, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_BOLD, style = wx.FONTSTYLE_MAX)       # Size 12, Roman font, Bold wight, Max style
        self.Convert.SetFont(Size_Font)

    def Swap_Button(self):
        # Create the swap button to swap the chosen currencies
        self.Swap = wx.Button(self.panel, label = "⇆", size = (35, 34))                           # Create the swap button to swap the first currency with the the second
        self.Horizontal_Boxsizer.Add(self.Swap, 1, wx.EXPAND | wx.ALL, border = 10)                     # Add to Horizontal_Boxsizer
        self.Swap.SetPosition(wx.Point(733, 198))                                                     # Set its position

        # Set the color
        self.Swap.SetForegroundColour(wx.Colour(0, 0, 255))            # Set the foreground color of the swap button to dark blue

        # Bind the swap button to Swap_Currencies to swap the currencies
        self.Swap.Bind(wx.EVT_BUTTON, self.Swap_Currencies)

        # Set size and font for the Arrow Back and Forth above
        Size_Font_Arrow = wx.Font(25, family = wx.FONTFAMILY_ROMAN, weight = wx.FONTWEIGHT_NORMAL, style = wx.FONTSTYLE_NORMAL)       # Size 25, Roman font, Normal wight, Normal style
        self.Swap.SetFont(Size_Font_Arrow)

    def Swap_Currencies(self, evt):
        First_Currency_Choice = self.From_currency_choices.GetValue()           # Get the value of the First_Currency_Choices
        Second_Currency_Choice = self.To_currency_choices.GetValue()           # Get the value of the Second_Currency_Choices

        self.From_currency_choices.SetValue(Second_Currency_Choice)             # Swap, set the value of the First_Currency_Choice to the Second_Currency_Choice
        self.To_currency_choices.SetValue(First_Currency_Choice)             # Swap, set the value of the Second_Currency_Choice to the First_Currency_Choice

        self.Currency_Codes(self.From_currency_choices.GetValue())          # Call the Currency_Codes fucntion and pass the value of the From_currency_choices to display the correct code

    def Button_Click(self, evt):
        # Get the values of Amount, From_Currency and To_Currency
        Amount = self.Amount_input.GetValue()                           # Get the value of Amount_Input entered and store it in Amount
        From_Currency = self.From_currency_choices.GetValue()           # Get the choice of From_currency_choices chosen and store in From_Currency
        To_Currency = self.To_currency_choices.GetValue()               # Get the choice of To_currency_choices chosen and store in To_currency

        # If conditions to check if everything is correctly entered/selected
        if ((not Amount) or (Amount.isalpha()) or (Amount in "!@#$%^&*()-_=[]{\};:'\",<>/?`~+")) and (From_Currency == "Select") and (To_Currency == "Select"):
            wx.MessageBox("Please Enter a Valid Input For Amount and Currencies", "Error", wx.OK | wx.ICON_ERROR)
            return
        if ((not Amount) or (Amount.isalpha()) or (Amount in "!@#$%^&*()-_=[]{\};:'\",<>/?`~+")) and (From_Currency == "Select"):
            wx.MessageBox("Please Enter a Valid Input For Amount and Currency to Convert From", "Error", wx.OK | wx.ICON_ERROR)
            return
        if ((not Amount) or (Amount.isalpha()) or (Amount in "!@#$%^&*()-_=[]{\};:'\",<>/?`~+")) and (To_Currency == "Select"):
            wx.MessageBox("Please Enter a Valid Input For Amount and Currency to Convert to", "Error", wx.OK | wx.ICON_ERROR)
            return
        if (From_Currency == "Select") and (To_Currency == "Select"):
            wx.MessageBox("Please Enter Valid Currencies", "Error", wx.OK | wx.ICON_ERROR)
            return
        if (not Amount) or (Amount.isalpha()) or (Amount in "!@#$%^&*()-_=[]{\};:'\",<>/?`~+"):
            wx.MessageBox("Please Enter a Valid Input", "Error", wx.OK | wx.ICON_ERROR)
            return
        if (From_Currency == "Select"):
            wx.MessageBox("Please Enter a Valid Currency to Convert From", "Error", wx.OK | wx.ICON_ERROR)
            return
        if (To_Currency == "Select"):
            wx.MessageBox("Please Enter a Valid Currency to Convert to", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Split the From_Currency and To_Currency
        From_Currency_Symbol = From_Currency.split()[0]             # Get the "currency symbol" from From_Currency and store it in From_Currency_Symbol using the split method
        From_Currency_ = From_Currency.split(' - ')[1]               # Get the "currency and counrty" from From_Currency and store it in From_Currency_ using the split method
        From_Currency__ = From_Currency_.split('(')[0]             # Get the get the currecny complete name from From_Currency_ and store it in From_Currency__ using the split method

        To_Currency_Symbol = To_Currency.split()[0]                 # Get the "currency symbol" from To_Currency and store it in To_Currency_Symbol using the split method
        To_Currency_ = To_Currency.split(' - ')[1]                   # Get the "currency and counrty" from To_Currency and store it in To_Currency_ using the split method
        To_Currency__ = To_Currency_.split('(')[0]                 # Get the get the currecny complete name from To_Currency_ and store it in To_Currency__ using the split method

        # Get the Amount in an integer or float
        try:
            Amount = float(Amount)
            
            # If the Amount is negative show the MessageBox error
            if Amount < 0:
                wx.MessageBox("Please Enter a Non-Negative Input", "Error", wx.OK | wx.ICON_ERROR)
                return
        except (Exception, TypeError):
            # If there is a type error show the MessageBox error
            wx.MessageBox("Please Enter a Valid Input", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Do the convertions
        try:
            Conversion_Rate = self.Currency_Conversion_Rate(From_Currency_Symbol, To_Currency_Symbol)

            Result = Amount * Conversion_Rate                               # Initialize the result to the multiplication of Amount * Conversion_Rate
            From_Result_String = f"{Amount:,.2f} {From_Currency__} ="
            To_Result_String = f"{Result:,.5f} {To_Currency__}"
            self.From_Result.SetLabel(From_Result_String)                   # Set the From_Result label to From_Result_String
            self.To_Result.SetLabel(To_Result_String)                       # Set the To_Result label to To_Result_String

            # if the Amount is 1 or the Amount is 1 and the From_Currency_Symbol is the same as the To_Currency_Symbol show only the First_Coin
            if (Amount == 1) or ((Amount > 1) and (From_Currency_Symbol == To_Currency_Symbol)):
                conversion_rate = self.Currency_Conversion_Rate(To_Currency_Symbol, From_Currency_Symbol)
                reuslt = 1 * conversion_rate
                from_result_string = f"1 {To_Currency_Symbol} = {reuslt:,.5f} {From_Currency_Symbol}"
                self.First_Coin.SetLabel(from_result_string)                                           # Set the First_Coin label to from_result_string

                self.Second_Coin.SetLabel("")                                       # Set the Second_Coin label to nothing

            # Else if amount is greater than 1 show both coins, First_Coin and Second_Coin
            elif Amount > 1:
                reuslt = 1 * Conversion_Rate
                from_result_string = f"1 {From_Currency_Symbol} = {reuslt:,.5f} {To_Currency_Symbol}"
                self.First_Coin.SetLabel(from_result_string)                                           # Set the First_Coin label to from_result_string

                conversion_rate = self.Currency_Conversion_Rate(To_Currency_Symbol, From_Currency_Symbol)
                reuslt = 1 * conversion_rate
                from_result_string = f"1 {To_Currency_Symbol} = {reuslt:,.5f} {From_Currency_Symbol}"
                self.Second_Coin.SetLabel(from_result_string)                                           # Set the Second_Coin label to from_result_string
        except (Exception, KeyError):
            # If there is a key error show the MessageBox error
            wx.MessageBox("Please Check your API Key", "Error", wx.OK | wx.ICON_ERROR)
            return

    def Currency_Conversion_Rate(self, From_Currency_Symbol, To_Currency_Symbol):
        """
        For this project I used the the Fixer.io API, which is one of the top APIs for currency exchange rates. 
        This API provides up-to-date currency exchange rates for many currencies around the world. The Fixer 
        API is highly reliable, and up to time rate.
        """
        # Get the APIKey from the imported APIKey file
        api_key = APIKey()
        api_url = f"http://data.fixer.io/api/latest?access_key={api_key}"

        # Get the conversion rate
        try:
            response = requests.get(api_url)
            data = response.json()
            conversion_rate = data["rates"][To_Currency_Symbol] / data["rates"][From_Currency_Symbol]
            return conversion_rate
        except (requests.ConnectionError, requests.RequestException):
            return None
        
    def CopyRight(self, evt):
        # Show the copyright message when trying to close the app, and then close the app
        wx.MessageBox("Copyright © 2024 Abdul Karim Tamim. All rights reserved", "Copyright Information", wx.OK | wx.ICON_INFORMATION)
        evt.Skip()

def main():
    # Main Function
    app = wx.App()                      # Initialize app to the wx.App
    frame = CurrencyConverter(parent = None, title = "Currency Converter", size = (1167, 475))      # Initialize the frame to the CurrencyCoverter class

    frame.Show()                    # Show the currency converter app
    app.MainLoop()                  # Main infinite loop for continuous run unitl app is closed

if __name__ == "__main__":
    main()
