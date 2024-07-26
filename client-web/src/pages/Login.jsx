import React, { useState } from 'react'
import { useAuth } from '../utils/AuthContext';

const Login = () => {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const auth = useAuth();

    const handleLogin = async (e) => {
        e.preventDefault();
        const userData = {
            firstName,
            lastName,
        };

        if (userData.firstName !== "" && userData.lastName !== "") {
            await auth.loginAction(userData);
            return;
        }
        alert("first name and last name required");
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-background bg-gray-700">
            <div className="bg-card dark:bg-card bg-gray-400 rounded-lg p-8 shadow-md w-80">
                <input
                    type="text"
                    placeholder="Enter First Name"
                    className="w-full px-3 py-2 mb-4 rounded-lg bg-input dark:bg-input text-primary dark:text-primary-foreground focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primary"
                    onChange={(e) => setFirstName(e.target.value)}
                    value={firstName}
                />

                <input
                    type="text"
                    placeholder="Enter Last Name"
                    className="w-full px-3 py-2 mb-4 rounded-lg bg-input dark:bg-input text-primary dark:text-primary-foreground focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primary"
                    onChange={(e) => setLastName(e.target.value)}
                    value={lastName}
                />
                <button
                    className="w-full bg-gray-800/80 text-white rounded-lg py-2 transition-colors duration-300 hover:bg-primary/80 focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-primary"
                    onClick={handleLogin}
                >
                    Login
                </button>
            </div>
        </div>
    )
}

export default Login