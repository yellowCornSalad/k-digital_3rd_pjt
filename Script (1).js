use test01;

db.articles.insertMany(
[
{ subject: "coffee", author: "xyz", views: 50 },
{ subject: "Coffee Shopping", author: "efg", views: 5 },
{ subject: "Baking a cake", author: "abc", views: 90 },
{ subject: "baking", author: "xyz", views: 100 },
{ subject: "Café Con Leche", author: "abc", views: 200 },
{ subject: "Сырники", author: "jkl", views: 80 },
{ subject: "coffee and cream", author: "efg", views: 10 },

{ subject: "Cafe con Leche", author: "xyz", views: 10 },
{ subject: "coffees", author: "xyz", views: 10 },
{ subject: "coffee1", author: "xyz", views: 10 }
]
)

db.people.find()
db.people.find({ }, { user_id: 1, status: 1 })
db.people.find({ },{ user_id: 1, status: 1, _id: 0 })
db.people.find({ status: "A" })
db.people.find({ status: "A", age: 50 })
db.people.find({ $or: [ { status: "A" } , { age: 50 } ] }) 

db.people.find({ age: { $gt: 25 } }) 
db.people.find({ age: { $lt: 25 } }) 
db.people.find({ age: { $gt: 25, $lte: 50 } })
db.people.find({ age: { $nin: [ 5, 15 ] } } )
db.people.find( { user_id: /bc/ } )
db.people.find( { user_id: { $regex: /bc/ } } )
db.people.find( { user_id: /^bc/ } )
db.people.find( { user_id: { $regex: /^bc/ } } )
db.people.find( { status: "A" } ).sort( { user_id: 1 } ) 
db.people.find( { status: "A" } ).sort( { user_id: -1 } )
db.people.count()
db.people.find().count()
db.people.count( { user_id: { $exists: true } } )
db.people.find( { user_id: { $exists: true } } ).count()
db.people.count( { age: { $gt: 30 } } )
db.people.find( { age: { $gt: 30 } } ).count()
db.people.distinct( "status" ) 
db.people.findOne()
db.people.find().limit(1)


db.people.find( {status: