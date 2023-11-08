use velocurien

db.createCollection("restaurants")

restaurants = db['restaurants']
restos_a_filter = db['restaurants_raw']

types_autorises = ['Bar laitier', 'Bar laitier saisonnier', 'Bar salon, taverne', 'Boulangerie', 'Brasserie', 'Casse-croûte', 'Pâtisserie', 'Restaurant', 'Restaurent mets pour emporter', 'Restaurant service rapide']

restos_a_garder = restos_a_filter.find({"properties.statut":{$eq:"Ouvert"}, "properties.type":{$in:types_autorises}, geometry:{$ne:null}}).toArray()

restaurants.insertMany(restos_a_garder)
