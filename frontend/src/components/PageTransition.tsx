import React from "react";
import { useLocation } from "react-router-dom";
import { CSSTransition, TransitionGroup } from "react-transition-group";

interface PageTransitionProps {
  children: React.ReactNode;
}

const PageTransition: React.FC<PageTransitionProps> = ({ children }) => {
  const location = useLocation();

  return (
    <TransitionGroup component={null}>
      <CSSTransition key={location.pathname} classNames="page" timeout={200}>
        <div className="page-transition">{children}</div>
      </CSSTransition>
    </TransitionGroup>
  );
};

export default PageTransition;
