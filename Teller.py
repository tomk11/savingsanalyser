import requests
import json
import io
import moment

# Make it work for Python 2+3 and with Unicode
try:
    toUnicode = unicode
except NameError:
    toUnicode = str

clases = {''}   

class Transaction:
    def __init__(self, transactionsJson):
        self.json = transactionsJson
        self.counterparty = toUnicode(self.json[u'counterparty'])
        self.amount = float(self.json[u'amount'])
        self.date = moment.date(self.json[u'date'], "%Y-%m-%d")

    def __repr__(self):
        return "{} on {} to {}".format(self.amount, self.date.format("YYYY-M-D"), self.counterparty)

# Read JSON file if we have it
try:
    with open('data.json') as dataFile:
        data = json.load(dataFile)
        initJson=data[u'init']
        transactionsJson=data[u'transactions']
except (IOError, KeyError, ValueError):
    BearerID = 'Bearer {}'.format(apiKey)
    initRequest = requests.get('https://api.teller.io/accounts',headers={'Authorization': BearerID})
    initJson = initRequest.json()
    transactionsUrl = initJson[0][u'links'][u'transactions']
    transactionsRequest = requests.get(transactionsUrl, headers={'Authorization': BearerID})
    transactionsJson = transactionsRequest.json()
    data={u'init': initJson, u'transactions':transactionsJson} 
    # Write JSON file
    with io.open('data.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data,
            indent=4, 
            separators=(',', ': '), ensure_ascii=False)
        outfile.write(toUnicode(str_))

if __name__=='__main__':
    transactions = []
    for t in data[u'transactions']:
        transactions.append(Transaction(t))







