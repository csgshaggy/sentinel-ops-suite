#!/usr/bin/env node

/**
 * Makefile Dependency Graph Generator
 * -----------------------------------
 * Parses the Makefile and produces a Graphviz DOT file
 * showing target → dependency relationships.
 *
 * Output:
 *   scripts/make/makefile-graph.dot
 */

import fs from "fs";
import path from "path";

const projectRoot = process.cwd();
const makefilePath = path.join(projectRoot, "Makefile");
const outputPath = path.join(projectRoot, "scripts/make/makefile-graph.dot");

function parseMakefile(content) {
  const lines = content.split("\n");
  const edges = [];

  for (const line of lines) {
    // Match: target: dep1 dep2 dep3
    const match = line.match(/^([A-Za-z0-9._-]+)\s*:\s*(.*)$/);
    if (!match) continue;

    const target = match[1];
    const deps = match[2]
      .split(/\s+/)
      .filter((d) => d.length > 0 && !d.startsWith("#"));

    for (const dep of deps) {
      edges.push({ from: target, to: dep });
    }
  }

  return edges;
}

function generateDot(edges) {
  let dot = "digraph Makefile {\n";
  dot += '  rankdir="LR";\n';
  dot += "  node [shape=box, style=filled, color=lightgray];\n\n";

  for (const { from, to } of edges) {
    dot += `  "${from}" -> "${to}";\n`;
  }

  dot += "}\n";
  return dot;
}

(function run() {
  console.log("🔍 Generating Makefile dependency graph...");

  if (!fs.existsSync(makefilePath)) {
    console.error("❌ Cannot generate graph: Makefile not found.");
    process.exit(1);
  }

  const content = fs.readFileSync(makefilePath, "utf8");
  const edges = parseMakefile(content);
  const dot = generateDot(edges);

  fs.writeFileSync(outputPath, dot, "utf8");

  console.log("📈 Dependency graph written to:");
  console.log("   " + outputPath);
  process.exit(0);
})();
