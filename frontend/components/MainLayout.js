import React from "react";

export default function MainLayout({ children }) {
  return (
    <div style={{
      display: "flex",
      minHeight: "100vh",
      background: "#f5f7fa"
    }}>
      <aside style={{
        width: 220,
        background: "#232946",
        color: "#fff",
        padding: "32px 16px",
        fontWeight: "bold",
        fontSize: 20,
        boxShadow: "2px 0 8px rgba(0,0,0,0.04)"
      }}>
        <div style={{ marginBottom: 40 }}>
          <span role="img" aria-label="mail" style={{ fontSize: 32 }}>📧</span>
          <div>AI Email Assistant</div>
        </div>
        <nav>
          <div style={{ margin: "24px 0" }}>Dashboard</div>
          <div style={{ margin: "24px 0" }}>Analytics</div>
          <div style={{ margin: "24px 0" }}>Responses</div>
        </nav>
      </aside>
      <main style={{
        flex: 1,
        padding: "40px 48px",
        background: "#fff",
        borderRadius: 12,
        margin: 24,
        boxShadow: "0 4px 24px rgba(0,0,0,0.08)"
      }}>
        {children}
      </main>
    </div>
  );
}