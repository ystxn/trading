from ibind import IbkrClient
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Ibkr:
    def get_positions(self):
        client = IbkrClient(host='ibeam')
        account_id = client.portfolio_accounts().data[0]['id']
        full_positions = client.positions(account_id = account_id).data

        marketdata_fields = {
            '31': 'lastPrice',
            '80': 'unrealizedPnlPercent',
            '78': 'dailyPnl',
            '83': 'changePercent'
        }
        client.portfolio_accounts()
        marketdata = client.live_marketdata_snapshot(
            conids = [ str(item['conid']) for item in full_positions ],
            fields = list(marketdata_fields.keys())
        ).data

        marketdata_fields['conid'] = 'conid'
        processed_marketdata = [
            { marketdata_fields[key]: value for key, value in item.items() if key in marketdata_fields }
            for item in marketdata
        ]

        positions_fields = [ 'avgCost', 'conid', 'ticker', 'name', 'unrealizedPnl', 'mktValue' ]
        positions = [
            { k: v for k, v in d.items() if k in positions_fields }
            for d in full_positions
        ]

        merged = [
            { **pos, **next(md for md in processed_marketdata if md['conid'] == pos['conid']) }
            for pos in positions
        ]

        return merged
