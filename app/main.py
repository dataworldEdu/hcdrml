from typing import Optional
from fastapi import FastAPI
import app.data.ingestion as ig
from app.common import logger
logger = logger.getLogger(__name__)
app = FastAPI()


@app.get("/dataload/test")
async def logger_test():
    logger.info('ig.logger_test run!')
    ig.logger_test()
    return 'test'


@app.get("/lern/lightgbm")
async def lern_lightgbm():
    logger.info('ig.test_test run!')
    ig.train_model()
    return 'test'



@app.get("/dataload/appTrain")
async def collect_application_train():
    logger.info('ig.collect_application_train run!')
    ig.collect_application_train()
    return 'collect_application_train'


@app.get("/dataload/prevApp")
async def collect_previous_application():
    logger.info('ig.collect_previous_application run!')
    ig.collect_previous_application()
    return 'collect_previous_application'


@app.get("/dataload/bureau")
async def collect_bureau():
    logger.info('ig.collect_bureau run!')
    ig.collect_bureau()
    return 'collect_bureau'


@app.get("/dataload/poscash")
async def collect_pos_cash_balance():
    logger.info('ig.collect_pos_cash_balance run!')
    ig.collect_pos_cash_balance()
    return 'collect_pos_cash_balance'


@app.get("/dataload/instments")
async def collect_installments_payments():
    logger.info('ig.collect_installments_payments run!')
    ig.collect_installments_payments()
    return 'collect_installments_payments'


@app.get("/dataload/credit")
async def collect_credit_card_balance():
    logger.info('ig.collect_credit_card_balance run!')
    ig.collect_credit_card_balance()
    return 'collect_credit_card_balance'

if __name__ == "__main__":
    logger.info('app start!')