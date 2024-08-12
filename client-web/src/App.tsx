import Home from "./pages/Home";
import Login from "./pages/Login";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import PrivateRoute from "./components/PrivateRoute";
import { AuthProvider } from "./utils/authContext";
import { ChatProvider } from "./utils/chatContext";
const App = () => {
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
