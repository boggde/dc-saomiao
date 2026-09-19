from flask import Flask, jsonify, render_template_string
import threading
from utils import format_money

app = Flask(__name__)


# 当前数据

current_alerts = []



# =====================================
# 更新数据
# =====================================

def update_alerts(data):

    global current_alerts

    current_alerts = data



# =====================================
# API
# =====================================

@app.route("/api/alerts")
def api_alerts():

    return jsonify(
        current_alerts
    )



@app.route("/api/snapshot")
def api_snapshot():

    return jsonify(
        current_alerts
    )



# =====================================
# 页面
# =====================================

@app.route("/")
def index():

    html = """

<!DOCTYPE html>

<html>

<head>

<title>
Binance Anomaly Monitor V1
</title>


<meta http-equiv="refresh"
content="5">


<style>

body {

    font-family: Arial;

    margin:40px;

}


table {

    border-collapse: collapse;

    width:100%;

}


th,td {

    border:1px solid #ccc;

    padding:8px;

    text-align:center;

}


th {

    background:#222;

    color:white;

}


</style>


</head>


<body>


<h2>
🚨 Binance 1H Anomaly Monitor V1
</h2>


<table>


<tr>

<th>Symbol</th>
<th>Price</th>
<th>1H Range</th>
<th>High</th>
<th>Low</th>
<th>Volume</th>
<th>Surge</th>

</tr>


{% for x in data %}


<tr>


<td>{{x.symbol}}</td>

<td>{{x.price}}</td>

<td>
{{x.range_pct}}%
</td>


<td>
{{x.high}}
</td>


<td>
{{x.low}}
</td>


<td>
{{format_money(x.volume_1h)}} USDT
</td>


<td>
{{x.volume_multiple}}x
</td>


</tr>


{% endfor %}


</table>


</body>

</html>

"""

    return render_template_string(
        html,
        data=current_alerts,
        format_money=format_money
    )



# =====================================
# 启动WEB
# =====================================

def start_web(
    host,
    port
):

    thread = threading.Thread(

        target=lambda:
        app.run(
            host=host,
            port=port,
            debug=False,
            use_reloader=False
        ),

        daemon=True

    )


    thread.start()