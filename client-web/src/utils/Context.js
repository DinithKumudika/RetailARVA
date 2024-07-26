import { createContext, useState } from "react";
export const ContextApp = createContext();

const AppContext = ({ children }) => {
  const [showSlide, setShowSlide] = useState(false);
  const [Mobile, setMobile] = useState(false);
  const [chatValue, setChatValue] = useState("");

  // button Click function
  // const handleSend = async () => {
  //   const text = chatValue;
  //   setChatValue("");
  //   setMessages([...messages, { text, isBot: false }]);
  //   const res = await sendMsgToAI(text);
  //   setMessages([
  //     ...messages,
  //     { text, isBot: false },
  //     { text: res, isBot: true },
  //   ]);
  // };

  return (
    <ContextApp.Provider
      value={{
        showSlide,
        setShowSlide,
        Mobile,
        setMobile,
        chatValue,
        setChatValue,
      }}
    >
      {children}
    </ContextApp.Provider>
  );
};
export default AppContext;
