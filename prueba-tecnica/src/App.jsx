import React from 'react';
import './App.css';
import Countries from './Countries'; // Importar el componente Countries

function App() {
  return (
    <div>
      <h1 className='titulo'>Bienvenido a mi aplicación de países</h1>
      <Countries /> {/* Renderiza el componente Countries */}
    </div>
  );
}

export default App;
