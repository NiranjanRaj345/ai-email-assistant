import React, { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError("");
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (res.ok) {
      window.location.href = "/";
    } else {
      setError("Login failed. Please check your credentials.");
    }
    setLoading(false);
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minHeight: "100vh",
      background: "#f5f7fa"
    }}>
      <form onSubmit={handleSubmit} style={{
        background: "#fff",
        padding: 32,
        borderRadius: 12,
        boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
        minWidth: 320
      }}>
        <h2 style={{ marginBottom: 24 }}>Login to Email</h2>
        <input
          type="email"
          placeholder="Email address"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
          style={{
            width: "100%",
            padding: "10px 12px",
            marginBottom: 16,
            borderRadius: 6,
            border: "1px solid #ccc",
            fontSize: 16
          }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
          style={{
            width: "100%",
            padding: "10px 12px",
            marginBottom: 16,
            borderRadius: 6,
            border: "1px solid #ccc",
            fontSize: 16
          }}
        />
        {error && <div style={{ color: "red", marginBottom: 12 }}>{error}</div>}
        <button
          type="submit"
          disabled={loading}
          style={{
            width: "100%",
            padding: "10px 0",
            borderRadius: 6,
            background: "#232946",
            color: "#fff",
            fontWeight: "bold",
            fontSize: 18,
            border: "none"
          }}
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}