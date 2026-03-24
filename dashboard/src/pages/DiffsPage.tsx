import React from "react";
import MakefileDiffViewer from "../widgets/MakefileDiffViewer";

export default function DiffsPage() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Diff Viewer</h1>
      <MakefileDiffViewer />
    </div>
  );
}
