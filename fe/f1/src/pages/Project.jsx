import Hero from "../components/Hero";
import ProjectOverview from "../components/ProjectOverview";
import StrategyOutputPreview from "../components/StrategyOutputPreview";
import FinalCta from "../components/FinalCta";
import "../styles/project.css";

const Project = () => {
  return (
    <main className="project-page">
      <Hero />
      <ProjectOverview />
      <StrategyOutputPreview />
      <FinalCta />
    </main>
  );
};

export default Project;