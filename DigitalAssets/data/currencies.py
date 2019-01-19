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
 along with Digital Assets. If not, see <http://www.gnu.org/licenses/>.
"""

def getCurrencies ():
    # (name, symbol, website)
    return [
        ('Bitcoin', 'BTC', 'https://bitcoin.org/'),
        ('Ethereum', 'ETH', 'https://www.ethereum.org/'),
        ('Ripple', 'XRP', 'https://ripple.com/xrp/'),
        ('Bitcoin Cash', 'BCH', 'https://www.bitcoincash.org/'),
        ('EOS', 'EOS', 'https://eos.io/'),
        ('Stellar', 'XLM', 'https://www.stellar.org/'),
        ('Litecoin', 'LTC', 'https://litecoin.org/'),
        ('Tether', 'USDT', 'https://tether.to/'),
        ('Bitcoin SV', 'BSV', 'https://bitcoinsv.io/'),
        ('TRON', 'TRX', 'https://tron.network/'),
        ('Cardano', 'ADA', 'https://www.cardano.org/'),
        ('IOTA', 'IOT', 'https://www.iota.org/'),
        ('Binance Coin', 'BNB', 'https://www.binance.com/'),
        ('Monero', 'XMR', 'https://ww.getmonero.org/'),
        ('Dash', 'DASH', 'https://www.dash.org/'),
        ('NEM', 'XEM', 'http://nem.io/'),
        ('Ethereum Classic', 'ETC', 'https://ethereumclassic.org/'),
        ('NEO', 'NEO', 'https://neo.org/'),
        ('Maker', 'MKR', 'https://makerdao.com/'),
        ('Zcash', 'ZEC', 'https://z.cash/'),
        ('Waves', 'WAVES', 'https://wavesplatform.com/'),
        ('Tezos', 'XTZ', 'https://www.tezos.com/'),
        ('Dogecoin', 'DOGE', 'http://dogecoin.com/'),
        ('VeChain', 'VET', 'https://www.vechain.org/'),
        ('TrueUSD', 'TUSD', 'https://www.trusttoken.com/trueusd/'),
        ('Qtum', 'QTUM', 'https://qtum.org/'),
        ('OmiseGO', 'OMG', 'https://omg.omise.co/'),
        ('Zilliqa', 'ZIL', 'https://www.zilliqa.com/'),
        ('Ontology', 'ONT', 'https://ont.io/'),
        ('Ox', 'ZRX', 'https://0xproject.com/'),
        ('Basic Attention Token', 'BAT', 'https://basicattentiontoken.org/'),
        ('Lisk', 'LSK', 'https://lisk.io/'),
        ('Decred', 'DCR', 'https://www.decred.org/'),
        ('Nano', 'NANO', 'http://nano.org/'),
        ('DigiByte', 'DGB', 'http://www.digibyte.io/'),
        ('Stratis', 'STRAT', 'http://stratisplatform.com/'),
        ('Chainlink', 'LINK', 'https://chain.link/'),
        ('Augur', 'REP', 'http://www.augur.net/'),
        ('Pundi X', 'NPXS', 'https://pundix.com/'),
        ('Golem', 'GNT', 'https://golem.network/'),
        ('Holo', 'HOT', 'https://holochain.org/'),
        ('Siacoin', 'SC', 'https://sia.tech/'),
        ('Steem', 'STEEM', 'https://steem.com/'),
        ('Factom', 'FCT', 'https://www.factomprotocol.org/'),
        ('Ark', 'ARK', 'http://ark.io/'),
        ('Aion', 'AION', 'https://aion.network/'),
        ('BitShares', 'BTS', 'https://bitshares.org/'),
        ('Verge', 'XVG', 'http://vergecurrency.com/'),
        ('Paxos Standard Token', 'PAX', 'https://paxos.com/standard/'),
        ('Komodo', 'KMD', 'https://komodoplatform.com/'),
        ('Populous', 'PPT', 'https://populous.world/'),
        ('Status', 'SNT', 'http://status.im/'),
        ('Storj', 'STORJ', 'https://storj.io/')
    ]

def getBaseCurrencies ():
    return [
        ('Dollars', 'USD'),
        ('Bitcoin', 'BTC'),
        ('Ethereum', 'ETH'),
        ('TrueUSD', 'TUSD'),
        ('Tether', 'USDT')
    ]
