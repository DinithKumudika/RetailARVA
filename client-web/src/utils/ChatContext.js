import { createContext, useState, useRef, useContext } from "react";
import { HubConnectionBuilder, LogLevel } from "@microsoft/signalr";
export const ChatContext = createContext();

const ChatProvider = ({ children }) => {
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  // const [connection, setConnection] = useState();
  const [loading, setLoading] = useState(false);
  const [chatResponseLoading, setChatResponseLoading] = useState(false);
  const msgEnd = useRef(null);
  const [activeChatId, setActiveChatId] = useState(null);
  const connectionRef = useRef(null);
  const [chatResponse, setChatResponse] = useState("");
  const [firstChunkReceived, setFirstChunkRecieved] = useState(false);

  const joinChat = async (userId, chatId) => {
    // initiate connection
    try {
      const conn = new HubConnectionBuilder()
        .withUrl("http://localhost:5031/chatHub")
        .configureLogging(LogLevel.Information)
        .build();

      // setup handler
      conn.on("JoinChatThread", ({ userId, chatId }) => {
        console.log(`connection successfull, ${userId} joined chat ${chatId}`);
      });

      await conn.start();
      await conn.invoke("JoinChatThread", { userId, chatId });
      connectionRef.current = conn;
    } catch (error) {
      console.log("SignalR Connection Error: ", error);
      throw error;
    }
  };

  const getAssistantResponse = async (userId, message) => {
    if (connectionRef.current) {
      console.log(connectionRef.current);
      const userConnection = { userId: userId, chatId: activeChatId };
      console.log(userConnection);

      connectionRef.current.stream("StreamMessage", userConnection, message)
        .subscribe({
          next: (msg) => {
            setChatResponseLoading(false);
            setFirstChunkRecieved(true);
            console.log(msg);
            setChatResponse(prevMessage => [...prevMessage, msg]);
          },
          complete: () => {
            console.log("Streaming complete.");
            setChatResponseLoading(false);
            setFirstChunkRecieved(false);
          },
          error: (err) => {
            console.error("Streaming error: ", err);
            setChatResponseLoading(false);
            setFirstChunkRecieved(false);
          }
        });
    }
    else {
      console.log("no connection");
    }
  }

  return (
    <ChatContext.Provider
      value={{
        chats,
        setChats,
        messages,
        setMessages,
        loading,
        setLoading,
        msgEnd,
        joinChat,
        activeChatId,
        setActiveChatId,
        chatResponseLoading,
        chatResponse,
        setChatResponse,
        setChatResponseLoading,
        firstChunkReceived,
        setFirstChunkRecieved,
        connectionRef,
        getAssistantResponse
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
