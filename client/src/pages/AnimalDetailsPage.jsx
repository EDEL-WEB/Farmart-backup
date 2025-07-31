// src/pages/AnimalDetailsPage.jsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Container, Card, Button, Spinner } from "react-bootstrap";

const AnimalDetailsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [animal, setAnimal] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:5000/api/animals/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setAnimal(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch animal:", err);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <Spinner animation="border" className="m-5" />;

  if (!animal) return <p className="text-center mt-5">Animal not found.</p>;

  return (
    <Container className="mt-5">
      <Card className="text-center">
        <Card.Img
          variant="top"
          src={animal.picture_url}
          alt={animal.name}
          style={{ height: "400px", objectFit: "cover" }}
        />
        <Card.Body>
          <Card.Title>{animal.name}</Card.Title>
          <Card.Text>Breed: {animal.breed}</Card.Text>
          <Card.Text>Price: KES {animal.price}</Card.Text>
          <Card.Text>Description: {animal.description || "No description provided."}</Card.Text>
          <Button variant="success" onClick={() => navigate("/buyer")}>
            Proceed to Buy
          </Button>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default AnimalDetailsPage;
