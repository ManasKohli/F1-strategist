import { useEffect } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Project from "./pages/Project";
import Simulator from "./pages/Simulator";
import Model from "./pages/Model";

import "./styles/navbar.css";
import "./styles/project.css";
import "./styles/simulator.css";
import "./styles/model.css";
import "./index.css";


const AppContent = () => {
  const location = useLocation();

  useEffect(() => {
    const sections = document.querySelectorAll("section, footer");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
          }
        });
      },
      {
        threshold: 0.1,
      }
    );

    sections.forEach((section) => {
      observer.observe(section);
    });

    return () => {
      observer.disconnect();
    };
  }, [location.pathname]);


  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/" element={<Project />} />
        <Route path="/project" element={<Project />} />
        <Route path="/simulator" element={<Simulator />} />
        <Route path="/model" element={<Model />} />
      </Routes>

      <Footer />
    </>
  );
};


const App = () => {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
};


export default App;