import { createContext, useRef, useState, useContext } from "react";
import { HubConnectionBuilder, LogLevel } from "@microsoft/signalr";
export const ChatContext = createContext();

const ChatProvider = ({ children }) => {
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  const [connection, setConnection] = useState();
  const [loading, setLoading] = useState(false);
  const msgEnd = useRef(null);
  const [activeChatId, setActiveChatId] = useState(null);

  const joinChat = async (userId, chatId) => {
    // initiate connection
    try {
      const conn = new HubConnectionBuilder()
        .withUrl("/chatHub")
        .configureLogging(LogLevel.Information)
        .build();

      // setup handler
      conn.on("JoinChatThread", ({userId, chatId}) => {
        console.log(`connection successfull, ${userId} joined chat ${chatId}`);
      });

      await conn.start();
      await conn.invoke("JoinChatThread", { userId, chatId });
      setConnection(conn);
    } catch (error) {
      throw error;
    }
  };

  return (
    <ChatContext.Provider
      value={{
        chats,
        setChats,
        messages,
        setMessages,
        loading,
        setLoading,
        connection,
        setConnection,
        msgEnd,
        joinChat,
        activeChatId,
        setActiveChatId,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export default ChatProvider;

export const useChat = () => {
    return useContext(ChatContext);
};
