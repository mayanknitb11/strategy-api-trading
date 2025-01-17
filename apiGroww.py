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


def get_current_orders() -> Optional[OrderListResponse]:
    """
    Fetch and log the current orders.
    """
    try:
        orders = groww_client.get_order_list()
        logger.info("Current orders: %s", orders)
        return orders
    except GrowwClientException as e:
        logger.error("Failed to get orders: %s", e)
        return None


def get_holdings() -> Optional[HoldingsResponse]:
    """
    Fetch and log the user's holdings.
    """
    try:
        holdings_response = groww_client.get_holdings_for_user(timeout=5)
        logger.info("Holdings: %s", holdings_response)
        return holdings_response
    except GrowwClientException as e:
        logger.error("Failed to get holdings: %s", e)
        return None


def get_latest_index_data() -> Optional[LatestIndexResponse]:
    """
    Fetch and log the latest index data.
    """
    try:
        latest_index_data = groww_client.get_latest_index_data(
            symbol="NIFTY",
            exchange=Exchange.NSE,
            segment=Segment.CASH,
            timeout=5,
        )
        logger.info("Latest index data: %s", latest_index_data)
        return latest_index_data
    except GrowwClientException as e:
        logger.error("Failed to get latest index data: %s", e)
        return None


def get_latest_price_data(symbol: str, exchange: Exchange, segment: Segment) -> Optional[LatestPriceResponse]:
    """
    Fetch and log the latest price data.
    """
    try:
        latest_price_data = groww_client.get_latest_price_data(
            symbol=symbol,
            exchange=exchange,
            segment=segment,
            timeout=5,
        )
        logger.info("Latest price data: %s", latest_price_data)
        return latest_price_data
    except GrowwClientException as e:
        logger.error("Failed to get latest price data: %s", e)
        return None


def get_market_depth(symbol: str, exchange: Exchange, segment: Segment) -> Optional[MarketDepthData]:
    """
    Fetch and log the market depth data.
    """
    try:
        market_depth_data = groww_client.get_market_depth(
            symbol=symbol,
            exchange=exchange,
            segment=segment,
            timeout=5,
        )
        logger.info("Market depth data: %s", market_depth_data)
        return market_depth_data
    except GrowwClientException as e:
        logger.error("Failed to get market depth data: %s", e)
        return None


def place_order(
        duration: Duration,
        exchange: Exchange,
        transaction_type: TransactionType,
        order_type: OrderType,
        price: float,
        product: Product,
        qty: int,
        segment: Segment,
        symbol: str,
        timeout: int
) -> Optional[OrderResponse]:
    """
    Place an order and return the response.

    Args:
        duration (Duration): The duration of the order.
        exchange (Exchange): The exchange to place the order on.
        transaction_type (TransactionType): The type of transaction (e.g., BUY, SELL).
        order_type (OrderType): The type of order (e.g., MARKET, LIMIT).
        price (float): The price of the order.
        product (Product): The product type (e.g., MIS, CNC).
        qty (int): The quantity of the order.
        segment (Segment): The segment of the order (e.g., CASH, DERIVATIVES).
        symbol (str): The symbol for the order.
        timeout (int): The timeout for the request in seconds.

    Returns:
        Optional[OrderResponse]: The response from placing the order or None if failed.
    """
    try:
        create_order_response = groww_client.place_order(
            duration=duration,
            exchange=exchange,
            transaction_type=transaction_type,
            order_type=order_type,
            price=price,
            product=product,
            qty=qty,
            segment=segment,
            symbol=symbol,
            timeout=timeout,
        )
        logger.info("Order placed: %s", create_order_response)
        return create_order_response
    except GrowwClientException as e:
        logger.error("Failed to place order: %s", e)
        return None


def modify_order(
        order_type: OrderType,
        price: float,
        qty: int,
        segment: Segment,
        create_order_response: OrderResponse,
) -> Optional[ModifyOrderResponse]:
    """
    Modify an existing order.

    Args:
        groww_client (StructuredGrowwClient): The Groww API client instance.
        create_order_response (OrderResponse): The response from placing the order.

    Returns:
        Optional[ModifyOrderResponse]: The response from modifying the order or None if failed.
    """
    try:
        modify_order_response = groww_client.modify_order(
            groww_order_id=create_order_response.groww_order_id,
            order_reference_id=create_order_response.order_reference_id,
            order_type=order_type,
            price=price,
            qty=qty,
            segment=segment,
            timeout=5,
        )
        logger.info("Order modified: %s", modify_order_response)
        return modify_order_response
    except GrowwClientException as e:
        logger.error("Failed to modify order: %s", e)
        return None


def get_trades(create_order_response: OrderResponse) -> Optional[TradeResponse]:
    """
    Fetch and log the trades for an order.

    Args:
        groww_client (StructuredGrowwClient): The Groww API client instance.
        create_order_response (OrderResponse): The response from placing the order.

    Returns:
        Optional[TradeResponse]: The response from getting the trades or None if failed.
    """
    try:
        trade_response = groww_client.get_trade_list_for_order(
            groww_order_id=create_order_response.groww_order_id,
            segment=Segment.CASH,
            timeout=5,
        )
        logger.info("Trades: %s", trade_response)
        return trade_response
    except GrowwClientException as e:
        logger.error("Failed to get trades: %s", e)
        return None


def cancel_order(create_order_response: OrderResponse) -> Optional[CancelOrderResponse]:
    """
    Cancel an existing order.

    Args:
        groww_client (StructuredGrowwClient): The Groww API client instance.
        create_order_response (OrderResponse): The response from placing the order.

    Returns:
        Optional[CancelOrderResponse]: The response from canceling the order or None if failed.
    """
    try:
        cancel_response = groww_client.cancel_order(
            groww_order_id=create_order_response.groww_order_id,
            order_reference_id=create_order_response.order_reference_id,
            segment=Segment.CASH,
            timeout=5,
        )
        logger.info("Order canceled: %s", cancel_response)
        return cancel_response
    except GrowwClientException as e:
        logger.error("Failed to cancel order: %s", e)
        return None


def get_order_details(create_order_response: OrderResponse) -> Optional[OrderDetailResponse]:
    """
    Get and log the details of an order.

    Args:
        groww_client (StructuredGrowwClient): The Groww API client instance.
        create_order_response (OrderResponse): The response from placing the order.

    Returns:
        Optional[OrderDetailResponse]: Response from getting the order details or None if failed.
    """
    try:
        order_details = groww_client.get_order_detail(
            groww_order_id=create_order_response.groww_order_id,
            segment=Segment.CASH,
            timeout=5,
        )
        logger.info("Order details: %s", order_details)
        return order_details
    except (GrowwClientException, KeyError) as e:
        logger.error("Failed to get order details: %s", e)
        return None


def get_positions() -> Optional[SymbolToPositionsResponse]:
    """
    Fetch and log the user's positions.

    Args:
        groww_client (StructuredGrowwClient): The Groww API client instance.

    Returns:
        Optional[PositionsResponse]: The response from getting the positions or None if failed.
    """
    try:
        positions = groww_client.get_positions_for_user(
            segment=Segment.CASH,
            timeout=5,
        )
        logger.info("Positions: %s", positions)
        return positions
    except GrowwClientException as e:
        logger.error("Failed to get positions: %s", e)
        return None


def get_position_for_symbol(symbol: str) -> Optional[PositionsResponse]:
    """
    Fetch and log the user's positions for a symbol.

    Args:
        groww_client (StructuredGrowwClient): The Groww API client instance.
        symbol (str): The symbol for which to get the positions.

    Returns:
        Optional[SymbolToPositionsResponse]: Response from getting the positions for a symbol
        or None if failed.
    """
    try:
        positions = groww_client.get_position_for_symbol(
            symbol_isin=symbol,
            timeout=5,
        )
        logger.info("Positions for symbol: %s", positions)
        return positions
    except GrowwClientException as e:
        logger.error("Failed to get positions for symbol: %s", e)
        return None


def get_available_margin_for_user() -> Optional[MarginAvailableResponse]:
    """
    Fetch and log the user's available margin.

    Args:
        groww_client (StructuredGrowwClient): The Groww API client instance.

    Returns:
        Optional[MarginAvailableResponse]: The response from getting the available margin or None if failed.
    """
    try:
        margin_available = groww_client.get_available_margin_details(
            timeout=5,
        )
        logger.info("Margin available: %s", margin_available)
        return margin_available
    except GrowwClientException as e:
        logger.error("Failed to get margin available: %s", e)
        return None


def test_groww_client() -> None:
    # Get flows
    get_current_orders()
    get_latest_index_data()
    get_latest_price_data()
    get_market_depth()
    get_holdings()

    # Order flows
    create_order_response = place_order(
        Duration.DAY,
        Exchange.NSE,
        TransactionType.BUY,
        OrderType.LIMIT,
        100.0,
        Product.CO,
        10,
        Segment.CASH,
        STOCK_SYMBOL_ISIN,
        5
    )
    if create_order_response:
        # modify_order(create_order_response)
        # cancel_order(create_order_response)
        get_order_details(create_order_response)
        get_trades(create_order_response)

    # Position flows
    positions = get_positions()
    if positions and len(positions.symbol_wise_positions) > 0:
        symbol = list(positions.symbol_wise_positions.keys())[0]
        get_position_for_symbol(groww_client, symbol)


if __name__ == "__main__":
    test_groww_client()
