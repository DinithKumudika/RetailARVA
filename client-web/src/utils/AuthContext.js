import { useContext, createContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const savedUser = localStorage.getItem("user");
        return savedUser ? JSON.parse(savedUser) : null;
    });
    const navigate = useNavigate();

    const loginAction = async (data) => {
        try {
            const user = await loginUser(data);
            if (user) {
                setUser(user);
                localStorage.setItem("user", JSON.stringify(user));
                navigate(`/chats/${user.id}`);
                return;
            }

        } catch (err) {
            console.error(err);
        }
    };

    const logOutAction = () => {
        setUser(null);
        localStorage.removeItem("user");
        navigate("/login");
    };

    return <AuthContext.Provider
        value={{
            user,
            loginAction,
            logOutAction
        }}>{children}
    </AuthContext.Provider>;
};

export default AuthProvider;

export const useAuth = () => {
    return useContext(AuthContext);
};

