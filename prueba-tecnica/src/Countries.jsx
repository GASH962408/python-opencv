import React from 'react'

const Countries = () => {

const [frase, setFrase] = useState("");

return(
  <div>
    <h2>Ingresa frase:</h2>
    <input type="text"
     value={frase}
     onChange={(e)=> setFrase(e.target.value)}
     placeholder='Ingresa tu texto aqui'
     />
  </div>
)

}
export default Countries
