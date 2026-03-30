export default function Table({ columns, data }) {
  return (
    <table
      className="panel"
      style={{ width: "100%", borderCollapse: "collapse" }}
    >
      <thead>
        <tr>
          {columns.map((c) => (
            <th
              key={c}
              style={{
                textAlign: "left",
                padding: "0.5rem",
                borderBottom: "1px solid var(--border)",
              }}
            >
              {c}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i}>
            {columns.map((c) => (
              <td
                key={c}
                style={{
                  padding: "0.5rem",
                  borderBottom: "1px solid var(--border-light)",
                }}
              >
                {row[c]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
