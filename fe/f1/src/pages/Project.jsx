import Hero from '../components/Hero';
import ProjectOverview from '../components/ProjectOverview';
import StrategyOutputPreview from '../components/StrategyOutputPreview';
import FinalCta from '../components/FinalCta';
import '../styles/project.css';

const Project = () => {
    return (
        <>
            <Hero />
            <ProjectOverview />
            <StrategyOutputPreview />
            <FinalCta />
        </>
    );
};

export default Project;
