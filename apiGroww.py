import logging

from gwapex import StructuredGrowwClient
from gwapex.groww.responses import *
from gwapex_base import GrowwFeed
from gwapex_base.groww.enums import *
from gwapex_base.groww.exceptions import GrowwClientException

from creds import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

groww_client = StructuredGrowwClient(API_AUTH_TOKEN, API_KEY)
groww_feed = GrowwFeed(SOCKET_TOKEN, SOCKET_KEY)


def get_historical_candle_data(interval_in_minutes: Optional[int] = None) -> Optional[dict[str, any]]:
    try:
        end_time_in_millis = "2025-01-17T15:30:00"
        start_time_in_millis = "2025-01-17T09:15:00"
        segment = Segment.CASH
        symbol = STOCK_SYMBOL_ISIN
        exchange = Exchange.NSE
        response = groww_client.get_historical_candle_data(symbol, exchange, segment, start_time_in_millis,
                                                           end_time_in_millis, interval_in_minutes)
        logger.info("History data: %s", response)
        return response
    except GrowwClientException as e:
        logger.error("Failed to get history data: %s", e)
        return None


def get_latest_index_data() -> Optional[LatestIndexResponse]:
    try:
        latest_index_data = groww_client.get_latest_index_data(
            symbol=STOCK_SYMBOL_ISIN,
            exchange=Exchange.NSE,
            segment=Segment.CASH,
            timeout=5,
        )
        logger.info("Latest index data: %s", latest_index_data)
        return latest_index_data
    except GrowwClientException as e:
        logger.error("Failed to get latest index data: %s", e)
        return None


def get_live_feed() -> None:
    groww_feed.subscribe_stocks_live(STOCK_SYMBOL_ISIN)
    groww_feed.subscribe_stocks_market_depth(STOCK_SYMBOL_ISIN)

    groww_feed.subscribe_market_info()
    while True:
        logging.info(
            "%s Equity LTP: %s",
            STOCK_SYMBOL_ISIN,
            groww_feed.get_stocks_ltp(STOCK_SYMBOL_ISIN, timeout=3),
        )


def place_order(
        self,
        duration: Duration,
        exchange: Exchange,
        order_type: OrderType,
        price: float,
        product: Product,
        qty: int,
        segment: Segment,
        symbol: str,
        transaction_type: TransactionType,
        timeout: Optional[int] = None,
) -> OrderResponse:
    """
    Place a new order.

    Args:
        duration (Duration): The duration of the order.
        exchange (Exchange): The exchange to place the order on.
        order_type (OrderType): The type of order.
        price (float): The price of the order.
        product (Product): The product type.
        qty (int): The quantity of the order.
        segment (Segment): The segment of the order.
        symbol (str): The symbol to place the order for.
        transaction_type (TransactionType): The transaction type.
        timeout (Optional[int]): The timeout for the request in seconds. Defaults to None (infinite).

    Returns:
        OrderResponse: The placed order response.

    Raises:
        GrowwClientException: If the request fails.
    """
    response: dict[str, any] = super().place_order(
        duration=duration,
        exchange=exchange,
        order_type=order_type,
        price=price,
        product=product,
        qty=qty,
        segment=segment,
        symbol=symbol,
        transaction_type=transaction_type,
        timeout=timeout,
    )
    return OrderResponse(**response)


def modify_order(
        self,
        order_type: OrderType,
        price: float,
        qty: int,
        segment: Segment,
        groww_order_id: Optional[str] = None,
        order_reference_id: Optional[str] = None,
        timeout: Optional[int] = None,
) -> ModifyOrderResponse:
    """
    Modify an existing order.

    Args:
        order_type (OrderType): The type of order.
        price (float): The price of the order.
        qty (int): The quantity of the order.
        segment (Segment): The segment of the order.
        groww_order_id (Optional[str]): The Groww order ID.
        order_reference_id (Optional[str]): The order reference ID.
        timeout (Optional[int]): The timeout for the request in seconds. Defaults to None (infinite).

    Returns:
        ModifyOrderResponse: The modified order response.

    Raises:
        GrowwClientException: If the request fails.
    """
    response: dict[str, any] = super().modify_order(
        order_type=order_type,
        price=price,
        qty=qty,
        segment=segment,
        groww_order_id=groww_order_id,
        order_reference_id=order_reference_id,
        timeout=timeout,
    )
    return ModifyOrderResponse(**response)


def cancel_order(
        self,
        groww_order_id: str,
        segment: Segment,
        order_reference_id: Optional[str] = None,
        timeout: Optional[int] = None,
) -> CancelOrderResponse:
    """
    Cancel an existing order.

    Args:
        groww_order_id (str): The Groww order ID.
        segment (Segment): The segment of the order.
        order_reference_id (Optional[str]): The order reference ID.
        timeout (Optional[int]): The timeout for the request in seconds. Defaults to None (infinite).

    Returns:
        CancelOrderResponse: The cancelled order response.

    Raises:
        GrowwClientException: If the request fails.
    """
    response: dict[str, any] = super().cancel_order(
        groww_order_id=groww_order_id,
        segment=segment,
        order_reference_id=order_reference_id,
        timeout=timeout,
    )
    return CancelOrderResponse(**response)


def get_holdings_for_user(self, timeout: Optional[int] = None) -> HoldingsResponse:
    """
    Get the holdings for the user.

    Args:
        timeout (Optional[int]): The timeout for the request in seconds. Defaults to None (infinite).

    Returns:
        HoldingsResponse: The user's holdings response.

    Raises:
        GrowwClientException: If the request fails.
    """
    response: dict[str, any] = super().get_holdings_for_user(timeout=timeout)
    return HoldingsResponse(**response)


if __name__ == "__main__":
    get_historical_candle_data()
    get_latest_index_data()
    get_live_feed()
    groww_feed.close()

