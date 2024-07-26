import React, { useContext, useState, useRef, useEffect } from "react";
import { AiOutlinePlus } from "react-icons/ai";
import { LuPanelLeftClose } from "react-icons/lu";
import { FiMessageSquare, FiTrash2 } from "react-icons/fi";
import { SlOptions } from "react-icons/sl";
import { useAuth } from "../utils/AuthContext";
import { getChatsByUser, getChatConversation, craeteNewChat, deleteChatById } from "../services/chatService";
import { ContextApp } from "../utils/Context";
import { useChat } from "../utils/ChatContext";

function LeftNav() {
  const { setShowSlide, showSlide } = useContext(ContextApp);
  const { chats, setChats, setMessages, joinChat, setLoading, activeChatId, setActiveChatId } = useChat();
  const { user, logOutAction } = useAuth();
  const [showMenu, setShowMenu] = useState(false);
  

  const menuRef = useRef(null);

  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  // logout user
  const handleLogout = () => {
    logOutAction();
    setShowMenu(false);
  };

  const handleClickOutside = (event) => {
    if (menuRef.current && !menuRef.current.contains(event.target)) {
      setShowMenu(false);
    }
  };


  const handleChatClick = async (chatId) => {
    try {
      const chatHistory = await getChatConversation(chatId);
      console.log(chatHistory);
      setMessages(chatHistory);
      setActiveChatId(chatId);
    } catch (error) {
      console.log(error);
    }
  }

  // delete chat
  const handleChatDelete = async (chatId) => {
    try {
      const result = await deleteChatById(chatId);
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

  // create new chat thread
  const handleNewChat = async (userId) => {
    setLoading(true);
    try {
      // create new chat Id and only make it permanent when the first chat message sent
      const chatMessage = await craeteNewChat(userId);
      joinChat(userId, chatMessage.chatId);
      setMessages([chatMessage]);
      const chats = await getChatsByUser(user);
      setChats(chats);
      setActiveChatId(chatMessage.chatId);
    } catch (error) {
      console.log(error);
    }
    finally {
      setLoading(false); // End loading
    }
  }

  useEffect(() => {
    const fetchChats = async (user) => {
      try {
        const chats = await getChatsByUser(user);
        setChats(chats);
        console.log(chats);
      }
      catch (error) {
        console.error("Error fetching chats:", error);
      }
    };

    if (user && user.id) {
      fetchChats(user);
    }

    if (showMenu) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };

  }, [showMenu, setChats, user]);

  return (
    // top section
    <div
      className={
        !showSlide
          ? "h-screen bg-gray-900 w-[300px] border-r border-gray-500 hidden lg:flex items-center justify-between p-2 text-white flex-col translate-x-0"
          : "hidden"
      }
    >
      <div className="flex items-start justify-between w-full">
        <span
          className="border border-gray-600  rounded w-[80%] py-2 text-xs flex gap-1 items-center justify-center cursor-pointer"
          onClick={() => handleNewChat(user.id)}
        >
          <AiOutlinePlus fontSize={18} />
          New Chat
        </span>
        <span
          className="border border-gray-600  rounded px-3 py-[9px] flex items-center justify-center cursor-pointer"
          title="Close sidebar"
          onClick={() => setShowSlide(!showSlide)}
        >
          <LuPanelLeftClose />
        </span>
      </div>
      {/* middle section  */}
      <div className="h-[80%] w-full p-2 flex items-start justify-start flex-col overflow-hidden overflow-y-auto text-sm scroll my-2">
        {/* msg  */}
        {chats.map((chat) => (
          <span
            className="rounded w-full py-3 px-2 text-xs my-2 flex gap-1 items-center justify-between cursor-pointer hover:bg-gray-800 transition-all duration-300 overflow-hidden truncate whitespace-nowrap"
            value={chat.title}
            onClick={() => handleChatClick(chat.id)}
            key={chat.id}
          >
            <span className="flex gap-2 items-center justify-center text-base">
              <FiMessageSquare />
              <span className="text-sm">{chat.title}</span>
            </span>
            <FiTrash2 size={"15"} color="red" onClick={()=> handleChatDelete(chat.id)}/>
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
            {user.firstName + " " + user.lastName}
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
  );
}

export default LeftNav;
