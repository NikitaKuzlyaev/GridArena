import React, { useEffect, useState, useRef } from 'react';

const FLOWER_SVGS = [
  // Цветочек 1 — классический с пятью лепестками
  (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
      <circle cx="16" cy="16" r="5" fill="#f48fb1"/>
      <ellipse cx="16" cy="7" rx="4" ry="7" fill="#f8bbd0"/>
      <ellipse cx="16" cy="25" rx="4" ry="7" fill="#f8bbd0"/>
      <ellipse cx="7" cy="16" rx="7" ry="4" fill="#f8bbd0"/>
      <ellipse cx="25" cy="16" rx="7" ry="4" fill="#f8bbd0"/>
    </svg>
  ),
  // Цветочек 2 — ромашка
  (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
      <circle cx="16" cy="16" r="4" fill="#fff176"/>
      <ellipse cx="16" cy="7" rx="3" ry="7" fill="#fff"/>
      <ellipse cx="16" cy="25" rx="3" ry="7" fill="#fff"/>
      <ellipse cx="7" cy="16" rx="7" ry="3" fill="#fff"/>
      <ellipse cx="25" cy="16" rx="7" ry="3" fill="#fff"/>
      <ellipse cx="9" cy="9" rx="4" ry="2" fill="#fff"/>
      <ellipse cx="23" cy="9" rx="4" ry="2" fill="#fff"/>
      <ellipse cx="9" cy="23" rx="4" ry="2" fill="#fff"/>
      <ellipse cx="23" cy="23" rx="4" ry="2" fill="#fff"/>
    </svg>
  ),
  // Цветочек 3 — сакура
  (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
      <circle cx="16" cy="16" r="3" fill="#f8bbd0"/>
      <path d="M16 5 Q18 10 16 16 Q14 10 16 5" fill="#f48fb1"/>
      <path d="M16 27 Q18 22 16 16 Q14 22 16 27" fill="#f48fb1"/>
      <path d="M5 16 Q10 18 16 16 Q10 14 5 16" fill="#f48fb1"/>
      <path d="M27 16 Q22 18 16 16 Q22 14 27 16" fill="#f48fb1"/>
      <ellipse cx="10" cy="10" rx="2" ry="4" fill="#f8bbd0"/>
      <ellipse cx="22" cy="10" rx="2" ry="4" fill="#f8bbd0"/>
      <ellipse cx="10" cy="22" rx="2" ry="4" fill="#f8bbd0"/>
      <ellipse cx="22" cy="22" rx="2" ry="4" fill="#f8bbd0"/>
    </svg>
  ),
];

function randomBetween(a, b) {
  return a + Math.random() * (b - a);
}

function FallingFlowers() {
  const [flowers, setFlowers] = useState([]);
  const headerHeightRef = useRef(0);

  useEffect(() => {
    // Определяем высоту хедера
    const header = document.querySelector('.header');
    headerHeightRef.current = header ? header.offsetHeight : 40;
  }, []);

  useEffect(() => {
    let running = true;
    function addFlower() {
      if (!running) return;
      setFlowers(flowers => [
        ...flowers,
        {
          left: randomBetween(10, 90),
          size: randomBetween(2, 6),
          duration: randomBetween(5, 12),
          svgIdx: Math.floor(Math.random() * FLOWER_SVGS.length),
          rotate: randomBetween(-30, 30),
          id: Math.random().toString(36).slice(2),
          start: Date.now(),
        },
      ]);
      setTimeout(addFlower, randomBetween(50, 400));
    }
    addFlower();
    return () => { running = false; };
  }, []);

  // Удаляем цветочки после завершения анимации
  useEffect(() => {
    if (!flowers.length) return;
    const interval = setInterval(() => {
      setFlowers(flowers => flowers.filter(f => Date.now() - f.start < f.duration * 1000));
    }, 1000);
    return () => clearInterval(interval);
  }, [flowers]);

  // Высота падения
  const fallHeight = (headerHeightRef.current || 60) + 200;

  return (
    <div style={{
      pointerEvents: 'none',
      position: 'fixed',
      top: 0,
      left: 0,
    //   width: '100vw',
      width: '90%',
      height: '100vh',
      zIndex: 0,
      overflow: 'hidden',
    }}>
      {flowers.map((f) => (
        <div
          key={f.id}
          style={{
            position: 'absolute',
            left: `${f.left}%`,
            top: -40,
            width: f.size,
            height: f.size,
            opacity: 0.85,
            transform: `rotate(${f.rotate}deg)`
          }}
        >
          <div
            style={{
              width: '90%',
              height: '100%',
              animation: `fall-flower-custom ${f.duration}s linear 0s forwards`,
            }}
          >
            {FLOWER_SVGS[f.svgIdx]}
          </div>
        </div>
      ))}
      <style>{`
        @keyframes fall-flower-custom {
          0% { transform: translateY(0); opacity: 0.9; }
          90% { opacity: 0.85; }
          100% { transform: translateY(${fallHeight}px); opacity: 0; }
        }
      `}</style>
    </div>
  );
}

export default FallingFlowers; 