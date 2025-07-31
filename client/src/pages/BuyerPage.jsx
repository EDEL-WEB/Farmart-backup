import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Spinner,
  ListGroup,
  Form,
  Modal,
} from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { CartContext } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";

const BuyerPage = () => {
  const [animals, setAnimals] = useState([]);
  const [loading, setLoading] = useState(true);
  const { cart, setCart } = useContext(CartContext);
  const [showModal, setShowModal] = useState(false);
  const [paymentInfo, setPaymentInfo] = useState({ method: "", number: "", name: "" });
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [buyerName, setBuyerName] = useState("");
  const { authFetch } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAnimals = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/animals");
        setAnimals(response.data);
      } catch (error) {
        console.error("Error fetching animals:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnimals();
  }, []);

  const addToCart = (animal) => {
    if (!cart.find((item) => item.id === animal.id)) {
      setCart([...cart, animal]);
    }
  };

  const removeFromCart = (id) => {
    setCart(cart.filter((item) => item.id !== id));
  };

  const handlePayment = async (e) => {
    e.preventDefault();

    try {
      const res = await authFetch("http://localhost:5000/api/payments/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          method: paymentInfo.method,
          number: paymentInfo.number,
        }),
      });

      await res.json();
      setBuyerName(paymentInfo.name);
      setCart([]);
      setShowModal(false);
      setShowSuccessModal(true);
    } catch (error) {
      const errorMessage =
        error.response?.data?.error || "Payment failed. Please try again.";
      alert("Error: " + errorMessage);
      console.error("Payment error:", error.response?.data || error);
    }
  };

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <Container fluid className="mt-4">
      <Row>
        <Col md={8}>
          <h2>Available Animals</h2>
          <Row>
            {animals.map((animal) => (
              <Col md={4} key={animal.id} className="mb-3">
                <Card>
                  <Card.Body>
                    <Card.Title>{animal.name}</Card.Title>
                    <Card.Text>Breed: {animal.breed}</Card.Text>
                    <Card.Text>Price: KES {animal.price}</Card.Text>
                    <Button
                      variant="primary"
                      onClick={() => addToCart(animal)}
                      disabled={cart.find((item) => item.id === animal.id)}
                    >
                      {cart.find((item) => item.id === animal.id)
                        ? "In Cart"
                        : "Add to Cart"}
                    </Button>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Col>

        <Col md={4}>
          <h2>Cart</h2>
          <ListGroup>
            {cart.map((item) => (
              <ListGroup.Item key={item.id} className="d-flex justify-content-between">
                <div>
                  {item.name} - KES {item.price}
                </div>
                <Button variant="danger" size="sm" onClick={() => removeFromCart(item.id)}>
                  Remove
                </Button>
              </ListGroup.Item>
            ))}
          </ListGroup>
          <div className="mt-3">
            <strong>
              Total: KES{" "}
              {cart.reduce((acc, item) => acc + parseFloat(item.price), 0)}
            </strong>
          </div>
          <Button
            className="mt-3"
            variant="success"
            onClick={() => setShowModal(true)}
            disabled={cart.length === 0}
          >
            Proceed to Payment
          </Button>
        </Col>
      </Row>

      {/* Payment Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Payment</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handlePayment}>
            <Form.Group className="mb-3">
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter your name"
                value={paymentInfo.name}
                onChange={(e) =>
                  setPaymentInfo({ ...paymentInfo, name: e.target.value })
                }
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Payment Method</Form.Label>
              <Form.Select
                value={paymentInfo.method}
                onChange={(e) =>
                  setPaymentInfo({ ...paymentInfo, method: e.target.value })
                }
                required
              >
                <option value="">Select Method</option>
                <option value="mpesa">M-PESA</option>
                <option value="airtel">Airtel Money</option>
              </Form.Select>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Phone Number</Form.Label>
              <Form.Control
                type="tel"
                placeholder="Enter mobile number"
                value={paymentInfo.number}
                onChange={(e) =>
                  setPaymentInfo({ ...paymentInfo, number: e.target.value })
                }
                required
              />
            </Form.Group>
            <Button variant="success" type="submit">
              Pay Now
            </Button>
          </Form>
        </Modal.Body>
      </Modal>

      {/* Payment Success Modal */}
      <Modal show={showSuccessModal} onHide={() => setShowSuccessModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>✅ Payment Successful</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <h5>Thank you, {buyerName}! Welcome again.</h5>
          <p>Your order has been placed successfully.</p>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="success"
            onClick={() => {
              setShowSuccessModal(false);
              navigate("/");
            }}
          >
            Continue Shopping
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default BuyerPage;
