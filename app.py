import requests
from flask import Flask, request, render_template

app = Flask(__name__)

base_url = 'http://api.exchangerate.host/convert?'
# access_key = 'access_key=8952bbb66f6525b39d0a59abaeb980bb'


@app.route('/', methods=['GET', 'POST'])
def currency_converter():
    if request.method == 'POST':
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])

        params = {
    # 'access_key': access_key,
    'from': from_currency,
    'to': to_currency,
    'amount': amount,
}

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            result = data['result']
            formatted_result = format_currency(result, to_currency)
            return render_template('converter.html', result=formatted_result, currencies=get_currency_list())
        else:
            error_message = data['error']
            return render_template('converter.html', error=error_message, currencies=get_currency_list())

    return render_template('converter.html', currencies=get_currency_list())

def get_currency_list():
    # Make an API call to get a list of available currencies
    currency_list_url = 'http://api.exchangerate.host/symbols'
    response = requests.get(currency_list_url)
    data = response.json()

    if response.status_code == 200:
        # Extract currency symbols from the response
        currencies = data['symbols']
        return list(currencies.keys())
    else:
        return []

def format_currency(amount, currency_code):
    # Make an API call to get the currency symbol for a given currency code
    currency_symbols_url = 'http://api.exchangerate.host/currencies'
    response = requests.get(currency_symbols_url)
    data = response.json()

    if response.status_code == 200 and currency_code in data:
        currency_symbol = data[currency_code]['symbol']
        return f"{currency_symbol} {amount:.2f}"
    else:
        return f"{currency_code} {amount:.2f}"

if __name__ == "__main__":
    app.run()
