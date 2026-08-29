import { useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Project from './pages/Project';
import './styles/navbar.css';
import './styles/project.css';
import './styles/simulator.css';
import './styles/model.css';
import './index.css';

const App = () => {
    return (
        <>
            <Navbar />
            {/* Future route structure:
                <Routes>
                    <Route path="/project" element={<Project />} />
                    <Route path="/simulator" element={<Simulator />} />
                    <Route path="/model" element={<Model />} />
                </Routes>
            */}
            <Project />
            <Footer />
        </>
    );
};

export default App;