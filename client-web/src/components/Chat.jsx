import React from "react";
import { useChat } from "../utils/ChatContext";
import LoadingDots from "../components/LoadingDots";

function Chat() {
  const { messages, msgEnd, loading } = useChat();
  return (
    <div className=" w-full h-[85%] flex items-center justify-center overflow-hidden overflow-y-auto px-2 py-1 scroll">
      {loading ? (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-50">
          <LoadingDots />
        </div>
      ) : (<div className="w-full lg:w-4/5 flex flex-col h-full items-start justify-start">
        {messages && messages.length > 0 ? (messages?.map((message) => (
          <div
            key={message.id}
            className={`w-full flex ${message.role === "Assistant" ? "justify-start" : "justify-end"} my-2`}
          >
            <span
              className={`flex rounded-md max-w-[75%] ${message.role === "Assistant" ? "justify-start" : "justify-end"} items-start gap-2 lg:gap-5 my-2 p-3 ${message.role === "Assistant" ? "bg-gray-800/80" : "bg-gray-600/80"}`}
            >
              {message.role === "Assistant" && (
                <img
                  src="/icon.png"
                  alt="assistant"
                  className="w-10 h-10 rounded object-cover"
                />
              )}
              <p className="text-white text-[15px]">{message.content}</p>
            </span>
          </div>
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
        <div ref={msgEnd} />
      </div>)}

    </div>
  );
}

export default Chat;
