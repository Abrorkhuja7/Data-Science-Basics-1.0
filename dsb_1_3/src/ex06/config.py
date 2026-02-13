num_of_steps = 3
telegram_webhook_url = "https://api.telegram.org/bot<6649029718:AAG9sIMVyuZpc9X8QJm5TWSQjYRETS-xSaQ>/sendMessage"

report_template = (
    "We made {n} observations by tossing a coin: {tails} were tails and {heads} were heads. "
    "The probabilities are {pt:.2f}% and {ph:.2f}%, respectively. "
    "Our forecast is that the next {steps} observations will be: {ft} tail and {fh} heads."
)
