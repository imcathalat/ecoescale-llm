from flask import Blueprint, request, jsonify
from application.controllers.avaliacao_controller import avaliar_empresa_controller
from application.controllers.avaliacao_controller import avaliar_criterios_controller

routes = Blueprint("avaliar_empresa", __name__)

@routes.route("/avaliar-criterios", methods=["POST"])
def avaliar_criterios_route():
    return avaliar_criterios_controller()
    

@routes.route("/avaliar-empresa", methods=["POST"])
def avaliar_empresa_route():
    return avaliar_empresa_controller()

