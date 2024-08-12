import axios from "axios";
import ENDPOINTS from "./endpoints";
import { TAddChatMessageDto, TChatMessageDto, TCreateChatDto, ChatRoles, TChatDto, TChatMessage, TUserDto } from "../utils/types";

export const getChatsByUser = async (user: TUserDto) : Promise<TChatDto[]> => {
    try {
        const response = await axios.get(ENDPOINTS.CHATS_BY_USER(user.id));
        const chats : TChatDto[] = response.data.data;
        return chats;
    } catch (error) {
        console.log(error);
        throw error;
    }
};

export const getChatConversation = async (chatId: string) => {
    try {
        const response = await axios.get(ENDPOINTS.CHAT_CONVERSATIONS(chatId));
        const chatHistory = response.data.data;
        return chatHistory;
    } catch (error) {
        console.log(error);
        throw error;
    }
}

export const addChatMessage = async (chatId: string, message: string): Promise<TChatMessage> => {
    const newMessage: TAddChatMessageDto = {
        chatId: chatId,
        content: message,
        role: ChatRoles[ChatRoles.User]
    }
    
    try {
        const response = await axios.post(ENDPOINTS.CHAT_CONVERSATIONS(chatId), newMessage, {
            headers: {
                "Content-Type": "application/json",
            },
        });

        const message : TChatMessageDto = response.data.data;
        console.log(message);
        return {
            id: message.id,
            content: message.content,
            role: message.role
        };
    } catch (error) {
        console.log(error);
        throw error;
    }
}

export const craeteNewChat = async (userId: string): Promise<TChatMessageDto> => {
    try {
        const createChat : TCreateChatDto = {
            userId: userId
        };

        const response = await axios.post(ENDPOINTS.CREATE_CHAT, createChat, {
            headers: {
                "Content-Type": "application/json",
            },
        });

        const newMessage : TChatMessageDto = response.data.data;
        console.log(newMessage);
        return newMessage;
    } catch (error) {
        console.log(error);
        throw error;
    }
}

export const deleteChatById = async (chatId: string) : Promise<boolean> => {
    try {
        const response = await axios.delete(ENDPOINTS.DELETE_CHAT(chatId));
        if (response.status === 204) {
            return true;
        }
        return false;
    } catch (error) {
        console.log(error);
        throw error;
    }
}