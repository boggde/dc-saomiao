def format_money(value):

    value = float(value)


    if value >= 100_000_000:

        return (
            f"{value / 100_000_000:.2f}亿"
        )


    elif value >= 10_000:

        return (
            f"{value / 10_000:.2f}万"
        )


    else:

        return (
            f"{value:.2f}"
        )