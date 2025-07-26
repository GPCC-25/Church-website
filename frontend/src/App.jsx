import { BrowserRouter, Routes, Route } from "react-router-dom"




function App() {

  return(
    <BrowserRouter>
      <Routes>
        <Route index element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
