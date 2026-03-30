// =====================================================================
// SSRF Command Console — PageTransition
// Smooth animated transitions between route changes
// =====================================================================

import { ReactNode } from "react";
import { useLocation } from "react-router-dom";
import { CSSTransition, TransitionGroup } from "react-transition-group";

type Props = {
  children: ReactNode;
};

export default function PageTransition({ children }: Props) {
  const location = useLocation();

  return (
    <TransitionGroup component={null}>
      <CSSTransition
        key={location.pathname}
        classNames="page"
        timeout={200}
        unmountOnExit
      >
        <div className="page-transition-wrapper">{children}</div>
      </CSSTransition>
    </TransitionGroup>
  );
}
