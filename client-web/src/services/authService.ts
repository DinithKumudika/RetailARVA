import axios from "axios";
import ENDPOINTS from "./endpoints";
import { TLoginUserDto, TUserDto } from "../utils/types";

export const loginUser = async (userData: TLoginUserDto): Promise<TUserDto> => {

    console.log(ENDPOINTS.LOGIN_USER);
    const response = await axios.post(ENDPOINTS.LOGIN_USER, userData, {
        headers: {
            "Content-Type": "application/json",
        },
    });
    const res = await response.data;
    if (res) {
        console.log(res);
        const user : TUserDto = res.data;
        return user;
    }
    throw new Error(res.message);
}
