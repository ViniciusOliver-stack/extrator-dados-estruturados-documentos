from ofxparse import OfxParser

def read_ofx_file(file_path: str) -> dict:
    with open(file_path, 'rb') as file:
        ofx = OfxParser.parse(file)
        transactions = []
        for account in ofx.accounts:
            for transaction in account.statement.transactions:
                transactions.append({
                    "date": transaction.date,
                    "amount": transaction.amount,
                    "description": transaction.memo
                })
        return {"transactions": transactions}
