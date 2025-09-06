import React from "react";
import { Bar } from "react-chartjs-2";
import { Chart, BarElement, CategoryScale, LinearScale } from "chart.js";
Chart.register(BarElement, CategoryScale, LinearScale);

export default function AnalyticsGraph({ analytics }) {
  const data = {
    labels: ["Positive", "Negative", "Neutral"],
    datasets: [
      {
        label: "Sentiment Distribution",
        data: [
          analytics.sentiments?.positive || 0,
          analytics.sentiments?.negative || 0,
          analytics.sentiments?.neutral || 0,
        ],
        backgroundColor: ["#4caf50", "#f44336", "#9e9e9e"],
      },
    ],
  };

  return (
    <div style={{ maxWidth: 400 }}>
      <Bar data={data} />
    </div>
  );
}