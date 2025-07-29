import React, { useEffect, useState } from "react";
import { Spinner, Table } from "react-bootstrap";
import api from "../api/axios"; // ✅ use axios instance

function OrderList() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/orders/")
      .then((res) => {
        console.log("✅ Fetched orders:", res.data);
        setOrders(res.data.orders || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("❌ Failed to fetch orders:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" />
        <p>Loading orders...</p>
      </div>
    );
  }

  if (!orders.length) {
    return <p className="text-center text-muted mt-5">No orders available.</p>;
  }

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Orders List</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Order ID</th>
            <th>Animal</th>
            <th>Buyer</th>
            <th>Paid</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.animal?.name || "N/A"}</td>
              <td>{order.user?.name || "N/A"}</td>
              <td>{order.paid ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default OrderList;
