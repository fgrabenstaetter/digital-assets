"""
 Copyright © François Grabenstaetter <francoisgrabenstaetter@gmail.com>

 This file is part of Digital Assets.

 Digital Assets is free software: you can redistribute it and/or
 modify it under the terms of the GNU General Public License as published
 by the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Digital Assets is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Digital Assets. If not, see <https://www.gnu.org/licenses/>.
"""

def getCurrencies ():
    """
        Return all supported currencies in a list of tuples
        (name, symbol, nomics ID, website URL)
    """
    return [
        ('Bitcoin', 'BTC', 'BTC', 'https://bitcoin.org/'),
        ('Ethereum', 'ETH', 'ETH', 'https://www.ethereum.org/'),
        ('Ripple', 'XRP', 'XRP', 'https://ripple.com/xrp/'),
        ('Bitcoin Cash', 'BCH', 'BCH', 'https://www.bitcoincash.org/'),
        ('EOS', 'EOS', 'EOS', 'https://eos.io/'),
        ('Stellar', 'XLM', 'XLM', 'https://www.stellar.org/'),
        ('Litecoin', 'LTC', 'LTC', 'https://litecoin.org/'),
        ('Tether', 'USDT', 'USDT', 'https://tether.to/'),
        ('Bitcoin SV', 'BSV', 'BSV', 'https://bitcoinsv.io/'),
        ('TRON', 'TRX', 'TRX', 'https://tron.network/'),
        ('Cardano', 'ADA', 'ADA', 'https://www.cardano.org/'),
        ('IOTA', 'MIOTA', 'IOT', 'https://www.iota.org/'),
        ('Binance Coin', 'BNB', 'BNB', 'https://www.binance.com/'),
        ('Monero', 'XMR', 'XMR', 'https://ww.getmonero.org/'),
        ('Dash', 'DASH', 'DASH', 'https://www.dash.org/'),
        ('NEM', 'XEM', 'XEM', 'https://nem.io/'),
        ('Ethereum Classic', 'ETC', 'ETC', 'https://ethereumclassic.org/'),
        ('NEO', 'NEO', 'NEO', 'https://neo.org/'),
        ('Maker', 'MKR', 'MKR', 'https://makerdao.com/'),
        ('Zcash', 'ZEC', 'ZEC', 'https://z.cash/'),
        ('Waves', 'WAVES', 'WAVES', 'https://wavesplatform.com/'),
        ('Tezos', 'XTZ', 'XTZ', 'https://www.tezos.com/'),
        ('Dogecoin', 'DOGE', 'DOGE', 'https://dogecoin.com/'),
        ('VeChain', 'VET', 'VET', 'https://www.vechain.org/'),
        ('TrueUSD', 'TUSD', 'TUSD', 'https://www.trusttoken.com/trueusd/'),
        ('Qtum', 'QTUM', 'QTUM', 'https://qtum.org/'),
        ('OmiseGO', 'OMG', 'OMG', 'https://omg.omise.co/'),
        ('Zilliqa', 'ZIL', 'ZIL', 'https://www.zilliqa.com/'),
        ('Ontology', 'ONT', 'ONT', 'https://ont.io/'),
        ('Ox', 'ZRX', 'ZRX', 'https://0xproject.com/'),
        ('Basic Attention Token', 'BAT', 'BAT', 'https://basicattentiontoken.org/'),
        ('Decred', 'DCR', 'DCR', 'https://www.decred.org/'),
        ('Nano', 'NANO', 'NANO', 'https://nano.org/'),
        ('DigiByte', 'DGB', 'DGB', 'https://www.digibyte.io/'),
        ('Chainlink', 'LINK', 'LINK', 'https://chain.link/'),
        ('Holo', 'HOT', 'HOT', 'https://holochain.org/'),
        ('Siacoin', 'SC', 'SC', 'https://sia.tech/'),
        ('Paxos Standard Token', 'PAX', 'PAX', 'https://paxos.com/standard/'),
        ('IOST', 'IOST', 'IOST', 'https://iost.io/'),
        ('Ravencoin', 'RVN', 'RVN', 'https://ravencoin.org/'),
        ('Cosmos', 'ATOM', 'ATOM', 'https://cosmos.network/'),
        ('Theta', 'THETA', 'THETA', 'https://www.thetatoken.org/'),
        ('ICON', 'ICX', 'ICX', 'https://www.icon.foundation/'),
        ('USD Coin', 'USDC', 'USDC', 'https://www.centre.io/usdc/'),
        ('Polkadot', 'DOT', 'DOT', 'https://polkadot.network/'),
        ('Solana', 'SOL', 'SOL', 'https://solana.com/'),
        ('Uniswap', 'UNI', 'UNI', 'https://uniswap.org/'),
        ('Terra', 'LUNA', 'LUNA', 'https://www.terra.money/'),
        ('Binance USD', 'BUSD', 'BUSD', 'https://www.binance.com/en/busd'),
        ('Polygon', 'MATIC', 'MATIC', 'https://polygon.technology/'),
        ('Internet Computer', 'ICP', 'ICP', 'https://dfinity.org/'),
        ('Avalanche', 'AVAX', 'AVAX', 'https://www.avax.network/'),
        ('Filecoin', 'FIL', 'FIL', 'https://filecoin.io/'),
        ('Dai', 'DAI', 'DAI', 'https://makerdao.com/en/'),
        ('Aave', 'AAVE', 'AAVE', 'https://aave.com/'),
        ('PancakeSwap', 'CAKE', 'CAKE', 'https://pancakeswap.finance/'),
        ('The Graph', 'GRT', 'GRT', 'https://thegraph.com/'),
        ('Axie Infinity', 'AXS', 'AXS2', 'https://axieinfinity.com/'),
        ('Klaytn', 'KLAY', 'KLAY', 'https://www.klaytn.com/'),
        ('Crypto.com Coin', 'CRO', 'CRO', 'https://crypto.com/'),
        ('Algorand', 'ALGO', 'ALGO', 'https://www.algorand.com/')
    ]
