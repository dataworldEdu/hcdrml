import app.data.ingestion as ig
from fastapi import FastAPI
from app.common import logger

logger = logger.getLogger(__name__)
app = FastAPI()


@app.get("/learn/lightgbm")
async def lern_lightgbm():
    ig.train_model()


@app.get("/dataload/all")
async def collect_all_data():
    ig.collect_application_train()
    ig.collect_previous_application()
    ig.collect_bureau()
    ig.collect_pos_cash_balance()
    ig.collect_installments_payments()
    ig.collect_credit_card_balance()


@app.get("/dataload/train")
async def collect_application_train():
    ig.collect_application_train()


@app.get("/dataload/prev")
async def collect_previous_application():
    ig.collect_previous_application()


@app.get("/dataload/bureau")
async def collect_bureau():
    ig.collect_bureau()


@app.get("/dataload/poscash")
async def collect_pos_cash_balance():
    ig.collect_pos_cash_balance()


@app.get("/dataload/instments")
async def collect_installments_payments():
    ig.collect_installments_payments()


@app.get("/dataload/credit")
async def collect_credit_card_balance():
    ig.collect_credit_card_balance()
