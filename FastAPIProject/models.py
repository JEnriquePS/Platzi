from pydantic import BaseModel


class Customer(BaseModel):
    id: int
    name: str
    description: str | None
    email: str
    age: int


class Transaction(BaseModel):
    id: int
    amount: float
    description: str | None


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: float

    @property
    def total(self):
        return sum(transaction.ammount for transaction in self.transactions)