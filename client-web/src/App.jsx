import Home from "./pages/Home";
import Login from "./pages/Login";
import AuthProvider from "./utils/AuthContext";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import ChatProvider from "./utils/ChatContext";

function App() {
  return (
    <div className="overflow-hidden">
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<Login />} />
            <Route element={<PrivateRoute />}>
              <Route path="/chats/:uid" element={
                <ChatProvider>
                  <Home />
                </ChatProvider>
              } />
            </Route>
          </Routes>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
