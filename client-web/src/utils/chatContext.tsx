import { createContext, useState, useRef, ReactNode } from "react";
import { HubConnection, HubConnectionBuilder, LogLevel } from "@microsoft/signalr";
import { ChatRoles, TChatContext, TChatDto, TChatMessage, TStreamMessage } from "./types";
import ENDPOINTS from "../services/endpoints";

const ChatContext = createContext<TChatContext | null>(null);

interface ChatProviderProps {
  children: ReactNode;
};

const ChatProvider = ({ children }: ChatProviderProps) => {
  const [chats, setChats] = useState<TChatDto[]>([]);
  const [messages, setMessages] = useState<TChatMessage[]>([]);
  // const [connection, setConnection] = useState();
  const [loading, setLoading] = useState<boolean>(false);
  const [chatResponseLoading, setChatResponseLoading] = useState<boolean>(false);
  const msgEnd = useRef<HTMLDivElement>(null);
  const [activeChatId, setActiveChatId] = useState<string | null>(null);
  const connectionRef = useRef<HubConnection | null>(null);
  const [firstChunkReceived, setFirstChunkRecieved] = useState<boolean>(false);
  const [partialMessage, setPartialMessage] = useState<string>("");
  const responseRef = useRef<string>("");


  const joinChat = async (userId: string, chatId: string) => {
    // initiate connection
    try {
      const conn: HubConnection = new HubConnectionBuilder()
        .withUrl(ENDPOINTS.HUB_CONNECTION)
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

  const getAssistantResponse = async (userId: string, message: string) => {
    if (connectionRef.current) {
      console.log(connectionRef.current);
      const userConnection = { userId: userId, chatId: activeChatId };
      console.log(userConnection);

      connectionRef.current.stream("StreamMessage", userConnection, message)
        .subscribe({
          next: (msgDto: TStreamMessage) => {
            setChatResponseLoading(false);
            setFirstChunkRecieved(true);
            responseRef.current = responseRef.current + msgDto.content;
            // Update the partial message to display it in real-time
            setPartialMessage(responseRef.current);
            console.log("content:", msgDto.content);
            console.log("chat id:", msgDto.chatId);
            console.log("role:", msgDto.role);
          },
          complete: async () => {
            // When the stream is done, add the full message to the messages array
            setMessages((prevMessages) => [
              ...prevMessages,
              {
                id: "",
                content: responseRef.current,
                role: ChatRoles[ChatRoles.Assistant]
              }
            ]);
            setPartialMessage("");
            console.log("Streaming complete.");
            setChatResponseLoading(false);
            setFirstChunkRecieved(false);
          },
          error: (err: unknown) => {
            console.error("Streaming error: ", err);
            setChatResponseLoading(false);
            setFirstChunkRecieved(false);
          }
        });
    }
    else {
      console.log("no connection");
    }
  };

  return (<ChatContext.Provider value={{
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
      partialMessage,
      setPartialMessage,
      setChatResponseLoading,
      firstChunkReceived,
      setFirstChunkRecieved,
      connectionRef,
      getAssistantResponse,
    }}>{children}
    </ChatContext.Provider>)
};

export { ChatContext, ChatProvider };

