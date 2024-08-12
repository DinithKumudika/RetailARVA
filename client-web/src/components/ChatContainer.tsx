import { useState } from "react";
import { LuPanelLeftOpen } from "react-icons/lu";
import { HiOutlineMenuAlt2 } from "react-icons/hi";
import { RiSendPlane2Fill } from "react-icons/ri";
import useChat from "../utils/useChat";
import Chat from "./Chat";
import useAuth from "../utils/useAuth";
import { addChatMessage } from "../services/chatService";
import { TChatMessage } from "../utils/types";
import useApp from "../utils/useApp";

function ChatContainer() {
  const {
    setShowSlide,
    showSlide,
    setMobile,
    Mobile,
  } = useApp();
  const { activeChatId, setMessages, setChatResponseLoading, getAssistantResponse} = useChat();
  const { user } = useAuth();

  const [message, setMessage] = useState<string>("");

  const handleKeyUp = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSend(e);
    }
  };

  const handleSend = async (e: React.FormEvent | KeyboardEvent) => {
    e.preventDefault();
    if (message.trim() === "") return;

    if(!activeChatId)
    {
      throw new Error("active chat id not set");
    }

    const addedMessage : TChatMessage = await addChatMessage(activeChatId, message);
    console.log(addedMessage);
    setMessage("");
    setMessages((prevMessages : TChatMessage[]) => [...prevMessages, addedMessage]);
    setChatResponseLoading(true);
    
    if(!user)
    {
      throw new Error("user cannot be null");
    }
    else {
      getAssistantResponse(user.id, message);
    }
  }

  return (
    <div
      className={
        showSlide
          ? "h-screen w-screen bg-gray-700 flex items-start justify-between flex-col p-2"
          : "h-screen w-full lg:w-[calc(100%-300px)] bg-gray-700 flex items-start justify-between flex-col p-2"
      }
    >
      <span
        className="rounded px-3 py-[9px] hidden lg:flex items-center justify-center cursor-pointer text-white m-1 hover:bg-gray-600 duration-200"
        title="Open sidebar"
        onClick={() => setShowSlide(!showSlide)}
      >
        {showSlide && <LuPanelLeftOpen />}
      </span>
      <span
        className="rounded px-3 py-[9px] lg:hidden flex items-center justify-center cursor-pointer text-white mt-0 mb-3 border border-gray-600"
        title="Open sidebar"
        onClick={() => setMobile(!Mobile)}
      >
        <HiOutlineMenuAlt2 fontSize={20} />
      </span>
      {/* chat section */}
      <Chat />
      {/* chat input section */}
      <div className=" w-full  m-auto flex items-center justify-center flex-col gap-2 my-2">
        <span className="flex gap-2 items-center justify-center bg-gray-600 rounded-lg shadow-md w-[90%] lg:w-2/5 xl:w-1/2">
          <input
            type="text"
            placeholder="Send a message"
            className="h-full  text-white bg-transparent px-3 py-4 w-full border-none outline-none text-base"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyUp={handleKeyUp}
          />
          <RiSendPlane2Fill
            title="send message"
            className={
              message.length <= 0
                ? "text-gray-400 cursor-auto mx-3 text-xl"
                : "text-white cursor-pointer mx-3 text-3xl bg-green-500 p-1 rounded shadow-md "
            }
            onClick={handleSend}
          />
        </span>
      </div>
    </div>
  );
}

export default ChatContainer;
