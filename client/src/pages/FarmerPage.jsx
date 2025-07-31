import React, { useState } from "react";
import axios from "axios";

const FarmerPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    breed: "",
    age: "",
    price: "",
    description: "",
    type: "",
    image: null,
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === "image") {
      setFormData({ ...formData, image: files[0] });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    const data = new FormData();
    for (const key in formData) {
      if (formData[key]) {
        data.append(key, formData[key]);
      }
    }

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setMessage("Authentication token missing.");
        return;
      }

      const response = await axios.post("http://localhost:5555/api/animals", data, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true,
      });

      setMessage("✅ Animal uploaded successfully!");
      setFormData({
        name: "",
        breed: "",
        age: "",
        price: "",
        description: "",
        type: "",
        image: null,
      });
    } catch (error) {
      if (error.response?.data?.error) {
        setMessage(` Error: ${error.response.data.error}`);
      } else {
        setMessage(" Upload failed. Check server or connection.");
      }
      console.error("Upload error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Upload Animal for Sale</h2>

      {message && <div className="alert alert-info">{message}</div>}

      <form onSubmit={handleSubmit} encType="multipart/form-data">
        <div className="mb-3">
          <label className="form-label">Animal Name</label>
          <input
            type="text"
            className="form-control"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Breed</label>
          <input
            type="text"
            className="form-control"
            name="breed"
            value={formData.breed}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Age</label>
          <input
            type="number"
            className="form-control"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Price</label>
          <input
            type="number"
            className="form-control"
            name="price"
            value={formData.price}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Animal Type</label>
          <select
            className="form-select"
            name="type"
            value={formData.type}
            onChange={handleChange}
            required
          >
            <option value="">-- Select Type --</option>
            <option value="cow">Cow</option>
            <option value="goat">Goat</option>
            <option value="sheep">Sheep</option>
            <option value="chicken">Chicken</option>
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Description</label>
          <textarea
            className="form-control"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="3"
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Upload Image</label>
          <input
            type="file"
            className="form-control"
            name="image"
            accept="image/*"
            onChange={handleChange}
            required
          />
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading}
        >
          {loading ? "Uploading..." : "Upload Animal"}
        </button>
      </form>
    </div>
  );
};

export default FarmerPage;
