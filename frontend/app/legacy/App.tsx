import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './components/Home';
import Setting from './components/Setting';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/legacy" element={<Home />} />
        <Route path="/legacy/setting" element={<Setting />} />
      </Routes>
    </Router>
  );
}

export default App;
