// src/pages/CartPage.jsx
import React, { useContext, useState } from "react";
import { CartContext } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import { Modal, Button, Form } from "react-bootstrap";

const CartPage = () => {
  const { cart, setCart } = useContext(CartContext);
  const { user, authFetch } = useAuth();
  const [showModal, setShowModal] = useState(false);
  const [paymentInfo, setPaymentInfo] = useState({ method: "M-Pesa", number: "" });

  const total = cart.reduce((acc, item) => acc + item.price, 0);

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      const res = await authFetch("http://127.0.0.1:5000/api/payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          buyer_id: user?.id,
          items: cart.map((animal) => animal.id),
          total_amount: total,
          payment_method: paymentInfo.method,
          payment_number: paymentInfo.number,
        }),
      });

      if (res.ok) {
        alert("Payment successful!");
        setCart([]);
        setShowModal(false);
      } else {
        const err = await res.json();
        alert("Payment failed: " + err.message);
      }
    } catch (error) {
      alert("Payment error: " + error.message);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">🛒 My Cart</h2>

      {cart.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          <ul className="list-group mb-3">
            {cart.map((item) => (
              <li key={item.id} className="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <strong>{item.name}</strong> - {item.breed}
                </div>
                <span>KES {item.price.toLocaleString()}</span>
              </li>
            ))}
          </ul>

          <div className="d-flex justify-content-between align-items-center mb-4">
            <h5>Total: KES {total.toLocaleString()}</h5>
            <Button variant="success" onClick={() => setShowModal(true)}>
              Proceed to Payment
            </Button>
          </div>
        </>
      )}

      {/* Payment Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Complete Your Payment</Modal.Title>
        </Modal.Header>
        <Form onSubmit={handleCheckout}>
          <Modal.Body>
            <Form.Group controlId="paymentMethod">
              <Form.Label>Payment Method</Form.Label>
              <Form.Select
                value={paymentInfo.method}
                onChange={(e) => setPaymentInfo({ ...paymentInfo, method: e.target.value })}
              >
                <option>M-Pesa</option>
                <option>Airtel Money</option>
                <option>Card</option>
              </Form.Select>
            </Form.Group>

            <Form.Group controlId="paymentNumber" className="mt-3">
              <Form.Label>Phone or Card Number</Form.Label>
              <Form.Control
                type="text"
                value={paymentInfo.number}
                onChange={(e) => setPaymentInfo({ ...paymentInfo, number: e.target.value })}
                required
              />
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>
              Cancel
            </Button>
            <Button variant="primary" type="submit">
              Pay KES {total.toLocaleString()}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </div>
  );
};

export default CartPage;
