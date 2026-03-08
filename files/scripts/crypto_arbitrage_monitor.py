#!/usr/bin/env python3
"""
Crypto Arbitrage Monitor Scanner
Detects cross-exchange arbitrage opportunities for major cryptocurrencies.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Tuple
import httpx

class CryptoArbitrageMonitor:
    """Monitor crypto prices across exchanges to detect arbitrage opportunities."""
    
    def __init__(self):
        self.exchanges = {
            'coinbase': 'https://api.coinbase.com/v2/prices',
            'kraken': 'https://api.kraken.com/0/public/Ticker',
            'binance': 'https://api.binance.com/api/v3/ticker/price',
            'coingecko': 'https://api.coingecko.com/api/v3/simple/price'
        }
        
        self.trading_pairs = [
            'BTC', 'ETH', 'SOL', 'MATIC', 'AVAX', 'DOT', 'LINK', 'UNI'
        ]
        
        self.min_spread_threshold = 0.5  # Minimum 0.5% spread to be interesting
        self.exchange_status = {}
        
    def fetch_coinbase_prices(self) -> Dict[str, float]:
        """Fetch prices from Coinbase."""
        prices = {}
        try:
            with httpx.Client(timeout=10) as client:
                for pair in self.trading_pairs:
                    try:
                        response = client.get(f"{self.exchanges['coinbase']}/{pair}-USD/spot")
                        if response.status_code == 200:
                            data = response.json()
                            prices[pair] = float(data['data']['amount'])
                    except Exception as e:
                        print(f"Error fetching {pair} from Coinbase: {e}")
            
            self.exchange_status['coinbase'] = 'operational' if prices else 'degraded'
            return prices
        except Exception as e:
            print(f"Coinbase API error: {e}")
            self.exchange_status['coinbase'] = 'error'
            return {}
    
    def fetch_kraken_prices(self) -> Dict[str, float]:
        """Fetch prices from Kraken."""
        prices = {}
        kraken_pairs = {
            'BTC': 'XXBTZUSD',
            'ETH': 'XETHZUSD',
            'SOL': 'SOLUSD',
            'MATIC': 'MATICUSD',
            'AVAX': 'AVAXUSD',
            'DOT': 'DOTUSD',
            'LINK': 'LINKUSD',
            'UNI': 'UNIUSD'
        }
        
        try:
            with httpx.Client(timeout=10) as client:
                pair_query = ','.join(kraken_pairs.values())
                response = client.get(f"{self.exchanges['kraken']}?pair={pair_query}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('result'):
                        for symbol, kraken_symbol in kraken_pairs.items():
                            result_data = data['result'].get(kraken_symbol)
                            if result_data and 'c' in result_data:
                                prices[symbol] = float(result_data['c'][0])
            
            self.exchange_status['kraken'] = 'operational' if prices else 'degraded'
            return prices
        except Exception as e:
            print(f"Kraken API error: {e}")
            self.exchange_status['kraken'] = 'error'
            return {}
    
    def fetch_binance_prices(self) -> Dict[str, float]:
        """Fetch prices from Binance."""
        prices = {}
        binance_pairs = {
            'BTC': 'BTCUSDT',
            'ETH': 'ETHUSDT',
            'SOL': 'SOLUSDT',
            'MATIC': 'MATICUSDT',
            'AVAX': 'AVAXUSDT',
            'DOT': 'DOTUSDT',
            'LINK': 'LINKUSDT',
            'UNI': 'UNIUSDT'
        }
        
        try:
            with httpx.Client(timeout=10) as client:
                for symbol, binance_symbol in binance_pairs.items():
                    try:
                        response = client.get(f"{self.exchanges['binance']}?symbol={binance_symbol}")
                        if response.status_code == 200:
                            data = response.json()
                            prices[symbol] = float(data['price'])
                    except Exception as e:
                        print(f"Error fetching {symbol} from Binance: {e}")
            
            self.exchange_status['binance'] = 'operational' if prices else 'degraded'
            return prices
        except Exception as e:
            print(f"Binance API error: {e}")
            if '451' in str(e) or 'Unavailable' in str(e):
                self.exchange_status['binance'] = 'blocked'
            else:
                self.exchange_status['binance'] = 'error'
            return {}
    
    def fetch_coingecko_prices(self) -> Dict[str, float]:
        """Fetch prices from CoinGecko (validation layer)."""
        prices = {}
        coingecko_ids = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'SOL': 'solana',
            'MATIC': 'matic-network',
            'AVAX': 'avalanche-2',
            'DOT': 'polkadot',
            'LINK': 'chainlink',
            'UNI': 'uniswap'
        }
        
        try:
            with httpx.Client(timeout=10) as client:
                ids_query = ','.join(coingecko_ids.values())
                response = client.get(
                    f"{self.exchanges['coingecko']}",
                    params={'ids': ids_query, 'vs_currencies': 'usd'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for symbol, cg_id in coingecko_ids.items():
                        if cg_id in data and 'usd' in data[cg_id]:
                            prices[symbol] = float(data[cg_id]['usd'])
            
            self.exchange_status['coingecko'] = 'operational' if prices else 'degraded'
            return prices
        except Exception as e:
            print(f"CoinGecko API error: {e}")
            self.exchange_status['coingecko'] = 'error'
            return {}
    
    def validate_price(self, price: float, symbol: str, reference_prices: Dict[str, float]) -> bool:
        """Validate if a price is reasonable compared to reference prices."""
        if symbol not in reference_prices:
            return False
        
        reference_price = reference_prices[symbol]
        if reference_price == 0:
            return False
        
        # Price should be within 50% of reference (catches corrupted data)
        deviation = abs(price - reference_price) / reference_price
        return deviation < 0.5
    
    def find_arbitrage_opportunities(self, all_prices: Dict[str, Dict[str, float]], 
                                    reference_prices: Dict[str, float]) -> List[Dict]:
        """Find arbitrage opportunities across exchanges."""
        opportunities = []
        
        for symbol in self.trading_pairs:
            symbol_prices = {}
            
            # Collect valid prices for this symbol
            for exchange, prices in all_prices.items():
                if symbol in prices and prices[symbol] > 0:
                    # Validate price against reference
                    if self.validate_price(prices[symbol], symbol, reference_prices):
                        symbol_prices[exchange] = prices[symbol]
            
            if len(symbol_prices) < 2:
                continue
            
            # Find min and max prices
            min_exchange = min(symbol_prices, key=symbol_prices.get)
            max_exchange = max(symbol_prices, key=symbol_prices.get)
            min_price = symbol_prices[min_exchange]
            max_price = symbol_prices[max_exchange]
            
            # Calculate spread percentage
            spread_pct = ((max_price - min_price) / min_price) * 100
            
            if spread_pct >= self.min_spread_threshold:
                opportunity = {
                    'symbol': symbol,
                    'buy_exchange': min_exchange,
                    'sell_exchange': max_exchange,
                    'buy_price': min_price,
                    'sell_price': max_price,
                    'spread_pct': round(spread_pct, 2),
                    'potential_profit_per_unit': round(max_price - min_price, 2),
                    'reference_price': reference_prices.get(symbol, 0),
                    'timestamp': datetime.utcnow().isoformat()
                }
                opportunities.append(opportunity)
        
        return sorted(opportunities, key=lambda x: x['spread_pct'], reverse=True)
    
    def run_scan(self) -> Dict:
        """Execute full arbitrage scan across all exchanges."""
        start_time = time.time()
        
        print("Fetching prices from exchanges...")
        
        # Fetch prices from all exchanges
        coinbase_prices = self.fetch_coinbase_prices()
        kraken_prices = self.fetch_kraken_prices()
        binance_prices = self.fetch_binance_prices()
        coingecko_prices = self.fetch_coingecko_prices()
        
        all_prices = {
            'coinbase': coinbase_prices,
            'kraken': kraken_prices,
            'binance': binance_prices
        }
        
        # Use CoinGecko as reference for validation
        reference_prices = coingecko_prices
        
        # Find opportunities
        opportunities = self.find_arbitrage_opportunities(all_prices, reference_prices)
        
        scan_duration = time.time() - start_time
        
        # Calculate statistics
        operational_exchanges = sum(1 for status in self.exchange_status.values() 
                                   if status == 'operational')
        
        result = {
            'scan_metadata': {
                'timestamp': datetime.utcnow().isoformat(),
                'duration_seconds': round(scan_duration, 2),
                'exchanges_scanned': len(self.exchanges),
                'operational_exchanges': operational_exchanges,
                'trading_pairs': len(self.trading_pairs)
            },
            'exchange_status': self.exchange_status,
            'opportunities': opportunities,
            'raw_prices': {
                'coinbase': coinbase_prices,
                'kraken': kraken_prices,
                'binance': binance_prices,
                'coingecko_reference': coingecko_prices
            },
            'summary': {
                'total_opportunities': len(opportunities),
                'best_spread': opportunities[0]['spread_pct'] if opportunities else 0,
                'best_pair': opportunities[0]['symbol'] if opportunities else None
            }
        }
        
        return result

def main():
    """Main execution function."""
    print("=" * 60)
    print("CRYPTO ARBITRAGE MONITOR")
    print("=" * 60)
    
    monitor = CryptoArbitrageMonitor()
    scan_results = monitor.run_scan()
    
    # Save results
    timestamp = datetime.utcnow().strftime('%Y%m%d')
    output_file = f'data/crypto_arbitrage_scan_{timestamp}.json'
    
    with open(output_file, 'w') as f:
        json.dump(scan_results, f, indent=2)
    
    print(f"\nScan complete!")
    print(f"Duration: {scan_results['scan_metadata']['duration_seconds']}s")
    print(f"Opportunities found: {scan_results['summary']['total_opportunities']}")
    
    if scan_results['opportunities']:
        print(f"\nTop opportunity:")
        top = scan_results['opportunities'][0]
        print(f"  {top['symbol']}: Buy on {top['buy_exchange']} at ${top['buy_price']:,.2f}")
        print(f"           Sell on {top['sell_exchange']} at ${top['sell_price']:,.2f}")
        print(f"           Spread: {top['spread_pct']}%")
    
    print(f"\nResults saved to: {output_file}")
    
    return scan_results

if __name__ == '__main__':
    main()
