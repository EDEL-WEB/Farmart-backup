// src/pages/CartPage.jsx
import React, { useContext, useEffect, useState } from "react";
import { Container, ListGroup, Button, Alert, Row, Col, Card } from "react-bootstrap";
import { Link } from "react-router-dom";
import api from "../api/axios"; // your axios instance

const CartContext = React.createContext(); // Replace with actual import if needed

function CartPage() {
  const { cart, setCart } = useContext(CartContext);
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [latestAnimals, setLatestAnimals] = useState([]);

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  useEffect(() => {
    if (cart.length === 0 && !orderPlaced) {
      api
        .get("/animals/")
        .then((res) => {
          const latest = res.data.slice(-3).reverse(); // last 3
          setLatestAnimals(latest);
        })
        .catch((err) => console.error("Failed to load animals:", err));
    }
  }, [cart, orderPlaced]);

  const handleCheckout = () => {
    setOrderPlaced(true);
    setCart([]);
  };

  return (
    <Container className="mt-5">
      <h2 className="text-center mb-4">🛒 My Cart</h2>

      {cart.length === 0 && !orderPlaced && (
        <>
          <Alert variant="info">Your cart is currently empty.</Alert>
          <div className="text-center mb-4">
            <Link to="/animals">
              <Button variant="outline-primary">Browse Animals</Button>
            </Link>
          </div>

          <h5 className="mb-3">Try These</h5>
          <Row>
            {latestAnimals.map((animal) => (
              <Col key={animal.id} sm={12} md={6} lg={4} className="mb-3">
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
                    <Link to="/animals">
                      <Button variant="success">View Details</Button>
                    </Link>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </>
      )}

      {orderPlaced && (
        <Alert variant="success">✅ Order placed successfully!</Alert>
      )}

      {cart.length > 0 && (
        <>
          <ListGroup className="mb-3">
            {cart.map((item, index) => (
              <ListGroup.Item key={index}>
                {item.name} - KES {item.price}
              </ListGroup.Item>
            ))}
          </ListGroup>

          <h5>Total: KES {total}</h5>

          <Button variant="primary" onClick={handleCheckout}>
            Place Order
          </Button>
        </>
      )}
    </Container>
  );
}

export default CartPage;