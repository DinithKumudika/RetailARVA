import { useContext } from "react";
import { TChatContext } from "./types";
import { ChatContext } from "./chatContext";

const useChat = (): TChatContext => {
    const context = useContext(ChatContext);
    if (!context) {
      throw new Error("useChat must be used within a ChatProvider");
    }
  
    return context;
  };

export default useChat;
  