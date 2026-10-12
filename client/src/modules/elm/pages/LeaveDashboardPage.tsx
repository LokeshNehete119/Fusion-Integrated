import { useEffect, useState } from "react";
import {
  fetchMyApplications,
  fetchMyBalances,
  type LeaveApplication,
  type LeaveBalance,
} from "../api";

export default function LeaveDashboardPage() {
  const [balances, setBalances] = useState<LeaveBalance[]>([]);
  const [applications, setApplications] = useState<LeaveApplication[]>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    Promise.all([fetchMyBalances(), fetchMyApplications()])
      .then(([balData, appData]) => {
        setBalances(balData);
        setApplications(appData);
      })
      .catch((err) => setError(err.message || "Could not load leave data"));
  }, []);

  return (
    <div style={{ padding: "1.5rem" }}>
      <h2>Employee Leave Dashboard</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <h3>My Leave Balances</h3>
      <table border={1} cellPadding={8} style={{ borderCollapse: "collapse", width: "100%", marginBottom: "1.5rem" }}>
        <thead>
          <tr>
            <th>Leave Type</th>
            <th>Year</th>
            <th>Allocated</th>
            <th>Used</th>
            <th>Remaining</th>
          </tr>
        </thead>
        <tbody>
          {balances.map((b) => (
            <tr key={b.id}>
              <td>{b.leave_type}</td>
              <td>{b.year}</td>
              <td>{b.total_allocated}</td>
              <td>{b.used_days}</td>
              <td>{b.remaining_days}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>My Leave Applications</h3>
      <table border={1} cellPadding={8} style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>From</th>
            <th>To</th>
            <th>Days</th>
            <th>Status</th>
            <th>Remarks</th>
          </tr>
        </thead>
        <tbody>
          {applications.map((app) => (
            <tr key={app.id}>
              <td>{app.id}</td>
              <td>{app.leave_type}</td>
              <td>{app.start_date}</td>
              <td>{app.end_date}</td>
              <td>{app.total_days}</td>
              <td>{app.status}</td>
              <td>{app.review_remarks || "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
