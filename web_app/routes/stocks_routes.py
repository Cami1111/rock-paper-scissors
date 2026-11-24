# this is the "web_app/routes/stocks_routes.py" file...

from flask import Blueprint, request, render_template, redirect, flash

from app.stocks import fetch_stocks_csv, format_usd

stocks_routes = Blueprint("stocks_routes", __name__)


@stocks_routes.route("/stocks/form")
def stocks_form():
    print("STOCKS FORM...")
    return render_template("stocks_form.html")


# also works with url params, like /stocks/dashboard?symbol=SPOT
@stocks_routes.route("/stocks/dashboard", methods=["GET", "POST"])
def stocks_dashboard():
    print("STOCKS DASHBOARD...")

    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    symbol = (request_data.get("symbol") or "NFLX").strip().upper()

    try:
        df = fetch_stocks_csv(symbol=symbol)
        latest_close_usd = format_usd(df.iloc[0]["adjusted_close"])
        latest_date = df.iloc[0]["timestamp"]
        data = df.to_dict("records")

        flash("Fetched Real-time Market Data!", "success")
        return render_template("stocks_dashboard.html",
            symbol=symbol,
            latest_close_usd=latest_close_usd,
            latest_date=latest_date,
            data=data
        )
    except Exception as err:
        # if the symbol is invalid (or the API has a problem), we end up here
        # instead of crashing, send the user back to the form with a message
        print("OOPS", err)

        flash("Market Data Error. Please check your symbol and try again!", "danger")
        return redirect("/stocks/form")
