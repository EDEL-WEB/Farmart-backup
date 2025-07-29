import React, { useState, useRef } from "react";
import axios from "axios";

const FarmerPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    breed: "",
    age: "",
    price: "",
    description: "",
    image: null,
  });

  const [preview, setPreview] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleChange = (e) => {
    const { name, value, files } = e.target;

    if (name === "image" && files[0]) {
      setFormData({ ...formData, image: files[0] });
      setPreview(URL.createObjectURL(files[0]));
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    const data = new FormData();
    for (const key in formData) {
      if (formData[key]) {
        data.append(key, formData[key]);
      }
    }

    try {
      await axios.post("http://localhost:5000/api/animals/", data);
      setMessage("✅ Animal uploaded successfully!");
      setFormData({
        name: "",
        breed: "",
        age: "",
        price: "",
        description: "",
        image: null,
      });
      setPreview(null);
      if (fileInputRef.current) fileInputRef.current.value = null;
    } catch (err) {
      console.error("Upload error:", err);
      setError("❌ Failed to upload animal. Please check your input or server.");
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Upload New Animal</h2>

      {message && <div className="alert alert-success">{message}</div>}
      {error && <div className="alert alert-danger">{error}</div>}

      <form onSubmit={handleSubmit} encType="multipart/form-data">
        {[
          { label: "Animal Name", name: "name", type: "text" },
          { label: "Breed", name: "breed", type: "text" },
          { label: "Age", name: "age", type: "number" },
          { label: "Price (KES)", name: "price", type: "number" },
        ].map(({ label, name, type }) => (
          <div className="mb-3" key={name}>
            <label className="form-label">{label}</label>
            <input
              type={type}
              className="form-control"
              name={name}
              value={formData[name]}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        <div className="mb-3">
          <label className="form-label">Description</label>
          <textarea
            className="form-control"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="3"
            required
          ></textarea>
        </div>

        <div className="mb-3">
          <label className="form-label">Image</label>
          <input
            type="file"
            className="form-control"
            name="image"
            accept="image/*"
            onChange={handleChange}
            ref={fileInputRef}
            required
          />
        </div>

        {preview && (
          <div className="mb-3">
            <img
              src={preview}
              alt="Preview"
              style={{ maxWidth: "200px", borderRadius: "10px" }}
            />
          </div>
        )}

        <button type="submit" className="btn btn-primary">Submit Animal</button>
      </form>
    </div>
  );
};

export default FarmerPage;
