import React, { useState } from 'react';
import PropTypes from 'prop-types';

const Countries = ({initial=0}) => {
  const [contador, setContador] = useState(initial);

  const incrementar = () => {setContador(contador+1);}
  const decrementar = () => {if (contador>0) {setContador(contador-1);}}
  const reset = () => {setContador(0)}

  return(<div>
      <p>El contador esta en : {contador}</p>
      <button onClick={incrementar}>+</button>
      <button onClick={decrementar}>-</button>
      <button onClick={reset}>reset</button>
      </div>)
}
Countries.propTypes={
  initial:PropTypes.number,
};

Countries.defaultProps={
  initial:0,
}



export default Countries;
