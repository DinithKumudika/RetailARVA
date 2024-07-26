import axios from "axios";

export const loginUser = async (userData) => {
    try {
        const response = await axios.post("/api/users/login", userData, {
            headers: {
                "Content-Type": "application/json",
            },
        });
        const res = await response.data;
        if (res) {
            console.log(res);
            const user = res.data;
            return user;
        }
        throw new Error(res.message);
    } catch (err) {
        console.error(err);
    }
}
