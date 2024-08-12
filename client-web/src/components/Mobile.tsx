import { AiOutlinePlus } from "react-icons/ai";
import { SlOptions } from "react-icons/sl";
import { MdClose } from "react-icons/md";
import useApp from "../utils/useApp";
import useChat from "../utils/useChat";
import {
  deleteChatById,
  getChatConversation
} from "../services/chatService";
import useAuth from "../utils/useAuth";
import { FiMessageSquare, FiTrash2 } from "react-icons/fi";
import { useEffect, useRef, useState } from "react";

const Mobile = () => {
  const { Mobile, setMobile } = useApp();
  const { chats, setChats, setMessages, setLoading, joinChat, activeChatId, setActiveChatId } = useChat();
  const { user, logOutAction } = useAuth();
  const [showMenu, setShowMenu] = useState(false);

  const menuRef = useRef<HTMLDivElement | null>(null);

  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };


  // logout user
  const handleLogout = () => {
    logOutAction();
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
      setShowMenu(false);
    }
  };

  const handleChatClick = async (chatId: string) => {
    try {
      setLoading(true);
      if (user && user.id) {
        joinChat(user.id, chatId);
      }
      const chatHistory = await getChatConversation(chatId);
      console.log(chatHistory);
      setMessages(chatHistory);
      setActiveChatId(chatId);
      setLoading(false);
    } catch (error) {
      console.log(error);
    }
  }

  // delete chat
  const handleChatDelete = async (chatId: string) => {
    try {
      await deleteChatById(chatId);
      const updatedChats = chats.filter((chat) => chat.id !== chatId);
      setChats(updatedChats);
      if (activeChatId === chatId) {
        setActiveChatId(null);
        setMessages([]);
      }
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {

    if (showMenu) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };

  }, [showMenu]);


  return (
    <div className="absolute left-0 top-0 w-full z-50  bg-black/40 flex justify-between items-start">
      <div
        className={
          Mobile
            ? "h-screen bg-gray-900 w-[300px]  flex items-center justify-between p-2 text-white flex-col translate-x-0"
            : "hidden"
        }
      >
        <div className="flex items-start justify-between w-full">
          <span
            className="border border-gray-600  rounded w-full py-2 text-xs flex gap-1 items-center justify-center cursor-pointer "
            onClick={() => window.location.reload()}
          >
            <AiOutlinePlus fontSize={18} />
            New Chat
          </span>
        </div>
        {/* middle section  */}
        <div className="h-[80%] w-full p-2 flex items-start justify-start flex-col overflow-hidden overflow-y-auto text-sm scroll my-2">
          {/* msg  */}
          {chats.map((chat) => (
            <span
              className={`rounded w-full py-3 px-2 text-xs my-2 flex gap-1 items-center justify-between cursor-pointer transition-all duration-300 overflow-hidden truncate whitespace-nowrap ${activeChatId === chat.id ? "bg-gray-800" : "hover:bg-gray-800"
                }`}
              chat-title={chat.title}
              onClick={() => handleChatClick(chat.id)}
              key={chat.id}
            >
              <span className="flex gap-2 items-center justify-center text-base">
                <FiMessageSquare />
                <span className="text-sm">{chat.title}</span>
              </span>
              <FiTrash2 size={"15"} color="red" onClick={() => handleChatDelete(chat.id)} />
            </span>
          ))}
        </div>
        {/* bottom section  */}
        <div className="w-full border-t border-gray-600 flex flex-col gap-2 items-center justify-center p-2">
          <span className="rounded w-full py-2 px-2 text-xs flex gap-1 items-center justify-between cursor-pointer hover:bg-gray-800 transition-all duration-300">
            <span className="flex gap-2 items-center justify-center text-sm font-bold">
            <img
              src="/user.png"
              alt="user"
              className="w-8 h-8 object-cover rounded-sm"
            />
            {user!.firstName + " " + user!.lastName}
            </span>
            <span className="rounded-md  px-1.5 py-0.5 text-xs font-medium uppercase text-gray-500" onClick={toggleMenu}>
              <SlOptions />
            </span>
          </span>
          {showMenu && (
          <div ref={menuRef} className="absolute bottom-12 right-2 w-48 bg-gray-800 border border-gray-600 rounded-md shadow-lg z-10">
            <span
              className="block px-4 py-2 text-sm text-white hover:bg-gray-700 cursor-pointer"
              onClick={handleLogout}
            >
              Logout
            </span>
          </div>
        )}
        </div>
      </div>
      {Mobile && (
        <span
          className="border border-gray-600 text-white m-2 rounded px-3 py-[9px] flex items-center justify-center cursor-pointer"
          title="Close sidebar"
          onClick={() => setMobile(!Mobile)}
        >
          <MdClose />
        </span>
      )}
    </div>
  );
};

export default Mobile;
