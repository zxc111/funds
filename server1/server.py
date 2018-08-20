import json

from flask import Flask

from models.db import InitDB
from models.funds import (
    Fund, FundStatistics
)

DB = InitDB("dev")


app = Flask(__name__)

@app.route("/")
def hello():
    session = DB.Session()
    fund = session.query(Fund).first()
    fund_statistics_list = session.query(FundStatistics).filter(
        FundStatistics.fundcode == fund.fundcode,
    ).all()
    res = [i.dict for i in fund_statistics_list]
    return json.dumps(res)
