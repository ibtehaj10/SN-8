from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bittensor as bt
from bittensor import Keypair, metagraph, wallet
from proprietary_rading_network.template.protocol import SendSignal, GetPositions
import typing
import bittensor as bt
from pydantic import Field

from typing import List

# Configuration and Setup
hotkey = Keypair.create_from_mnemonic()
dendrite = bt.dendrite(wallet=hotkey)
bt_network = bt.metagraph(8, network="finney")
bt_network.sync()

app = FastAPI()

# class QueryParams(BaseModel):
#     trade_pair_id: str
#     trade_pair: str
#     fees: float

@app.post("/search/")
async def search_synapse():
    #yTradeView
    synapse=SendSignal(
        signal={'trade_pair': {'trade_pair_id': 'ETHUSD', 'trade_pair': 'ETH/USD', 'fees': 0.003, 'min_leverage': 0.001, 'max_leverage': 20},
                   'order_type': 'SHORT',
                   'leverage': 0.01})
    axons = bt_network.axons
    if not axons:
        raise HTTPException(status_code=404, detail="No axons available for querying")

    try:
        response = dendrite(axons[:min(len(axons), 10)], timeout=300.0, synapse=synapse)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

