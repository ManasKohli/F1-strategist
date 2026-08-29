import { useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ProjectOverview from './components/ProjectOverview';
import StrategyOutputPreview from './components/StrategyOutputPreview';
import FinalCta from './components/FinalCta';
import Footer from './components/Footer';
import './App.css';
import './index.css';

const App = () => {
    useEffect(() => {
        const elements = document.querySelectorAll('section, footer');

        if (!elements.length) {
            return undefined;
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                    }
                });
            },
            {
                threshold: 0.15,
                rootMargin: '0px 0px -30px 0px',
            }
        );

        elements.forEach((element) => {
            observer.observe(element);
        });

        return () => observer.disconnect();
    }, []);

    return (
        <>
            <Navbar />
            <Hero />
            <ProjectOverview />
            <StrategyOutputPreview />
            <FinalCta />
            <Footer />
        </>
    );
};

export default App;