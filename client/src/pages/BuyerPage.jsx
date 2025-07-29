import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../api/axios";
import { Container, Form, Button, Alert, Card } from "react-bootstrap";

const FarmerPage = () => {
  const { user, token } = useAuth();
  const [animals, setAnimals] = useState([]);
  const [formData, setFormData] = useState({
    name: "",
    breed: "",
    age: "",
    price: "",
    description: "",
  });
  const [imageFile, setImageFile] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Fetch user animals
  useEffect(() => {
    if (token) {
      api
        .get("/animals", {
          headers: { Authorization: `Bearer ${token}` },
          withCredentials: true,
        })
        .then((res) => {
          const userAnimals = res.data.filter((a) => a.farmer_id === user?.id);
          setAnimals(userAnimals);
        })
        .catch(() => setError("Failed to fetch your animals."));
    }
  }, [token, user?.id]);

  // Handle form input
  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === "image") {
      setImageFile(files[0]);
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  // Submit animal data with image in single request
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Validate required fields
    if (!formData.name || !formData.breed || !formData.age || !formData.price || !imageFile) {
      setError("Please fill in all required fields and select an image.");
      return;
    }

    try {
      // Create FormData with all fields including image
      const submitData = new FormData();
      submitData.append("name", formData.name);
      submitData.append("breed", formData.breed);
      submitData.append("age", formData.age);
      submitData.append("price", formData.price);
      submitData.append("description", formData.description);
      submitData.append("image", imageFile);

      // Single request to create animal
      const res = await api.post("/animals/", submitData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true,
      });

      setAnimals([...animals, res.data]);
      setSuccess("Animal uploaded successfully!");
      
      // Reset form
      setFormData({
        name: "",
        breed: "",
        age: "",
        price: "",
        description: "",
      });
      setImageFile(null);
      
      // Reset file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = '';

    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.error || "Upload failed. Check form and try again."
      );
    }
  };

  return (
    <Container className="mt-5">
      <h2>Welcome {user?.email || "Farmer"}</h2>
      <h4 className="mt-3">Upload a New Animal</h4>

      {error && <Alert variant="danger">{error}</Alert>}
      {success && <Alert variant="success">{success}</Alert>}

      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Name</Form.Label>
          <Form.Control 
            name="name" 
            value={formData.name} 
            onChange={handleChange} 
            required 
            placeholder="Enter animal name"
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Breed</Form.Label>
          <Form.Control 
            name="breed" 
            value={formData.breed} 
            onChange={handleChange} 
            required 
            placeholder="Enter breed"
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Age</Form.Label>
          <Form.Control 
            type="number" 
            name="age" 
            value={formData.age} 
            onChange={handleChange} 
            required 
            min="0"
            placeholder="Enter age in years"
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Price (KES)</Form.Label>
          <Form.Control 
            type="number" 
            name="price" 
            value={formData.price} 
            onChange={handleChange} 
            required 
            min="0"
            step="0.01"
            placeholder="Enter price in KES"
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Description (optional)</Form.Label>
          <Form.Control 
            as="textarea" 
            rows={3} 
            name="description" 
            value={formData.description} 
            onChange={handleChange}
            placeholder="Enter description (optional)"
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Image</Form.Label>
          <Form.Control 
            type="file" 
            name="image" 
            accept="image/*" 
            onChange={handleChange} 
            required 
          />
          {imageFile && (
            <Form.Text className="text-muted">
              Selected: {imageFile.name}
            </Form.Text>
          )}
        </Form.Group>

        <Button variant="primary" type="submit">
          Upload Animal
        </Button>
      </Form>

      <hr />
      <h4 className="mt-4">Your Uploaded Animals</h4>
      {animals.length === 0 ? (
        <p className="text-muted">No animals uploaded yet.</p>
      ) : (
        <div className="d-flex flex-wrap gap-3">
          {animals.map((animal) => (
            <Card key={animal.id} style={{ width: "18rem" }}>
              <Card.Img
                variant="top"
                src={
                  animal.picture_url?.startsWith("/")
                    ? `http://localhost:5000${animal.picture_url}`
                    : animal.picture_url
                }
                onError={(e) => {
                  e.target.src = "http://localhost:5000/fallback.jpg";
                }}
                style={{ height: "200px", objectFit: "cover" }}
              />
              <Card.Body>
                <Card.Title>{animal.name}</Card.Title>
                <Card.Text>
                  <strong>Breed:</strong> {animal.breed}<br />
                  <strong>Age:</strong> {animal.age} years<br />
                  <strong>Price:</strong> KES {animal.price}
                  {animal.description && (
                    <>
                      <br />
                      <strong>Description:</strong> {animal.description}
                    </>
                  )}
                </Card.Text>
              </Card.Body>
            </Card>
          ))}
        </div>
      )}
    </Container>
  );
};

export default FarmerPage;