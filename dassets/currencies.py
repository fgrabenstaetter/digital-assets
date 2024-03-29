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
        ('0x', 'ZRX', 'ZRX', 'https://0xproject.com/'),
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
        ('Algorand', 'ALGO', 'ALGO', 'https://www.algorand.com/'),
        ('Shiba Inu', 'SHIB', 'SHIB', 'https://shibatoken.com/'),
        ('Elrond', 'EGLD', 'EGLD' , 'https://elrond.com/'),
        ('UNUS SED LEO', 'LEO', 'LEO' , 'https://leo.bitfinex.com/'),
        ('BitTorrent', 'BTT', 'BITTORRENT' , 'https://www.bittorrent.com/token/btt/'),
        ('Kusama', 'KSM', 'KSM' , 'https://kusama.network/'),
        ('Amp', 'AMP', 'AMP2' , 'https://amptoken.org/'),
        ('Quant', 'QNT', 'QNT' , 'https://www.quant.network/'),
        ('THORChain', 'RUNE', 'RUNE' , 'https://thorchain.org/'),
        ('TerraUSD', 'UST', 'UST' , 'https://www.terra.money/'),
        ('Near', 'NEAR', 'NEAR' , 'https://near.org/'),
        ('Huobi Token', 'HT', 'HT' , 'https://www.huobi.com/'),
        ('Celsius Network', 'CEL', 'CEL' , 'https://celsius.network/'),
        ('Sushi', 'SUSHI', 'SUSHI' , 'https://sushi.com/'),
        ('Compound', 'COMP', 'COMP' , 'https://compound.finance/'),
        ('Helium', 'HNT', 'HELIUM' , 'https://www.helium.com/'),
        ('Chiliz', 'CHZ', 'CHZ' , 'https://www.chiliz.com/'),
        ('Enjin Coin', 'ENJ', 'ENJ' , 'https://enjin.io/'),
        ('Fantom', 'FTM', 'FTM' , 'https://fantom.foundation/'),
        ('Synthetix', 'SNX', 'SNX' , 'https://www.synthetix.io/'),
        ('KuCoin Token', 'KCS', 'KCS' , 'https://www.kucoin.com/'),
        ('Nexo', 'NEXO', 'NEXO' , 'https://nexo.io/'),
        ('Horizen', 'ZEN', 'ZEN' , 'https://www.horizen.io/'),
        ('SwissBorg', 'CHSB', 'CHSB' , 'https://swissborg.com/'),
        ('Decentraland', 'MANA', 'MANA' , 'https://decentraland.org/'),
        ('yearn.finance', 'YFI', 'YFI' , 'https://yearn.finance/'),
        ('Stacks', 'STX', 'BLOCKSTACK' , 'https://www.stacks.co/'),
        ('Celo', 'CELO', 'CELO' , 'https://celo.org/'),
        ('Theta Fuel', 'TFUEL', 'TFUEL' , 'https://www.thetatoken.org/'),
        ('Curve DAO Token', 'CRV', 'CRV' , 'https://curve.fi/'),
        ('Flow', 'FLOW', 'FLOW2' , 'https://www.onflow.org/'),
        ('Mina', 'MINA', 'MINA' , 'https://minaprotocol.com/'),
        ('Serum', 'SRM', 'SRM' , 'https://www.projectserum.com/'),
        ('OKB', 'OKB', 'OKB' , 'https://www.okex.com/'),
        ('Ren', 'REN', 'REN' , 'https://renproject.io/'),
        ('Mdex', 'MDX', 'MDX2' , 'https://mdex.co/'),
        ('Telcoin', 'TEL', 'TEL' , 'https://www.telco.in/'),
        ('Perpetual Protocol', 'PERP', 'PERP' , 'https://www.perp.fi/'),
        ('Bancor', 'BNT', 'BNT' , 'https://bancor.network/'),
        ('Audius', 'AUDIO', 'AUDIO' , 'https://audius.co/'),
        ('Raydium', 'RAY', 'RAY' , 'https://raydium.io/'),
        ('Ankr', 'ANKR', 'ANKR' , 'https://www.ankr.com/'),
        ('Golem', 'GLM', 'GNT' , 'https://golem.network/'),
        ('Dent', 'DENT', 'DENT' , 'https://www.dentwireless.com/'),
        ('Ocean Protocol', 'OCEAN', 'OCEAN' , 'https://oceanprotocol.com/'),
        ('Reserve Rights', 'RSR', 'RSR' , 'https://reserve.org/'),
        ('WOO Network', 'WOO', 'WOO' , 'https://woo.org/'),
        ('Storj', 'STORJ', 'STORJ' , 'https://storj.io/')
    ]
