import { useEffect } from "react";

function App() {
  useEffect(() => {
    fetch("http://127.0.0.1:5000/health")
      .then(res => res.json())
      .then(data => console.log(data));
  }, []);

  return <h1>Frontend Working</h1>;
}

export default App;