from fastapi import APIRouter

router = APIRouter(prefix="/assets",tags=["assets"])

@router.get("/{symbol}/quote")
async def get_quote(symbol:str):
    return {
        "symbol": symbol.upper(),
        "price":189.42,
        "change_percent":1.18,
        "currency": "USD",
        "source":"mock",
    }