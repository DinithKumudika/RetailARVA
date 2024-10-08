import { useContext } from "react";
import { AppContext } from "./appContext";
import { TAppContext } from "./types";

const useApp = (): TAppContext => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error("useApp must be used within an AppProvider");
    }
    return context;
};

export default useApp;
