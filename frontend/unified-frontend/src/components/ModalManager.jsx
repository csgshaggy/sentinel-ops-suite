// /src/components/ModalManager.jsx
import React, { createContext, useContext, useState, useCallback } from "react";
import { createPortal } from "react-dom";

const ModalContext = createContext(null);

export function ModalProvider({ children }) {
  const [modal, setModal] = useState(null);
  const [modalProps, setModalProps] = useState({});

  const openModal = useCallback((name, props = {}) => {
    setModal(name);
    setModalProps(props);
  }, []);

  const closeModal = useCallback(() => {
    setModal(null);
    setModalProps({});
  }, []);

  return (
    <ModalContext.Provider value={{ modal, modalProps, openModal, closeModal }}>
      {children}
      <ModalRoot modal={modal} modalProps={modalProps} closeModal={closeModal} />
    </ModalContext.Provider>
  );
}

export function useModal() {
  return useContext(ModalContext);
}

/* ------------------------------------------------------------
   Modal Root — renders whichever modal is active
------------------------------------------------------------- */

function ModalRoot({ modal, modalProps, closeModal }) {
  if (!modal) return null;

  return createPortal(
    <div className="modal-overlay">
      <div className="modal-container">
        {modal === "changePassword" && (
          <ChangePasswordModal {...modalProps} closeModal={closeModal} />
        )}

        {/* Future modals:
            modal === "mfa" && <MFAModal ... />
            modal === "sessions" && <SessionsModal ... />
        */}
      </div>
    </div>,
    document.body
  );
}

/* ------------------------------------------------------------
   Placeholder — real modal added in next step
------------------------------------------------------------- */

function ChangePasswordModal({ closeModal }) {
  return (
    <div className="modal-card">
      <h2>Change Password</h2>
      <p>Modal placeholder — real UI coming next.</p>

      <button onClick={closeModal} className="modal-close-btn">
        Close
      </button>
    </div>
  );
}
