from app.extensions import db
from app.models import User, Farmer, Animal
from app import create_app
from sqlalchemy import text  # ✅ ADD THIS

def seed_data():
    print("🌱 Seeding data...")

    # ⛔ Wipe existing data safely
    db.session.execute(
        text("TRUNCATE orders, animals, farmers, users RESTART IDENTITY CASCADE")
    )
    db.session.commit()

    # Create a farmer user
    farmer_user = User(
        username="John Doe",
        email="farmer1@example.com",
        password="password123",
        role="farmer"
    )
    db.session.add(farmer_user)
    db.session.commit()

    # Create a farmer profile
    farmer_profile = Farmer(
        user_id=farmer_user.id,
        farm_name="Happy Farm",
        location="Homabay",
        farm_type="Mixed"
    )
    db.session.add(farmer_profile)
    db.session.commit()

    # Add animals linked to actual farmer
    animals = [
    Animal(
        name="Bull Alpha",
        breed="Boran",
        age=5,
        price=50000,
        type="Cattle",
        is_sold=False,
        picture_url="/static/images/animals/bull1.jpg",
        description="Strong and healthy Boran bull.",
        farmer_id=farmer_profile.id,
        user_id=farmer_user.id
    ),
    Animal(
        name="Bull Bravo",
        breed="Sahiwal",
        age=4,
        price=47000,
        type="Cattle",
        is_sold=False,
        picture_url="/static/images/animals/bull2.jpg",
        description="Well-fed Sahiwal bull ideal for breeding.",
        farmer_id=farmer_profile.id,
        user_id=farmer_user.id
    ),
    Animal(
        name="Chicken Classic",
        breed="Kienyeji",
        age=1,
        price=800,
        type="Poultry",
        is_sold=False,
        picture_url="/static/images/animals/chicken1.jpg",
        description="Free-range indigenous chicken.",
        farmer_id=farmer_profile.id,
        user_id=farmer_user.id
    ),
    Animal(
        name="Chicken Elite",
        breed="Broiler",
        age=1,
        price=1000,
        type="Poultry",
        is_sold=False,
        picture_url="/static/images/animals/chicken2.jpg",
        description="Fast-growing broiler chicken.",
        farmer_id=farmer_profile.id,
        user_id=farmer_user.id
    ),
    Animal(
        name="Cow Dairy",
        breed="Friesian",
        age=3,
        price=45000,
        type="Cattle",
        is_sold=False,
        picture_url="/static/images/animals/cow1.jpg",
        description="High milk-producing Friesian cow.",
        farmer_id=farmer_profile.id,
        user_id=farmer_user.id
    ),
    Animal(
        name="Cow Crossbreed",
        breed="Ayrshire",
        age=3,
        price=44000,
        type="Cattle",
        is_sold=False,
        picture_url="/static/images/animals/cow2.jpg",
        description="Ayrshire crossbreed cow suitable for dairy.",
        farmer_id=farmer_profile.id,
        user_id=farmer_user.id
    )
]

    db.session.add_all(animals)
    db.session.commit()
    print("✅ Done seeding!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_data()
