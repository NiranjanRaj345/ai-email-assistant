import React, { useEffect, useState } from "react";
import MainLayout from "../components/MainLayout";
import AnalyticsGraph from "../components/AnalyticsGraph";

export default function Dashboard() {
  const [emails, setEmails] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [loadingEmails, setLoadingEmails] = useState(true);
  const [loadingAnalytics, setLoadingAnalytics] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    setLoadingEmails(true);
    fetch("/api/emails")
      .then(res => res.json())
      .then(data => {
        setEmails(data);
        setLoadingEmails(false);
      });
    setLoadingAnalytics(true);
    fetch("/api/analytics")
      .then(res => res.json())
      .then(data => {
        setAnalytics(data);
        setLoadingAnalytics(false);
      });
  }, []);

  const filteredEmails = emails.filter(
    email =>
      email.subject.toLowerCase().includes(search.toLowerCase()) ||
      email.body.toLowerCase().includes(search.toLowerCase()) ||
      email.sender.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <MainLayout>
      <div>
        <h1 style={{ fontWeight: 700, fontSize: 32, marginBottom: 24 }}>Dashboard</h1>
        <div style={{ display: "flex", gap: 32 }}>
          <section style={{ flex: 2 }}>
            <h2 style={{ fontSize: 24, marginBottom: 16 }}>Support Emails</h2>
            <input
              type="text"
              placeholder="Search emails..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              style={{
                padding: "8px 12px",
                marginBottom: 18,
                borderRadius: 6,
                border: "1px solid #ccc",
                width: "100%",
                fontSize: 16
              }}
            />
            {loadingEmails ? (
              <div style={{ padding: 24, textAlign: "center" }}>Loading emails...</div>
            ) : filteredEmails.length === 0 ? (
              <div style={{ padding: 24, textAlign: "center", color: "#888" }}>No emails found.</div>
            ) : (
              <ul style={{ listStyle: "none", padding: 0 }}>
                {filteredEmails.map(email => (
                  <li key={email.id} style={{
                    background: "#f0f4fc",
                    marginBottom: 18,
                    padding: 18,
                    borderRadius: 8,
                    boxShadow: "0 2px 8px rgba(0,0,0,0.03)"
                  }}>
                    <strong>{email.subject}</strong> <span style={{ color: "#232946" }}>from {email.sender}</span> <br />
                    <em>{email.date}</em>
                    <p>{email.body}</p>
                    <span style={{ fontWeight: 500 }}>Sentiment: {email.sentiment} | Priority: {email.priority}</span>
                  </li>
                ))}
              </ul>
            )}
          </section>
          <section style={{ flex: 1 }}>
            <h2 style={{ fontSize: 24, marginBottom: 16 }}>Analytics</h2>
            {loadingAnalytics ? (
              <div style={{ padding: 24, textAlign: "center" }}>Loading analytics...</div>
            ) : (
              <>
                <div style={{ marginBottom: 12 }}>Total: {analytics.total}</div>
                <div style={{ marginBottom: 12 }}>Resolved: {analytics.resolved}</div>
                <div style={{ marginBottom: 12 }}>Pending: {analytics.pending}</div>
                <AnalyticsGraph analytics={analytics} />
              </>
            )}
          </section>
        </div>
        <section style={{ marginTop: 40 }}>
          <h2 style={{ fontSize: 24, marginBottom: 16 }}>AI Responses</h2>
          <div style={{
            background: "#e9ecef",
            padding: 18,
            borderRadius: 8,
            minHeight: 80,
            fontStyle: "italic"
          }}>
            Coming soon...
          </div>
        </section>
      </div>
    </MainLayout>
  );
}