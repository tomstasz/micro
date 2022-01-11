from flask import Flask, jsonify, request, abort
from json import JSONDecodeError
from models import Barrier, BarrierSchema
from app import app, db


@app.route("/api/v1/barrier", methods=["GET", "POST"])
def barrier_operations():
    """Open/close barrier depending on current status"""
    if request.method == "GET":
        barrier = Barrier.query.order_by(Barrier.updated_at.desc()).first()
        barrier_schema = BarrierSchema()
        result = barrier_schema.dump(barrier)
        return jsonify({"status": result["status"], "updated_at": result["updated_at"]})
    else:
        try:
            new_status = request.form["status"]
        except (KeyError, JSONDecodeError):
            abort(400)
        barrier = Barrier.query.order_by(Barrier.updated_at.desc()).first()
        barrier.status = new_status
        db.session.commit()
        barrier_schema = BarrierSchema()
        result = barrier_schema.dump(barrier)
        return jsonify({"status": result["status"], "updated_at": result["updated_at"]})


if __name__ == "__main__":
    app.run(debug=True)
