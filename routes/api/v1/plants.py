from app import api, db
from flask import request
from flask_restful import Resource
from models.models import Plant as PlantModel

class PlantResource(Resource):
    def get(self):
        filter = request.args
        query = PlantModel.query
        if len(filter) < 1:
            plants = query.all()
        else:
            for key in filter.keys():
                print(key)
                plants = query.filter(getattr(PlantModel, key) == filter.get(key))

        plant_data = []
        for plant in plants:
            plant_data.append(plant.serialize())
        return plant_data

    def post(self):
        data = request.json
        plant = PlantModel(
            title=data.get("title"),
            location=data.get("location"),
        )
        db.session.add(plant)
        db.session.commit()
        return plant.serialize()

class SingPlantResource(Resource):
    def get(self, id):
        plant = PlantModel.query.get(id)
        return plant.serialize()

    def put(self, id):
        data = request.json
        plant = PlantModel.query.get(id)
        plant.title = data.get("title", plant.title)
        plant.location = data.get("location", plant.location)
        db.session.add(plant)
        db.session.commit()
        return plant.serialize()

    def delete(self, id):
        plant = PlantModel.query.get(id)
        db.session.delete(plant)
        db.session.commit()
        return plant.serialize()



api.add_resource(PlantResource, "/api/v1/plants")
api.add_resource(SingPlantResource, "/api/v1/plants/<int:id>")