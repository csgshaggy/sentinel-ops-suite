// /src/components/CommandPalette.jsx

import React, { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useCommandPalette } from "../state/commandPaletteState.js";
import "./CommandPalette.css";

export default function CommandPalette() {
  const {
    isOpen,
    closePalette,
    query,
    setQuery,
    results,
    selectedIndex,
    moveSelectionUp,
    moveSelectionDown,
    selectCurrent,
  } = useCommandPalette();

  const navigate = useNavigate();
  const inputRef = useRef(null);

  // Close on ESC
  useEffect(() => {
    const handler = (e) => {
      if (e.key === "Escape") closePalette();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [closePalette]);

  // Keyboard navigation
  useEffect(() => {
    const handler = (e) => {
      if (!isOpen) return;

      if (e.key === "ArrowDown") {
        e.preventDefault();
        moveSelectionDown();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        moveSelectionUp();
      } else if (e.key === "Enter") {
        e.preventDefault();
        const item = results[selectedIndex];
        if (item) {
          navigate(item.path);
          closePalette();
        }
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [isOpen, results, selectedIndex, navigate, closePalette, moveSelectionDown, moveSelectionUp]);

  // Autofocus when opened
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current.focus(), 10);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="cmdp-overlay" onClick={closePalette}>
      <div className="cmdp-container" onClick={(e) => e.stopPropagation()}>
        <input
          ref={inputRef}
          className="cmdp-input"
          placeholder="Search commands, pages…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <div className="cmdp-results">
          {results.length === 0 ? (
            <div className="cmdp-empty">No matches</div>
          ) : (
            results.map((item, index) => (
              <div
                key={item.path}
                className={`cmdp-item ${index === selectedIndex ? "selected" : ""}`}
                onClick={() => {
                  navigate(item.path);
                  closePalette();
                }}
              >
                <span className="cmdp-icon">{item.icon}</span>
                <div className="cmdp-text">
                  <div className="cmdp-title">{item.label}</div>
                  <div className="cmdp-sub">{item.path}</div>
                </div>
                <div className="cmdp-kb">↵</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
