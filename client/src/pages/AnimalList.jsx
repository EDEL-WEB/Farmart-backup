import React, { useEffect, useState } from "react";
import { Container, Row, Col, Card, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const AnimalList = () => {
  const [animals, setAnimals] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:5000/api/animals/")
      .then((res) => res.json())
      .then((data) => setAnimals(data))
      .catch((err) => console.error("Failed to fetch animals:", err));
  }, []);

  const handleViewAnimal = (id) => {
    navigate(`/animals/${id}`);
  };

  return (
    <Container className="mt-5">
      <h2 className="mb-4 text-center">All Available Animals</h2>
      <Row>
        {animals.map((animal) => (
          <Col key={animal.id} sm={12} md={6} lg={4} className="mb-4">
            <Card>
              <Card.Img
                variant="top"
                src={animal.picture_url}
                alt={animal.name}
                style={{ height: "200px", objectFit: "cover" }}
              />
              <Card.Body>
                <Card.Title>{animal.name}</Card.Title>
                <Card.Text>Breed: {animal.breed}</Card.Text>
                <Card.Text>Price: KES {animal.price}</Card.Text>
                <Button variant="info" onClick={() => handleViewAnimal(animal.id)}>
                  View Animal
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default AnimalList;
