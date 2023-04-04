db = db.getSiblingDB('allowance');

db.createCollection('Family');

db.Family.insertMany([
 { 
    "_id": new ObjectId("642b09500fec1b9fe4ab78ae"),
    "name": "Green",
    "guardians": [
        "642b03b9f0d9fe0007309f0e",
        "642b050c62d9566c1c02abe5"
    ]
  }
]);

db.createCollection('User');

db.User.insertMany([
    {
        "_id": new ObjectId("642b03b9f0d9fe0007309f0e"),
        "name": "John",
        "password": "1234",
        "type": "guardian",
        "familyId": "642b09500fec1b9fe4ab78ae"
    },
    {
        "_id": new ObjectId("642b03b9f0d9fe0007309f0f"),
        "name": "Bob",
        "password": "1234",
        "type": "child",
        "familyId": "642b09500fec1b9fe4ab78ae"
    },
    {
        "_id": new ObjectId("642b03b9f0d9fe0007309f10"),
        "name": "Kyle",
        "password": "1234",
        "type": "child",
        "familyId": "642b09500fec1b9fe4ab78ae"
    },
    {
        "_id": new ObjectId("642b050c62d9566c1c02abe5"),
        "name": "Mary",
        "password": "1234",
        "type": "child",
        "familyId": "642b09500fec1b9fe4ab78ae"
    }
]);

db.createCollection('Ledger');

db.Ledger.insertMany([
    {
        "userId": "642b03b9f0d9fe0007309f0f",
        "amount": 100,
        "type": "gift"
    },
    {
        "userId": "642b03b9f0d9fe0007309f10",
        "amount": 125,
        "type": "gift"
    },
    {
        "userId": "642b03b9f0d9fe0007309f0f",
        "amount": -30,
        "type": "withdrawal"
    },
    {
        "userId": "642b03b9f0d9fe0007309f10",
        "amount": -100,
        "type": "withdrawal"
    },
    {
        "userId": "642b03b9f0d9fe0007309f0f",
        "amount": 25,
        "type": "chores"
    },
]);