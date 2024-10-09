import React from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Sistema de Vigilancia Inteligente</h1>
        <p>Transmisión de Video en Tiempo Real con Detección de Objetos</p>
        {/* Mostrar la transmisión de video desde Flask */}
        <img
          src="http://127.0.0.1:5000/video_feed"
          alt="Video en tiempo real"
          style={{ width: '80%', border: '2px solid #ccc' }}
        />
      </header>
    </div>
  );
}

export default App;
