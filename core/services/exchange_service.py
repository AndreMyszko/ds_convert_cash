def convert_currency(amount, from_currency, to_currency, exchange_rates):
    try:
        if from_currency == 'USD':
            converted_amount = amount * float(exchange_rates[to_currency])
        elif to_currency == 'USD':
            converted_amount = amount / float(exchange_rates[from_currency])
        else:
            converted_amount = amount * (float(exchange_rates[to_currency]) / float(exchange_rates[from_currency]))
        return '{:.8f}'.format(converted_amount)
    except KeyError as e:
        print(f"Error converting currency: {e}")
        return None
