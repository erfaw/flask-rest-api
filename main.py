from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func
from pathlib import Path
import os
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent
(ROOT_DIR / "instance").mkdir(exist_ok= True)
db_path = ROOT_DIR / 'instance' / 'cafes.db'
db_path.as_posix()

load_dotenv(ROOT_DIR/'.env')

app = Flask(__name__)

class Base(DeclarativeBase): pass

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
    def __repr__(self):
        return f"<Cafe: id={self.id}, name={self.name}>"
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()
print()

@app.route('/random')
def random():
    random_cafe = db.session.execute(
        db.select(Cafe).order_by(func.random()).limit(1)
    ).scalar_one_or_none()
    if random_cafe:
        return jsonify(cafe= random_cafe.to_dict())

@app.route('/')
def all_cafes():
    all_cafes_records = db.session.execute(
        db.select(Cafe).order_by(Cafe.id)
    ).scalars().all()
    return jsonify(
            all_cafes = [cafe.to_dict() for cafe in all_cafes_records]
        )

@app.route('/search')
def search():
    loc = request.args.get('loc').title()
    result = db.session.execute(
        db.select(Cafe).where(Cafe.location == loc)
    ).scalars().all()
    if len(result) != 0:
        return jsonify(
            cafe = [cafe.to_dict() for cafe in result]
        )
    else: 
        return jsonify(error={'Not Found': "Sorry, we don't have a cafe at that location."})

@app.route('/add', methods=["POST"])
def add():
    new_record = Cafe(
        name= request.form.get('name'),
        map_url= request.form.get('map_url'),
        img_url= request.form.get('img_url'),
        location= request.form.get('location'),
        seats= request.form.get('seats'),
        has_toilet= bool(int(request.form.get('has_toilet'))),
        has_wifi= bool(int(request.form.get('has_wifi'))),
        has_sockets= bool(int(request.form.get('has_sockets'))),
        can_take_calls= bool(int(request.form.get('can_take_calls'))),            
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify(
        result = {
            "success": "Successfully added the new cafe."
        }
    )

@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    new_price = request.args.get('new_price')
    record_to_update = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar_one_or_none()
    if record_to_update:
        record_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(
            result={
                "success": f"cafe_price successfully updated for <{record_to_update.name}> to <{new_price}>"
            }
        )
    else: 
        return jsonify(
            result={
                "Not Found": f"Sorry a cafe with that id=<{cafe_id}> was not found in the database.>"
            }
        ), 404
    
@app.route('/report-closed/<int:cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    recieved_api_key = request.args.get('api_key')
    true_api_key = os.environ.get('api_key')
    if recieved_api_key != true_api_key:
        return jsonify(
            result={
                "Unauthorized": "Your client doesn't have access to do that."
            }
        ), 403 
    record_to_delete = db.session.execute(
        db.select(Cafe).where(Cafe.id == cafe_id)
    ).scalar_one_or_none()
    if record_to_delete:
        deleted_name = record_to_delete.name
        deleted_id = record_to_delete.id
        db.session.delete(record_to_delete)
        db.session.commit()
        return jsonify(
            result={
                "success": f"cafe <{deleted_name}> (id={deleted_id}) successfully deleted."
            }
        ), 200
    else: 
        return jsonify(
            result={
                "Not Found": f"Sorry a cafe with that id=<{cafe_id}> was not found in the database.>"
            }
        ), 404

if __name__ == '__main__':
    app.run(debug=True)
