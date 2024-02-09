from flask import Blueprint, jsonify, request
from sqlalchemy import or_, and_
from .database import db
from .models import Chambre, Reservation, Client
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify({'message': 'Hello !'})


# Searching available rooms
@main.route('/api/chambres/disponibles', methods=['GET'])
def recherche_chambres_disponibles():
    date_arrivee = request.args.get('date_arrivee')
    date_depart = request.args.get('date_depart')

    if not date_arrivee or not date_depart:
        return jsonify({'error': 'Veuillez fournir les dates de recherche.'}), 400

    try:
        date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d')
        date_depart = datetime.strptime(date_depart, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Format de date invalide. Utilisez le format YYYY-MM-DD.'}), 400

    chambres_disponibles = Chambre.query.filter(
        ~Chambre.reservations.any(and_(
            or_(Reservation.date_arrivee <= date_arrivee, Reservation.date_arrivee >= date_depart),
            or_(Reservation.date_depart <= date_arrivee, Reservation.date_depart >= date_depart)
        ))
    ).all()

    result = []
    for chambre in chambres_disponibles:
        result.append({
            'id': chambre.id,
            'numero': chambre.numero,
            'type': chambre.type,
            'prix': chambre.prix
        })

    return jsonify(result)


# Creating a reservation
@main.route('/api/reservations', methods=['POST'])
def creation_reservation():
    data = request.get_json()

    # Check if all necessary data is present in the request body
    required_fields = ['id_client', 'id_chambre', 'date_arrivee', 'date_depart']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis dans le corps de la requête.'}), 400

    # Convert dates to datetime objects
    try:
        date_arrivee = datetime.strptime(data['date_arrivee'], '%Y-%m-%d')
        date_depart = datetime.strptime(data['date_depart'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Format de date invalide. Utilisez le format YYYY-MM-DD.'}), 400

    # Check room availability
    chambre = Chambre.query.get(data['id_chambre'])
    if not chambre:
        return jsonify({'error': 'Chambre non trouvée.'}), 404

    reservations_overlap = chambre.reservations.filter(
        and_(
            or_(Reservation.date_arrivee <= date_arrivee, Reservation.date_arrivee >= date_depart),
            or_(Reservation.date_depart <= date_arrivee, Reservation.date_depart >= date_depart)
        )
    ).all()

    if reservations_overlap:
        return jsonify({'error': 'La chambre n\'est pas disponible pour les dates demandées.'}), 400

    # Create a reservation
    nouvelle_reservation = Reservation(
        id_client=data['id_client'],
        id_chambre=data['id_chambre'],
        date_arrivee=date_arrivee,
        date_depart=date_depart,
        statut='confirmee'
    )

    db.session.add(nouvelle_reservation)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Réservation créée avec succès.'})


# Cancel a reservation
@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def annulation_reservation(id):
    reservation = Reservation.query.get(id)

    if not reservation:
        return jsonify({'error': 'Réservation non trouvée.'}), 404

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Réservation annulée avec succès.'})


# Room management

## Add a room
@main.route('/api/chambres', methods=['POST'])
def ajouter_chambre():
    data = request.get_json()

    # Check if all necessary data is present in the request body
    required_fields = ['numero', 'type', 'prix']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis dans le corps de la requête.'}), 400

    # Create a new room
    nouvelle_chambre = Chambre(
        numero=data['numero'],
        type=data['type'],
        prix=data['prix']
    )

    db.session.add(nouvelle_chambre)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre ajoutée avec succès.'})

## Edit a room
@main.route('/api/chambres/<int:id>', methods=['PUT'])
def modifier_chambre(id):
    chambre = Chambre.query.get(id)

    if not chambre:
        return jsonify({'error': 'Chambre non trouvée.'}), 404

    data = request.get_json()

    # Check if all necessary data is present in the request body
    required_fields = ['numero', 'type', 'prix']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis dans le corps de la requête.'}), 400

    # Update room information
    chambre.numero = data['numero']
    chambre.type = data['type']
    chambre.prix = data['prix']

    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre mise à jour avec succès.'})

## Delete a room
@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def supprimer_chambre(id):
    chambre = Chambre.query.get(id)

    if not chambre:
        return jsonify({'error': 'Chambre non trouvée.'}), 404

    db.session.delete(chambre)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Chambre supprimée avec succès.'})


# Create a client
@main.route('/api/clients', methods=['POST'])
def creation_client():
    data = request.get_json()

    # Check if all necessary data is present in the request body
    required_fields = ['nom', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Le champ {field} est requis dans le corps de la requête.'}), 400

    # Check if the email is unique
    existing_client = Client.query.filter_by(email=data['email']).first()
    if existing_client:
        return jsonify({'error': 'Un client avec cet email existe déjà.'}), 400

    # Create a new client
    nouveau_client = Client(
        nom=data['nom'],
        email=data['email']
    )

    db.session.add(nouveau_client)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Client créé avec succès.'})