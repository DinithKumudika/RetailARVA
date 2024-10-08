import React from "react";
import { useChat } from "../utils/chatContext";
import LoadingDots from "../components/LoadingDots";
import ChatMessage from "./ChatMessage";
import LoadingMessage from "./LoadingMessage";

function Chat() {
  const { messages, chatResponseLoading, msgEnd, loading, chatResponse, firstChunkReceived } = useChat();
  return (
    <div className=" w-full h-[85%] flex items-center justify-center overflow-hidden overflow-y-auto px-2 py-1 scroll">
      {loading ? (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-50">
          <LoadingDots size={8} />
        </div>
      ) : (
        <div className="w-full lg:w-4/5 flex flex-col h-full items-start justify-start">
          {messages && messages.length > 0 ? (messages?.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))) : (
            <div className="w-full h-full flex flex-col items-center justify-center">
              <img
                src="/icon.png"
                alt="assistant"
                className="w-40 h-40 rounded object-cover mb-4"
              />
              <p className="text-gray-500 text-center mt-4">
                No chat history available. Start by sending a message to initiate a conversation.
              </p>
            </div>
          )}
          {
            chatResponseLoading ? (<LoadingMessage role={"Assistant"} />)
              : (
                firstChunkReceived && <ChatMessage message={chatResponse}/>
              )
          }
          <div ref={msgEnd} />
        </div>)}

    </div>
  );
}

export default Chat;
