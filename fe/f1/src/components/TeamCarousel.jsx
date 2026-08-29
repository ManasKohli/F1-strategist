import { useEffect, useState } from "react";
import mercedes from "../assets/5e03a8e5-ac2d-4e05-a029-c6d551dbd0a8.png";
import ferrari from "../assets/e41406ee-703f-43aa-bcbb-4efa0b6f4e6b.png";
import mclaren from "../assets/f1901729-2375-400c-910b-0d2266c26f79.png";

const teams = [
    { id: "ferrari", name: "Ferrari", image: ferrari },
    { id: "mclaren", name: "McLaren", image: mclaren },
    { id: "mercedes", name: "Mercedes", image: mercedes },
];

const TeamCarousel = () => {
    const [activeIndex, setActiveIndex] = useState(1);

    useEffect(() => {
        const intervalId = window.setInterval(() => {
            setActiveIndex((current) => (current + 1) % teams.length);
        }, 3200);

        return () => window.clearInterval(intervalId);
    }, []);

    const getOffset = (index) => {
        const difference = index - activeIndex;

        if (difference > 1) {
            return difference - teams.length;
        }

        if (difference < -1) {
            return difference + teams.length;
        }

        return difference;
    };

    return (
        <div className="hero__visual">
            <div className="team-carousel" aria-label="F1 team carousel">
                <div className="team-carousel__stage">
                    {teams.map((team, index) => {
                        const offset = getOffset(index);
                        const isActive = offset === 0;
                        const isVisible = Math.abs(offset) <= 1;

                        if (!isVisible) {
                            return null;
                        }

                        const x = offset * 170;
                        const y = isActive ? 0 : 28;
                        const scale = isActive ? 1 : 0.75;
                        const opacity = isActive ? 1 : 0.68;
                        const zIndex = isActive ? 5 : 3;
                        const rotateY = offset * 12;

                        return (
                            <button
                                key={team.id}
                                type="button"
                                className={`team-card ${isActive ? "is-active" : ""}`}
                                onClick={() => setActiveIndex(index)}
                                aria-label={`Show ${team.name}`}
                                style={{
                                    transform: `translate(-50%, -50%) translate3d(${x}px, ${y}px, 0) perspective(1000px) rotateY(${rotateY}deg) scale(${scale})`,
                                    opacity,
                                    zIndex,
                                }}
                            >
                                <img src={team.image} alt={`${team.name} team card`} className="team-card__image" />
                            </button>
                        );
                    })}
                </div>

                <div className="team-carousel__dots" aria-label="Carousel pagination">
                    {teams.map((team, index) => (
                        <button
                            key={team.id}
                            type="button"
                            className={`team-carousel__dot ${index === activeIndex ? "is-active" : ""}`}
                            onClick={() => setActiveIndex(index)}
                            aria-label={`Go to ${team.name}`}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default TeamCarousel;