import { createContext, ReactNode, useState } from "react";
import { TAppContext } from "./types";

const AppContext = createContext<TAppContext | null>(null);

interface AppProviderProps {
  children: ReactNode;
}

const AppProvider = ({ children }: AppProviderProps) => {
  const [showSlide, setShowSlide] = useState(false);
  const [Mobile, setMobile] = useState(false);

  return (
    <AppContext.Provider
      value={{
        showSlide,
        setShowSlide,
        Mobile,
        setMobile,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export { AppContext, AppProvider };

