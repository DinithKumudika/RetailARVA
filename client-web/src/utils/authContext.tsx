import { createContext, useState, ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";
import { TLoginUserDto, TAuthContext, TUserDto } from "./types";

const AuthContext = createContext<TAuthContext | null>(null);

interface AuthProviderProps {
    children: ReactNode;
}

const AuthProvider = ({ children }: AuthProviderProps) => {
    const [user, setUser] = useState<TUserDto | null>(() => {
        const savedUser = localStorage.getItem("user");
        return savedUser ? JSON.parse(savedUser) : null;
    });
    const navigate = useNavigate();

    const loginAction = async (data : TLoginUserDto) => {
        try {
            const user: TUserDto = await loginUser(data);
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

    return (<AuthContext.Provider value={{
            user,
            loginAction,
            logOutAction
        }}>{children}
    </AuthContext.Provider>);
};

export {AuthContext, AuthProvider};