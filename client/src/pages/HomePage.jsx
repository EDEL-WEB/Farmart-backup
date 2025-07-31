import React from "react";
import { Container, Row, Col, Card, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import '../components/HomePage.css';


const HomePage = () => {
  const navigate = useNavigate();

  const staticAnimals = [
    {
      id: 1,
      name: "Dairy Cow",
      breed: "Friesian",
      price: 75000,
      picture_url: "/static/images/animals/cow1.jpg",
    },
    {
      id: 2,
      name: "Boer Cow",
      breed: "Boer",
      price: 15000,
      picture_url: "/static/images/animals/bull2.jpg",
    },
    {
      id: 3,
      name: "Chicken",
      breed: "Indigenous",
      price: 800,
      picture_url: "/static/images/animals/chicken1.jpg",
    },
  ];

  return (
    <Container className="mt-5">

      {/* 🌟 Hero Section */}
      <div className="text-center mb-5 p-5 bg-light rounded shadow">
        <h1 className="display-4 fw-bold text-success">Welcome to Farmart</h1>
        <p className="lead">Connecting farmers and buyers for a smarter, healthier livestock trade.</p>
        <Button variant="success" size="lg" onClick={() => navigate("/animals")}>
          Browse Animals
        </Button>
      </div>

      {/* 🐄 Static Preview Section */}
      <h3 className="mb-4 text-success fw-bold">Popular Animals</h3>
      <Row className="mb-5">
        {staticAnimals.map((animal) => (
          <Col key={animal.id} sm={12} md={6} lg={4} className="mb-4">
            <Card className="h-100 shadow-sm">
              <Card.Img
                variant="top"
                src={animal.picture_url}
                alt={animal.name}
                style={{ height: "220px", objectFit: "cover" }}
              />
              <Card.Body>
                <Card.Title>{animal.name}</Card.Title>
                <Card.Text>
                  <strong>Breed:</strong> {animal.breed} <br />
                  <strong>Price:</strong> KES {animal.price.toLocaleString()}
                </Card.Text>
                <Button variant="outline-success" onClick={() => navigate("/animals")}>
                  View More
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {/* 🌟 Features Section */}
      <div className="p-4 rounded bg-white shadow-sm mb-5">
        <h2 className="text-center mb-4 fw-bold text-success">Why Farmers & Buyers ❤️ Farmart</h2>
        <Row className="text-center">
          <Col md={4} className="mb-3">
            <h5>🧑‍🌾 Verified Farmers</h5>
            <p>We partner only with genuine, trusted farmers across the country.</p>
          </Col>
          <Col md={4} className="mb-3">
            <h5>💼 Transparent Deals</h5>
            <p>No middlemen. Just fair prices, real animals, and clear details.</p>
          </Col>
          <Col md={4} className="mb-3">
            <h5>🔐 Safe & Simple Payments</h5>
            <p>Your transactions are secured with industry-standard encryption.</p>
          </Col>
        </Row>
      </div>

      {/* 🚀 How It Works Section */}
      <div className="p-4 rounded bg-white shadow-sm mb-5">
        <h2 className="text-center mb-4 fw-bold text-success">Get Started in 4 Easy Steps</h2>
        <Row className="text-center">
          <Col md={3}><span className="fw-bold">1️⃣ Register</span><br />Create your free Farmart account.</Col>
          <Col md={3}><span className="fw-bold">2️⃣ Explore</span><br />Browse a variety of quality animals.</Col>
          <Col md={3}><span className="fw-bold">3️⃣ Select</span><br />View animal details and add to cart.</Col>
          <Col md={3}><span className="fw-bold">4️⃣ Buy</span><br />Checkout securely and connect with the farmer.</Col>
        </Row>
      </div>

      {/* 📢 About Section */}
     <div className="p-4 rounded about-section shadow-sm">
  <h2 className="text-center mb-4 fw-bold text-success">What is Farmart?</h2>
  <p className="text-center fs-5">
    Farmart is Kenya’s modern digital livestock market. We're revolutionizing how farmers sell
    and how buyers discover livestock. With real-time listings, secure payments, and farmer profiles,
    Farmart builds trust, saves time, and helps agriculture grow.
  </p>
</div>

    </Container>
  );
};

export default HomePage;
